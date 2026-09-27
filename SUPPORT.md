# Support

## Before opening an issue

1. Confirm Python 3.10 or newer is installed.
2. Install the project:
   ~~~bash
   python -m pip install -e .
   ~~~
3. Run:
   ~~~bash
   python -m compileall -q src tests
   python -m unittest discover -s tests -v
   smart-compressor --version
   ~~~
4. Reproduce the problem using a small archive containing non-sensitive test data.

## Useful bug-report details

Include:

- operating system;
- Python version;
- Smart Compressor version;
- exact CLI command;
- archive suffix;
- whether the source is a file or directory;
- expected behavior;
- actual behavior;
- stderr or traceback with private paths and data removed where necessary.

## Common questions

### Why is an existing output rejected?

Overwrite is opt-in. Use <code>--overwrite</code> only when replacing the destination is intentional.

### Why can I compress a file to .gz but not a directory?

GZ, BZ2, and XZ are single compressed streams in the current interface. Directory compression uses ZIP or TAR-based formats.

### Why does TAR.XZ ignore my requested level?

The current implementation passes <code>--level</code> to ZIP and single-file GZ/BZ2/XZ paths. TAR.GZ/TAR.BZ2/TAR.XZ creation uses the defaults from the current <code>tarfile.open()</code> path.

### Why does inspection of .xz/.gz/.bz2 take time?

The tool reads the decompressed stream to determine unpacked size for those single-stream formats.

### Does safe extraction protect against compression bombs?

No. Path traversal is checked, and unsafe TAR member types are rejected, but the project does not currently impose resource quotas.

## Security reports

Do not attach private archives, credentials, or weaponized samples to a public issue. Follow [SECURITY.md](SECURITY.md).

## Feature requests

Describe the workflow first. If the request concerns a new format, encryption, resource limits, or extraction semantics, mention compatibility and security implications.
