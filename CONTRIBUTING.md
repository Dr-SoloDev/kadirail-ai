# 🤝 ร่วมพัฒนา KadiRail AI

> ขอบคุณที่สนใจร่วมสร้างสิ่งที่ดีกว่าเดิมให้กับโลก  
> ทุก contribution ไม่ว่าเล็กหรือใหญ่ — มีความหมายเสมอ

---

## 📋 สารบัญ

- [ก่อนเริ่ม — ทำความเข้าใจโปรเจกต์](#-ก่อนเริ่ม--ทำความเข้าใจโปรเจกต์)
- [ประเภท Contribution ที่ต้องการ](#-ประเภท-contribution-ที่ต้องการ)
- [ตั้งค่า Development Environment](#-ตั้งค่า-development-environment)
- [โครงสร้างโค้ดและสิ่งที่แต่ละไฟล์ทำ](#-โครงสร้างโค้ดและสิ่งที่แต่ละไฟล์ทำ)
- [Workflow การส่ง Pull Request](#-workflow-การส่ง-pull-request)
- [มาตรฐานโค้ด](#-มาตรฐานโค้ด)
- [Responsible AI Guidelines](#-responsible-ai-guidelines---สำคัญมาก)
- [การรายงาน Bug](#-การรายงาน-bug)
- [การเสนอ Feature ใหม่](#-การเสนอ-feature-ใหม่)
- [Good First Issues สำหรับมือใหม่](#-good-first-issues-สำหรับมือใหม่)

---

## 🧭 ก่อนเริ่ม — ทำความเข้าใจโปรเจกต์

KadiRail AI มีเป้าหมายที่ชัดเจนและข้อจำกัดที่สำคัญ กรุณาอ่านก่อนเขียนโค้ดบรรทัดแรก

### สิ่งที่ KadiRail เป็น ✅

- แผนที่นำทางกระบวนการยุติธรรมสำหรับคนธรรมดา
- เครื่องมือช่วยตัดสินใจโดยใช้ข้อมูล
- ระบบที่โปร่งใส ตรวจสอบได้ และไม่เลือกปฏิบัติ

### สิ่งที่ KadiRail ไม่เป็น ❌

- ทนายความดิจิทัล
- ระบบที่ให้คำปรึกษากฎหมายโดยตรง
- เครื่องมือที่แทนที่ผู้เชี่ยวชาญด้านกฎหมาย

### หลักการหลัก 3 ข้อ

1. **Privacy First** — ไม่เก็บข้อมูลส่วนตัวเสมอ
2. **Bias Aware** — วัดและแสดง bias อย่างโปร่งใส อย่าซ่อน
3. **Human Oversight** — AI แนะนำ ไม่ตัดสิน

---

## 🎯 ประเภท Contribution ที่ต้องการ

### Priority สูง — ต้องการด่วน

| งาน | ทักษะที่ต้องการ | เวลาโดยประมาณ |
|-----|----------------|--------------|
| **Llama 3 Thai Fine-tune** สำหรับ legal domain | PyTorch, NLP, Thai language | 2–4 สัปดาห์ |
| **RAG pipeline** จากคำพิพากษาสาธารณะ | LangChain, ChromaDB, Python | 1–2 สัปดาห์ |
| **Dialect NLP** อีสาน/ใต้/เหนือ | NLP, ความรู้ภาษาถิ่น | 1–3 สัปดาห์ |
| **แก้บัก critical** ที่มีอยู่ | Python, Streamlit | 1–3 วัน |

### Priority กลาง

| งาน | ทักษะที่ต้องการ | เวลาโดยประมาณ |
|-----|----------------|--------------|
| **Test coverage** เพิ่มจาก 40% → 80% | pytest, Python | 3–7 วัน |
| **Mobile UI** responsive redesign | CSS, Streamlit | 1 สัปดาห์ |
| **LINE OCR** integration จริง | LINE API, Python | 3–5 วัน |
| **เพิ่มคดีใหม่** (ผู้บริโภค, เช่าบ้าน) | Python, ความรู้กฎหมายเบื้องต้น | 3–7 วัน |

### Priority ต่ำ — Good First Issue

| งาน | ทักษะที่ต้องการ | เวลาโดยประมาณ |
|-----|----------------|--------------|
| แก้ typo / ปรับ copy ภาษาไทย | ไม่ต้องเขียนโค้ด | 30 นาที |
| เพิ่มคำพิพากษาใน `case_law_search.py` | Python เบื้องต้น | 1–2 ชั่วโมง |
| เพิ่ม risk pattern ใน `scanner.py` | Python เบื้องต้น | 1–2 ชั่วโมง |
| ขียน docstring ที่ขาดหายไป | Python เบื้องต้น | 2–4 ชั่วโมง |
| แปล README เป็นภาษาอังกฤษ | ภาษาอังกฤษ | 2–3 ชั่วโมง |

---

## ⚙️ ตั้งค่า Development Environment

### 1. Fork & Clone

```bash
# Fork ก่อนจาก GitHub UI แล้วค่อย clone fork ของคุณ
git clone https://github.com/YOUR_USERNAME/kadirail-ai.git
cd kadirail-ai

# เพิ่ม upstream เพื่อ sync กับ main repo
git remote add upstream https://github.com/Dr-SoloDev/kadirail-ai.git
```

### 2. ตั้งค่า Environment

```bash
# สร้าง virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

# ติดตั้ง dependencies ทั้งหมด รวม dev tools
pip install -r requirements.txt

# ติดตั้ง dev dependencies
pip install pytest pytest-cov ruff bandit
```

### 3. ตรวจสอบว่าทุกอย่างทำงาน

```bash
# รัน tests
pytest -v

# รัน app
streamlit run app/main.py

# ตรวจสอบ code style
ruff check . --fix
```

ถ้าเห็น `http://localhost:8501` เปิดได้ — พร้อมแล้วครับ 🎉

---

## 📁 โครงสร้างโค้ดและสิ่งที่แต่ละไฟล์ทำ

```
kadirail/
│
├── app/main.py
│   └── Router หลัก + UI ทุกหน้า
│
├── core/
│   ├── map_engine.py        ← Logic สร้างแผนที่ station
│   ├── simulator.py         ← What-If calculation
│   ├── bias_engine.py       ← Responsible AI layer ← ระวังมาก
│   ├── scanner.py           ← OCR + risk detection
│   └── document_validator.py ← ตรวจเอกสาร
│
├── utils/
│   ├── thai_nlp.py          ← แปลง text → case data
│   ├── pii_masking.py       ← Privacy protection ← ระวังมาก
│   ├── case_law_search.py   ← ฐานข้อมูลคำพิพากษา
│   ├── document_summarizer.py ← สรุปเอกสาร
│   ├── mermaid_gen.py
│   └── auth.py
│
└── data/
    └── mock_generator.py   ← สร้าง test data
```

---

## 🔄 Workflow การส่ง Pull Request

### ขั้นตอนมาตรฐาน

```bash
# 1. Sync กับ upstream ก่อนเสมอ
git fetch upstream
git checkout main
git merge upstream/main

# 2. สร้าง branch ใหม่
git checkout -b feature/your-feature-name

# 3. เขียนโค้ด + เขียน test
# ... ทำงาน ...

# 4. รัน tests ก่อน commit
pytest -v
ruff check . --fix

# 5. Commit ด้วย message ที่ชัดเจน
git add .
git commit -m "feat: คำอธิบายสั้นๆ"

# 6. Push และเปิด PR
git push origin feature/your-feature-name
```

### Commit Message Format

```
type: คำอธิบายสั้นๆ

ประเภท (type):
  feat     - feature ใหม่
  fix      - แก้บัก
  docs     - แก้เอกสาร
  test     - เพิ่ม/แก้ test
  refactor - ปรับโค้ดโดยไม่เปลี่ยน behavior
  chore    - งานทั่วไป
  ci       - GitHub Actions, CI/CD
```

### PR Template

เมื่อเปิด PR กรุณาตอบคำถามเหล่านี้:

```markdown
## สิ่งที่เปลี่ยน
<!-- อธิบายสั้นๆ ว่าทำอะไร -->

## เหตุผล
<!-- ทำไมถึงต้องเปลี่ยน -->

## ทดสอบอย่างไร
<!-- บอกวิธีที่คุณทดสอบ -->

## Responsible AI Check
- [ ] ไม่เก็บหรือ log ข้อมูลส่วนตัวใหม่
- [ ] ไม่เพิ่ม bias ใหม่โดยไม่จำเป็น
- [ ] มี disclaimer หากเพิ่ม legal recommendation

## Screenshots (ถ้ามี UI เปลี่ยน)
```

---

## 📐 มาตรฐานโค้ด

### Python Style

```python
# ✅ ดี — ชัดเจน, มี type hints, มี docstring
def detect_trauma(text: str) -> bool:
    """
    ตรวจจับสัญญาณ emotional distress ในข้อความ
    
    Args:
        text: ข้อความภาษาไทยจากผู้ใช้
        
    Returns:
        True ถ้าพบคำที่บ่งบอก distress
    """
    TRAUMA_KEYWORDS = ["กลัว", "เครียด", "สิ้นหวัง", "ถูกหลอก"]
    return any(kw in text for kw in TRAUMA_KEYWORDS)


# ❌ ไม่ดี — ไม่มี type, ไม่มี docstring
def check(t):
    words = ["กลัว", "เครียด"]
    for w in words:
        if w in t:
            return True
    return False
```

### ข้อกำหนดที่ต้องทำ

- ใช้ **type hints** ทุก function
- เขียน **docstring** ทุก public function
- เขียน **unit test** สำหรับ logic ใหม่ทุกชิ้น
- ตั้งชื่อ variable/function เป็น **ภาษาอังกฤษ**
- แต่ละไฟล์ไม่ควรยาวเกิน **400 บรรทัด**

### ข้อห้าม

```python
# ❌ ห้าม hardcode path
open("/home/username/kadirail/data/file.json")

# ✅ ใช้ pathlib
from pathlib import Path
DATA_DIR = Path(__file__).parent
open(DATA_DIR / "file.json")

# ❌ ห้าม log ข้อมูลคดีแบบ raw
print(f"User filed case: {case_data}")

# ✅ log เฉพาะ metadata
print(f"Case created: type={case_data['case_type']}")
```

---

## 🛡️ Responsible AI Guidelines — สำคัญมาก

ส่วนนี้สำคัญที่สุด **กรุณาอ่านก่อนแก้ไข `bias_engine.py` หรือ `pii_masking.py`**

### หลักการ Bias

```python
# เมื่อเพิ่ม legal recommendation ใหม่:

# ✅ ต้องทำ
# 1. ระบุว่าข้อมูลมาจากกลุ่มไหน
data_label = "คดีไม่มีทนาย 3,241 คดี (2563–2566)"

# 2. แสดง confidence ที่ต่ำเมื่อข้อมูลน้อย
if sample_size < 100:
    confidence = "ต่ำ — ข้อมูลน้อย"
```

### หลักการ Privacy

```python
# ❌ ห้ามเด็ดขาด
def log_case(case_data):
    with open("cases.log", "a") as f:
        f.write(json.dumps(case_data))

# ✅ ถ้าต้องการ analytics ใช้ aggregate เท่านั้น
def log_aggregate(case_type: str, province: str):
    analytics_db.increment(f"{case_type}:{province}")
```

---

## 🐛 การรายงาน Bug

### ก่อนรายงาน

1. ตรวจสอบว่ายังไม่มีใครรายงานไว้ใน [Issues](https://github.com/Dr-SoloDev/kadirail-ai/issues)
2. ลองรัน `pip install -r requirements.txt` ใหม่
3. ตรวจสอบว่าใช้ Python 3.10+

### วิธีรายงาน

เปิด Issue และใส่ข้อมูลเหล่านี้:

```markdown
**บัคที่พบ:**
[อธิบายว่าเกิดอะไร]

**ขั้นตอนที่ทำให้เกิดบัค:**
1. เปิดหน้า...
2. กด...
3. พิมพ์...

**ผลที่คาดหวัง:**
[ควรจะเกิดอะไร]

**ผลที่เกิดจริง:**
[เกิดอะไรแทน]

**Environment:**
- OS: [เช่น macOS 14, Ubuntu 22.04]
- Python: [เช่น 3.11.4]
```

---

## 💡 การเสนอ Feature ใหม่

### ก่อนเสนอ

- Feature นั้นช่วยให้คนเข้าถึงความยุติธรรมได้ดีขึ้นไหม?
- มันไม่ทำให้ระบบ bias ขึ้นหรือ privacy แย่ลงใช่ไหม?
- มันทำได้จริงใน scope ของโปรเจกต์นี้ไหม?
