# Architecture

Smart Compressor is a dependency-free Python compression toolkit built on the standard library.

## Core flow

~~~text
source file / directory
        |
        v
format inferred from output suffix
        |
        v
compression engine
  ├─ ZIP / Deflate
  ├─ TAR + gzip
  ├─ TAR + bzip2
  ├─ TAR + xz
  ├─ gzip stream
  ├─ bzip2 stream
  └─ xz stream
        |
        v
temporary archive file
        |
        v
atomic replace
        |
        v
inspect_archive()
members · packed bytes · unpacked bytes · ratio
~~~

Extraction follows a separate safety path:

~~~text
archive
  |
  v
member enumeration
  |
  +--> resolve target path inside destination
  |
  +--> reject traversal outside destination
  |
  +--> TAR: reject links / devices / special members
  |
  +--> protect existing files unless overwrite is explicit
  |
  v
stream member content to destination
~~~

## Components

### <code>src/smart_compressor/core.py</code>

Implements:

- format detection from file suffixes;
- recursive file discovery for directory compression;
- atomic destination creation through a temporary file;
- archive compression;
- archive inspection;
- safe extraction.

### <code>src/smart_compressor/cli.py</code>

Provides three commands:

| Command | Purpose |
|---|---|
| <code>compress</code> | Create a supported archive |
| <code>inspect</code> | Read archive statistics without extracting |
| <code>extract</code> | Safely extract supported archives |

JSON output is available for automation where implemented by the CLI.

### <code>src/smart_compressor/__init__.py</code>

Exports the small public Python API:

- <code>compress</code>
- <code>extract</code>
- <code>inspect_archive</code>
- <code>CompressionError</code>

## Supported formats

### Directory compression

- <code>.zip</code>
- <code>.tar.gz</code> / <code>.tgz</code>
- <code>.tar.bz2</code> / <code>.tbz2</code>
- <code>.tar.xz</code> / <code>.txz</code>

### Single-file stream compression

- <code>.gz</code>
- <code>.bz2</code>
- <code>.xz</code>

Single-stream formats accept files only.

## Write behavior

Archive creation is atomic at the destination level:

1. create a temporary file in the destination directory;
2. write the archive there;
3. replace the final destination only after successful creation.

Existing outputs are rejected unless <code>overwrite=True</code> or <code>--overwrite</code> is explicit.

## Extraction safety

The implementation resolves every member target against the destination root and rejects paths that escape it.

For TAR archives, symbolic links, hard links, devices, and other special members are rejected. Only regular files and directories are accepted.

This provides path-traversal protection, but it does **not** impose resource quotas against compression bombs.

## Inspection

<code>inspect_archive()</code> returns:

- archive path;
- detected format;
- member count;
- packed bytes;
- unpacked bytes;
- packed/unpacked ratio.

For <code>.gz</code>, <code>.bz2</code>, and <code>.xz</code>, calculating the unpacked size requires reading the decompressed stream.

## Boundaries

The current project does not provide:

- RAR;
- 7z;
- Zstandard;
- password-protected or encrypted archives;
- multipart archives;
- GUI;
- resource quotas for compression bombs;
- transactional rollback of already-extracted files.

These are not current features and should not be documented as implemented.
