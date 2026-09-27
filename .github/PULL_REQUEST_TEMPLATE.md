## Summary

Describe the compression, inspection, extraction, or repository problem and the focused change that solves it.

## Validation

- [ ] <code>python -m compileall -q src tests</code>
- [ ] <code>python -m unittest discover -s tests -v</code>
- [ ] <code>smart-compressor --version</code>
- [ ] Tests were added or updated for behavior changes
- [ ] User-visible behavior is documented

## Archive safety

- [ ] Destination-boundary checks remain intact
- [ ] TAR link / special-member handling remains intentional
- [ ] Overwrite behavior remains explicit
- [ ] New archive-format claims match tested behavior
- [ ] No private archives, credentials, or large generated artifacts were committed

## Notes

Add compatibility, security, performance, or follow-up context here.
