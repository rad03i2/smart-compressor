<div dir="rtl" align="right">

# Smart Compressor — الدليل العربي

[العودة إلى الصفحة الرئيسية](README.md)

## نظرة عامة

**Smart Compressor** أداة ضغط وأرشفة محلية مبنية ببايثون، وتستخدم مكتبة Python القياسية فقط أثناء التشغيل. يمكنها إنشاء الأرشيفات وفحصها وفك الصيغ المدعومة مع التحقق من سلامة مسارات الاستخراج.

المشروع مناسب للسكربتات والاستخدام المحلي عندما تريد واجهة واحدة واضحة من دون 7-Zip أو برامج ضغط خارجية أو رفع الملفات إلى خدمة سحابية.

## المتطلبات

- Python 3.10 أو أحدث.
- pip للتثبيت.
- لا تحتاج أداة ضغط خارجية.

## التثبيت

</div>

~~~bash
git clone https://github.com/rad03i2/smart-compressor.git
cd smart-compressor
python -m pip install -e .
smart-compressor --version
~~~

<div dir="rtl" align="right">

## بنية الأوامر

</div>

~~~text
smart-compressor compress SOURCE OUTPUT [--level 0-9] [--overwrite] [--json]
smart-compressor inspect ARCHIVE [--json]
smart-compressor extract ARCHIVE DESTINATION [--overwrite] [--json]
~~~

<div dir="rtl" align="right">

## إنشاء الأرشيفات

### ZIP لمجلد

</div>

~~~bash
smart-compressor compress ./documents ./documents.zip
~~~

<div dir="rtl" align="right">

### TAR مع gzip

</div>

~~~bash
smart-compressor compress ./documents ./documents.tar.gz
~~~

<div dir="rtl" align="right">

### TAR مع bzip2

</div>

~~~bash
smart-compressor compress ./documents ./documents.tar.bz2
~~~

<div dir="rtl" align="right">

### TAR مع xz

</div>

~~~bash
smart-compressor compress ./documents ./documents.tar.xz
~~~

<div dir="rtl" align="right">

كما يتعرف المشروع على الامتدادات المختصرة <code>.tgz</code> و<code>.tbz2</code> و<code>.txz</code>.

### ضغط ملف واحد

</div>

~~~bash
smart-compressor compress report.csv report.csv.gz --level 9
smart-compressor compress report.csv report.csv.bz2 --level 9
smart-compressor compress report.csv report.csv.xz --level 9
~~~

<div dir="rtl" align="right">

صيغ GZ وBZ2 وXZ المفردة تقبل ملفًا واحدًا وليست حاويات لمجلد كامل.

## مستوى الضغط

الخيار <code>--level</code> يقبل القيم من 0 إلى 9.

في التنفيذ الحالي تُمرر القيمة إلى ZIP وإلى ضغط الملفات المفردة GZ/BZ2/XZ. أما إنشاء TAR.GZ وTAR.BZ2 وTAR.XZ فيستخدم إعدادات الضغط الافتراضية التي يستعملها مسار <code>tarfile.open()</code> الحالي.

## فحص الأرشيف

</div>

~~~bash
smart-compressor inspect archive.zip
smart-compressor inspect archive.zip --json
~~~

<div dir="rtl" align="right">

تتضمن معلومات الفحص:

- مسار الأرشيف.
- الصيغة.
- عدد العناصر.
- الحجم المضغوط.
- الحجم غير المضغوط.
- النسبة بين الحجمين.

عند فحص GZ/BZ2/XZ يحتاج البرنامج إلى قراءة التدفق بعد فك الضغط لحساب الحجم غير المضغوط.

## فك الضغط الآمن

</div>

~~~bash
smart-compressor extract archive.zip ./restored
~~~

<div dir="rtl" align="right">

الملفات الموجودة محمية افتراضيًا. للسماح بالاستبدال بشكل صريح:

</div>

~~~bash
smart-compressor extract archive.zip ./restored --overwrite
~~~

<div dir="rtl" align="right">

## نموذج الأمان أثناء الاستخراج

كل عنصر داخل الأرشيف يُحوّل إلى مسار داخل مجلد الوجهة، ثم يتحقق البرنامج من أن المسار النهائي لا يخرج خارج هذا المجلد. بذلك تُرفض محاولات مثل <code>../</code> التي تستهدف الكتابة خارج الوجهة.

وبالنسبة إلى TAR يقبل التنفيذ الملفات العادية والمجلدات فقط، ويرفض:

- الروابط الرمزية.
- الروابط الصلبة.
- الأجهزة.
- العناصر الخاصة الأخرى.

لكن هذا لا يمنع كل مخاطر الأرشيفات. المشروع لا يفرض حاليًا حدودًا على استهلاك المعالج أو الذاكرة أو مساحة القرص ضد compression bombs.

## سلامة إنشاء الأرشيف

عند إنشاء أرشيف:

1. يتحقق المشروع من المصدر.
2. يتحقق من مسار الإخراج.
3. يرفض الاستبدال إذا كان الناتج موجودًا إلا عند طلبه صراحة.
4. ينشئ ملفًا مؤقتًا داخل مجلد الوجهة.
5. يكتب الأرشيف إلى الملف المؤقت.
6. يعتمد الناتج النهائي بعد نجاح الإنشاء.

كما يجب أن يختلف مسار المصدر عن مسار الناتج.

## واجهة Python

</div>

~~~python
from smart_compressor import compress, extract, inspect_archive

info = compress("documents", "documents.zip", level=6)
print(info.to_dict())

extract("documents.zip", "restored")

checked = inspect_archive("documents.zip")
print(checked.ratio)
~~~

<div dir="rtl" align="right">

## الاختبارات

</div>

~~~bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
smart-compressor --version
~~~

<div dir="rtl" align="right">

يشغّل GitHub Actions الفحوص نفسها على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

تغطي الاختبارات الحالية دورة ZIP، وضغط GZIP لملف، وTAR.XZ، وحماية الاستبدال، والمستوى غير الصحيح، ومحاولة Zip Slip.

## الخصوصية

لا يحتوي المشروع على Telemetry أو عميل شبكي أو إعداد لمفاتيح API. تتم العمليات على مسارات الملفات المحلية التي يحددها المستخدم.

هذا لا يعني أن كل أرشيف آمن؛ فقد يحتوي الأرشيف على بيانات خاصة أو يكون مصممًا لاستهلاك موارد كبيرة عند فحصه أو فكّه.

## الحدود الحالية

لا يدعم المشروع حاليًا:

- RAR.
- 7z.
- Zstandard.
- كلمات المرور أو التشفير.
- الأرشيفات متعددة الأجزاء.
- واجهة رسومية.
- التراجع التلقائي عن الملفات التي فُكت قبل وقوع خطأ لاحق.
- حدود الموارد ضد compression bombs.

كما أنه لا يعيد ترميز الصور أو الفيديو أو الصوت بطريقة خاصة؛ ضغط ZIP يستخدم Deflate القياسي على البيانات.

## البنية التقنية

راجع [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## المطور

**رضوان عبدالهادي**  
**Radwan Abd alhady Ahmed**  
GitHub: [@rad03i2](https://github.com/rad03i2)

## الترخيص

MIT — راجع [LICENSE](LICENSE).

</div>
