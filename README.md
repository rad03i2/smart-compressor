# Smart Compressor

A safe, dependency-free local compression toolkit for files and directories, built with Python's standard library.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · GitHub: @rad03i2

## English

### Overview

Smart Compressor provides one predictable CLI and Python API for creating, inspecting, and safely extracting common archives. It exists for users and scripts that need useful compression without cloud uploads, native binaries, or third-party runtime packages.

### Features

- Compress files or directories to ZIP.
- Compress directories to `.tar.gz`, `.tar.bz2`, or `.tar.xz`.
- Compress individual files to `.gz`, `.bz2`, or `.xz`.
- Safely extract every supported format.
- Inspect member count, packed size, unpacked size, and compression ratio without extraction.
- Compression levels `0-9` where supported.
- JSON output for automation.
- Refuses accidental overwrite by default.
- Atomic archive creation: writes a temporary file before replacing the destination.
- Zip Slip / path-traversal protection during extraction.
- Rejects TAR symlinks, hard links, devices, and special members.
- No telemetry, network access, API keys, or runtime dependencies.

### Requirements

- Python 3.10 or newer.
- No external compression programs are required.

### Installation

From a clone:

```bash
git clone https://github.com/rad03i2/smart-compressor.git
cd smart-compressor
python -m pip install -e .
```

### Usage

```bash
# ZIP a directory
smart-compressor compress ./photos ./photos.zip

# High-compression XZ TAR archive
smart-compressor compress ./project ./project.tar.xz --level 9

# Compress one file
smart-compressor compress report.csv report.csv.gz --level 9

# Inspect without extracting
smart-compressor inspect ./photos.zip
smart-compressor inspect ./photos.zip --json

# Safe extraction
smart-compressor extract ./photos.zip ./restored

# Explicitly permit replacing existing outputs
smart-compressor extract ./photos.zip ./restored --overwrite
```

The output format is inferred from the destination extension. Supported archive suffixes are `.zip`, `.tar.gz`/`.tgz`, `.tar.bz2`/`.tbz2`, `.tar.xz`/`.txz`, `.gz`, `.bz2`, and `.xz`. Single-stream `.gz`, `.bz2`, and `.xz` accept files only.

### Python API

```python
from smart_compressor import compress, extract, inspect_archive

info = compress("documents", "documents.zip", level=6)
print(info.to_dict())
extract("documents.zip", "restored")
```

### Configuration

There is intentionally no configuration file or `.env` file. Behavior is explicit through CLI flags or Python function arguments. `--overwrite` is always opt-in.

### Project structure

```text
src/smart_compressor/
  __init__.py       Public API and metadata
  core.py           Compression, inspection, safe extraction
  cli.py            Command-line interface
tests/test_core.py  Functional and security regression tests
.github/workflows/ci.yml  Cross-platform CI
```

### Testing

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
smart-compressor --version
```

CI runs the same validation across Python 3.10, 3.12, and 3.13 on Linux, Windows, and macOS.

### Preview / screenshots

This is a CLI-first project, so screenshots are optional. For a portfolio preview, show `smart-compressor inspect archive.zip` beside a successful `compress` command rather than a fabricated GUI.

### Security and privacy

All processing is local. Archive member paths are resolved and verified to remain inside the requested extraction directory. TAR links and special entries are rejected. Existing files are protected unless overwrite is explicitly enabled. Unknown archives can still be compression bombs and consume large amounts of CPU, memory, or disk; this tool does not impose resource quotas.

### Limitations

- No RAR, 7z, Zstandard, encrypted archives, or password support.
- No GUI.
- No split/multipart archives.
- Compression-bomb resource limits are not enforced.
- Extraction is fail-fast, not transactional: files extracted before a later error are not rolled back.
- ZIP uses Deflate from Python's standard library rather than format-specific image/video recompression.

### Optional roadmap

Potential future work includes streaming progress callbacks, explicit resource limits, and an optional desktop UI. These are not current features.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security guidance is in [SECURITY.md](SECURITY.md).

### License

MIT — see [LICENSE](LICENSE).

### Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة

**Smart Compressor** أداة محلية وآمنة لضغط الملفات والمجلدات وفحص الأرشيفات وفكها من خلال واجهة أوامر واحدة وواجهة Python بسيطة. صُممت لمن يحتاج ضغطًا عمليًا دون رفع الملفات إلى السحابة أو تثبيت برامج ضغط خارجية أو حزم تشغيل إضافية.

### المميزات

- ضغط الملفات أو المجلدات بصيغة ZIP.
- ضغط المجلدات بصيغ `.tar.gz` و`.tar.bz2` و`.tar.xz`.
- ضغط الملف المفرد بصيغ `.gz` و`.bz2` و`.xz`.
- فك آمن لجميع الصيغ المدعومة.
- فحص الأرشيف دون فكّه وعرض عدد العناصر والحجم المضغوط وغير المضغوط ونسبة الضغط.
- مستويات ضغط من `0` إلى `9` حيث تدعم الصيغة ذلك.
- إخراج JSON للاستخدام في الأتمتة والسكربتات.
- منع الاستبدال غير المقصود افتراضيًا.
- إنشاء الأرشيف عبر ملف مؤقت ثم اعتماده لتقليل خطر ترك ناتج ناقص.
- حماية من هجمات Zip Slip ومسارات `../` عند فك الضغط.
- رفض الروابط الرمزية والصلبة والأجهزة والعناصر الخاصة داخل TAR.
- لا Telemetry ولا اتصال شبكي ولا مفاتيح API ولا اعتماديات تشغيل خارجية.

### المتطلبات

Python 3.10 أو أحدث فقط. لا تحتاج إلى 7-Zip أو أدوات ضغط خارجية.

### التثبيت

```bash
git clone https://github.com/rad03i2/smart-compressor.git
cd smart-compressor
python -m pip install -e .
```

### أمثلة الاستخدام

```bash
smart-compressor compress ./photos ./photos.zip
smart-compressor compress ./project ./project.tar.xz --level 9
smart-compressor compress report.csv report.csv.gz --level 9
smart-compressor inspect ./photos.zip
smart-compressor inspect ./photos.zip --json
smart-compressor extract ./photos.zip ./restored
```

يتم تحديد صيغة الضغط من امتداد ملف الإخراج. الاستبدال لا يحدث تلقائيًا؛ استخدم `--overwrite` فقط عندما تريد ذلك صراحةً.

### الإعداد

لا يوجد ملف إعدادات أو `.env` لأن المشروع لا يحتاج أسرارًا أو خدمات خارجية. جميع الخيارات واضحة في سطر الأوامر أو معاملات واجهة Python.

### بنية المشروع

المحرك موجود في `src/smart_compressor/core.py`، وواجهة الأوامر في `cli.py`، والاختبارات الوظيفية والأمنية في `tests/test_core.py`، وCI في `.github/workflows/ci.yml`.

### الاختبارات

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
smart-compressor --version
```

تغطي الاختبارات دورة الضغط والفك لـZIP وGZIP وTAR.XZ، وحماية الاستبدال، والتحقق من المستوى، ومحاولة Zip Slip. ويُشغّل CI الاختبارات على Linux وWindows وmacOS مع عدة إصدارات Python.

### المعاينة والصور

المشروع موجّه لسطر الأوامر، لذلك لا يحتاج إلى صور واجهة. عند عرضه في Portfolio يُفضّل تصوير أمر `inspect` وأمر ضغط ناجح بدل إضافة واجهة رسومية غير موجودة.

### الأمان والخصوصية

كل المعالجة محلية. يتم التأكد من أن كل مسار مستخرج يبقى داخل مجلد الوجهة، وتُرفض العناصر الخاصة والروابط في TAR. مع ذلك، قد تستهلك الأرشيفات الخبيثة من نوع compression bomb موارد كبيرة؛ المشروع لا يفرض حاليًا حدودًا على الموارد.

### القيود

- لا يدعم RAR أو 7z أو Zstandard أو الأرشيفات المشفرة وكلمات المرور.
- لا توجد واجهة رسومية.
- لا يدعم الأرشيفات المجزأة متعددة الأجزاء.
- لا يفرض حدودًا تلقائية ضد compression bombs.
- فك الضغط fail-fast وليس معاملة قابلة للتراجع؛ الملفات التي فُكت قبل خطأ لاحق لا تُحذف تلقائيًا.
- لا يعيد ضغط محتوى الصور أو الفيديو بترميزات خاصة؛ ZIP يستخدم Deflate القياسي.

### تطوير اختياري مستقبلًا

يمكن مستقبلًا إضافة عرض تقدم streaming وحدود موارد صريحة وواجهة سطح مكتب اختيارية. هذه ليست ميزات حالية.

### المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md)، وإرشادات الأمان في [SECURITY.md](SECURITY.md).

### الترخيص

MIT — راجع [LICENSE](LICENSE).

### المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
