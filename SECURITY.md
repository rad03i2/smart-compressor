# Security Policy

## Scope

Smart Compressor creates, inspects, and extracts archives locally using Python's standard library.

Archives are untrusted binary input. Path validation reduces one important class of extraction vulnerability, but it does not make every archive safe to process.

## Supported code

Security fixes target the current <code>main</code> branch and any current release explicitly published by the repository.

## Extraction protections

The current implementation:

- resolves every archive member target against the chosen destination;
- rejects a target that escapes the destination;
- rejects TAR symbolic links;
- rejects TAR hard links;
- rejects TAR devices and other special members;
- refuses existing destination files unless overwrite is explicit.

These checks address path traversal and unsafe TAR member types.

## Archive creation protections

Archive output is written to a temporary file in the destination directory and replaces the final destination only after successful creation.

An existing archive is not replaced unless overwrite is explicitly enabled.

## Important remaining risks

Smart Compressor does **not** currently enforce:

- maximum unpacked size;
- maximum member count;
- maximum compression ratio;
- CPU or memory quotas;
- filesystem quotas;
- transactional rollback after partial extraction;
- malware scanning.

A malicious archive can therefore still consume substantial disk space, CPU, memory, or time.

Use operating-system isolation and resource controls when processing untrusted archives in higher-risk environments.

## Reporting a vulnerability

Use GitHub's private security reporting features when available.

A useful report includes:

- affected commit/version;
- archive format;
- minimal reproduction steps;
- impact;
- known mitigation.

Do not publish exploit archives, sensitive files, credentials, or weaponized payloads in a public issue before a fix is prepared.

## Privacy

The application does not contain telemetry or a network client. It operates on local filesystem paths supplied by the user.

Archive contents themselves may still be confidential or sensitive.
