# Smart Compressor — English Guide

[← Back to the repository overview](README.md)

## Overview

Smart Compressor is a dependency-free Python compression toolkit for files and directories. At runtime it uses Python's standard library to create archives, inspect archive statistics, and extract supported formats with path-safety checks.

It is intended for local workflows and scripts that need a predictable interface without requiring 7-Zip, native compression binaries, cloud uploads, or third-party Python runtime packages.

## Requirements

- Python 3.10 or newer
- pip for installation
- no external compression utility required

## Installation

~~~bash
git clone https://github.com/rad03i2/smart-compressor.git
cd smart-compressor
python -m pip install -e .
~~~

Verify the CLI:

~~~bash
smart-compressor --version
~~~

## CLI structure

~~~text
smart-compressor compress SOURCE OUTPUT [--level 0-9] [--overwrite] [--json]
smart-compressor inspect ARCHIVE [--json]
smart-compressor extract ARCHIVE DESTINATION [--overwrite] [--json]
~~~

## Compression

### ZIP a directory

~~~bash
smart-compressor compress ./documents ./documents.zip
~~~

### TAR + gzip

~~~bash
smart-compressor compress ./documents ./documents.tar.gz
~~~

### TAR + bzip2

~~~bash
smart-compressor compress ./documents ./documents.tar.bz2
~~~

### TAR + xz

~~~bash
smart-compressor compress ./documents ./documents.tar.xz
~~~

Short suffixes <code>.tgz</code>, <code>.tbz2</code>, and <code>.txz</code> are also detected.

### Single-file streams

~~~bash
smart-compressor compress report.csv report.csv.gz --level 9
smart-compressor compress report.csv report.csv.bz2 --level 9
smart-compressor compress report.csv report.csv.xz --level 9
~~~

Single-stream GZ, BZ2, and XZ outputs accept files only.

### Compression levels

<code>--level</code> accepts 0 through 9.

The current implementation passes the requested level to ZIP and single-file GZ/BZ2/XZ APIs. TAR.GZ, TAR.BZ2, and TAR.XZ creation currently uses the standard compression defaults exposed through <code>tarfile.open()</code> in this implementation.

## Inspection

~~~bash
smart-compressor inspect archive.zip
~~~

JSON:

~~~bash
smart-compressor inspect archive.zip --json
~~~

Archive information includes:

- path;
- format;
- member count;
- packed bytes;
- unpacked bytes;
- packed/unpacked ratio.

For GZ/BZ2/XZ streams, determining the unpacked size requires reading the decompressed stream.

## Extraction

~~~bash
smart-compressor extract archive.zip ./restored
~~~

Existing files are protected by default.

To explicitly allow replacement:

~~~bash
smart-compressor extract archive.zip ./restored --overwrite
~~~

JSON output is also supported:

~~~bash
smart-compressor extract archive.zip ./restored --json
~~~

## Extraction safety

Every member path is resolved against the requested extraction destination. A member that escapes the destination is rejected.

For TAR archives, the implementation only accepts regular files and directories. It rejects:

- symbolic links;
- hard links;
- devices;
- other special TAR members.

The project therefore includes path-traversal protection, but it does not impose CPU, memory, output-size, member-count, or decompression-ratio limits against compression bombs.

## Archive creation safety

When creating an archive:

1. the source is validated;
2. the destination is checked;
3. an output already present is rejected unless overwrite is explicit;
4. a temporary file is created in the destination directory;
5. the archive is written to the temporary file;
6. the temporary file atomically replaces the destination.

The source and output paths must differ.

## Python API

~~~python
from smart_compressor import (
    CompressionError,
    compress,
    extract,
    inspect_archive,
)

info = compress("documents", "documents.zip", level=6)
print(info.to_dict())

extract("documents.zip", "restored")

checked = inspect_archive("documents.zip")
print(checked.ratio)
~~~

## ArchiveInfo

The immutable result contains:

- <code>path</code>
- <code>format</code>
- <code>members</code>
- <code>packed_bytes</code>
- <code>unpacked_bytes</code>

The <code>ratio</code> property is <code>packed_bytes / unpacked_bytes</code>, or 0 for an empty unpacked size.

## Tests

~~~bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
smart-compressor --version
~~~

CI executes the same validation on:

- Ubuntu + Python 3.10 / 3.12 / 3.13
- Windows + Python 3.10 / 3.12 / 3.13
- macOS + Python 3.10 / 3.12 / 3.13

## Privacy

The package does not contain telemetry, a network client, or API-key configuration. Archive processing happens on local filesystem paths supplied by the caller.

That does not make every archive safe: archives can contain sensitive data, and malicious compressed content can consume large resources during inspection or extraction.

## Current limitations

- no RAR;
- no 7z;
- no Zstandard;
- no encryption or passwords;
- no multipart archives;
- no GUI;
- no extraction transaction / rollback;
- no compression-bomb resource quotas.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for format dispatch, atomic creation, inspection, and extraction safety details.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and run the full validation commands before opening a pull request.

## Author

**Radwan Abd alhady Ahmed**  
**رضوان عبدالهادي**  
GitHub: [@rad03i2](https://github.com/rad03i2)

## License

MIT — see [LICENSE](LICENSE).
