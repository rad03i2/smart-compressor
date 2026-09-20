import tempfile
import unittest
import zipfile
from pathlib import Path

from smart_compressor.core import CompressionError, compress, extract, inspect_archive


class SmartCompressorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_zip_directory_round_trip(self):
        source = self.root / "docs"
        source.mkdir()
        (source / "a.txt").write_text("hello " * 100, encoding="utf-8")
        (source / "nested").mkdir()
        (source / "nested" / "b.txt").write_text("world", encoding="utf-8")
        archive = self.root / "docs.zip"
        info = compress(source, archive)
        self.assertEqual(info.format, "zip")
        self.assertEqual(info.members, 2)
        out = self.root / "out"
        files = extract(archive, out)
        self.assertEqual(len(files), 2)
        self.assertEqual((out / "docs" / "nested" / "b.txt").read_text(), "world")

    def test_single_file_gzip_round_trip(self):
        source = self.root / "notes.txt"
        source.write_bytes(b"abc" * 500)
        archive = self.root / "notes.txt.gz"
        compress(source, archive, level=9)
        out = self.root / "restore"
        extract(archive, out)
        self.assertEqual((out / "notes.txt").read_bytes(), source.read_bytes())

    def test_tar_xz_round_trip(self):
        source = self.root / "data"
        source.mkdir()
        (source / "value.txt").write_text("42")
        archive = self.root / "data.tar.xz"
        compress(source, archive)
        self.assertEqual(inspect_archive(archive).format, "tar.xz")
        extract(archive, self.root / "unpacked")
        self.assertEqual((self.root / "unpacked" / "data" / "value.txt").read_text(), "42")

    def test_refuses_overwrite(self):
        source = self.root / "a.txt"
        source.write_text("a")
        output = self.root / "a.gz"
        output.write_text("existing")
        with self.assertRaises(CompressionError):
            compress(source, output)

    def test_rejects_zip_slip(self):
        archive = self.root / "evil.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("../escape.txt", "nope")
        with self.assertRaises(CompressionError):
            extract(archive, self.root / "safe")
        self.assertFalse((self.root / "escape.txt").exists())

    def test_invalid_level(self):
        source = self.root / "a.txt"
        source.write_text("a")
        with self.assertRaises(CompressionError):
            compress(source, self.root / "a.gz", level=10)


if __name__ == "__main__":
    unittest.main()
