# Security Policy

Smart Compressor processes archives locally and makes no network requests.

## Supported version

Security fixes target the latest release on `main`.

## Archive safety

Extraction validates every member path against the destination directory to prevent path traversal (Zip Slip). TAR symbolic links, hard links, devices and other special members are rejected. Existing output files are not overwritten unless `--overwrite` is explicitly supplied.

Archives are untrusted input. Resource-exhaustion attacks such as compression bombs can still consume substantial disk space or CPU; inspect unknown archives and use operating-system resource controls where appropriate.

## Reporting

Please report suspected vulnerabilities privately through GitHub's security reporting facilities when available. Do not publish exploit details before a fix can be prepared.
