# Contributing

Thanks for helping improve Smart Compressor.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e .`.
3. Keep the core dependency-free unless a dependency has a strong, documented justification.
4. Add or update tests for behavioral changes.
5. Run `python -m compileall -q src tests` and `python -m unittest discover -s tests -v`.
6. Keep archive extraction secure: never bypass path validation or silently overwrite files.
7. Update the English and Arabic README sections when user-visible behavior changes.

Small, reviewable pull requests are preferred. Never commit credentials, private archives, generated build output, or personal data.
