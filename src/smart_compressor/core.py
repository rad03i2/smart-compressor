from __future__ import annotations

import bz2
import gzip
import lzma
import os
import shutil
import tarfile
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


class CompressionError(RuntimeError):
    """Raised for invalid or unsafe compression operations."""


@dataclass(frozen=True)
class ArchiveInfo:
    path: str
    format: str
    members: int
    packed_bytes: int
    unpacked_bytes: int

    @property
    def ratio(self) -> float:
        return 0.0 if not self.unpacked_bytes else self.packed_bytes / self.unpacked_bytes

    def to_dict(self) -> dict:
        data = asdict(self)
        data["ratio"] = round(self.ratio, 4)
        return data


def _format(path: Path) -> str:
    name = path.name.lower()
    if name.endswith(".tar.gz") or name.endswith(".tgz"):
        return "tar.gz"
    if name.endswith(".tar.bz2") or name.endswith(".tbz2"):
        return "tar.bz2"
    if name.endswith(".tar.xz") or name.endswith(".txz"):
        return "tar.xz"
    return path.suffix.lower().lstrip(".")


def _files(source: Path) -> Iterable[tuple[Path, str]]:
    if source.is_file():
        yield source, source.name
        return
    for item in sorted(source.rglob("*")):
        if item.is_file() and not item.is_symlink():
            yield item, str(Path(source.name) / item.relative_to(source))


def _safe_target(root: Path, member: str) -> Path:
    target = (root / member).resolve()
    root_resolved = root.resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise CompressionError(f"unsafe archive path: {member}") from exc
    return target


def _atomic_path(output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    os.close(fd)
    return Path(name)


def compress(source: str | Path, output: str | Path, *, level: int = 6, overwrite: bool = False) -> ArchiveInfo:
    src, out = Path(source).expanduser().resolve(), Path(output).expanduser().resolve()
    if not src.exists():
        raise CompressionError(f"source does not exist: {src}")
    if src == out:
        raise CompressionError("source and output must differ")
    if out.exists() and not overwrite:
        raise CompressionError(f"output already exists: {out}")
    if not 0 <= level <= 9:
        raise CompressionError("level must be between 0 and 9")
    fmt = _format(out)
    if src.is_dir() and fmt not in {"zip", "tar.gz", "tar.bz2", "tar.xz"}:
        raise CompressionError("directories require .zip, .tar.gz, .tar.bz2, or .tar.xz")
    temp = _atomic_path(out)
    try:
        if fmt == "zip":
            with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=level) as zf:
                for path, arcname in _files(src):
                    zf.write(path, arcname)
        elif fmt in {"tar.gz", "tar.bz2", "tar.xz"}:
            mode = {"tar.gz": "w:gz", "tar.bz2": "w:bz2", "tar.xz": "w:xz"}[fmt]
            with tarfile.open(temp, mode) as tf:
                tf.add(src, arcname=src.name, recursive=True)
        elif fmt in {"gz", "bz2", "xz"} and src.is_file():
            opener = {"gz": gzip.open, "bz2": bz2.open, "xz": lzma.open}[fmt]
            kwargs = {"compresslevel": level} if fmt in {"gz", "bz2"} else {"preset": level}
            with src.open("rb") as inp, opener(temp, "wb", **kwargs) as dst:
                shutil.copyfileobj(inp, dst, length=1024 * 1024)
        else:
            raise CompressionError("unsupported output format")
        os.replace(temp, out)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    return inspect_archive(out)


def inspect_archive(path: str | Path) -> ArchiveInfo:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise CompressionError(f"archive not found: {p}")
    fmt = _format(p)
    if fmt == "zip":
        with zipfile.ZipFile(p) as zf:
            members = zf.infolist()
            unpacked = sum(m.file_size for m in members if not m.is_dir())
            return ArchiveInfo(str(p), fmt, len(members), p.stat().st_size, unpacked)
    if fmt in {"tar.gz", "tar.bz2", "tar.xz"}:
        with tarfile.open(p, "r:*") as tf:
            members = tf.getmembers()
            return ArchiveInfo(str(p), fmt, len(members), p.stat().st_size, sum(m.size for m in members if m.isfile()))
    if fmt in {"gz", "bz2", "xz"}:
        opener = {"gz": gzip.open, "bz2": bz2.open, "xz": lzma.open}[fmt]
        total = 0
        with opener(p, "rb") as fh:
            while chunk := fh.read(1024 * 1024):
                total += len(chunk)
        return ArchiveInfo(str(p), fmt, 1, p.stat().st_size, total)
    raise CompressionError("unsupported archive format")


def extract(archive: str | Path, destination: str | Path, *, overwrite: bool = False) -> list[str]:
    src, dest = Path(archive).expanduser().resolve(), Path(destination).expanduser().resolve()
    if not src.is_file():
        raise CompressionError(f"archive not found: {src}")
    dest.mkdir(parents=True, exist_ok=True)
    fmt = _format(src)
    written: list[str] = []
    if fmt == "zip":
        with zipfile.ZipFile(src) as zf:
            for member in zf.infolist():
                target = _safe_target(dest, member.filename)
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if target.exists() and not overwrite:
                    raise CompressionError(f"target already exists: {target}")
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as inp, target.open("wb") as out:
                    shutil.copyfileobj(inp, out)
                written.append(str(target))
        return written
    if fmt in {"tar.gz", "tar.bz2", "tar.xz"}:
        with tarfile.open(src, "r:*") as tf:
            for member in tf.getmembers():
                if member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                    raise CompressionError(f"unsupported archive member: {member.name}")
                target = _safe_target(dest, member.name)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if target.exists() and not overwrite:
                    raise CompressionError(f"target already exists: {target}")
                target.parent.mkdir(parents=True, exist_ok=True)
                inp = tf.extractfile(member)
                if inp is None:
                    raise CompressionError(f"cannot read archive member: {member.name}")
                with inp, target.open("wb") as out:
                    shutil.copyfileobj(inp, out)
                written.append(str(target))
        return written
    if fmt in {"gz", "bz2", "xz"}:
        target = dest / src.stem
        if target.exists() and not overwrite:
            raise CompressionError(f"target already exists: {target}")
        opener = {"gz": gzip.open, "bz2": bz2.open, "xz": lzma.open}[fmt]
        with opener(src, "rb") as inp, target.open("wb") as out:
            shutil.copyfileobj(inp, out)
        return [str(target)]
    raise CompressionError("unsupported archive format")
