# 🚂 KadiRail AI

> **Legal Case Navigation Tool for Thailand**  
> Responsible AI Hackathon 2026 (ศาลยุติธรรม × ETDA × AWS)

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Mission

Reduce case understanding time from **120 minutes → 5 minutes** (-96%)

Transform complex Thai legal procedures into interactive "train station" maps that anyone can understand.

---

## 🌍 Live Demo

> **Try it now without installing!**  
> The app runs in DEMO mode by default with mock data.

[![Deploy to Streamlit Community Cloud](https://img.shields.io/badge/Streamlit-Community_Cloud-FF4B4B?style=for-the-badge&logo=streamlit)](https://share.streamlit.io/)

### Quick Demo (No Setup Required)
1. Open the demo link above
2. Click **"เข้าสู่ระบบ"** (login) — use any demo credentials:
   - Username: `demo` | Password: `demo123`
3. Try the 9 pages:
   - 🏠 Home — See the case map overview
   - 📄 Scan — Upload a document (or use sample)
   - 🗺️ Case Map — Drag the interactive timeline
   - 🔮 Predict — See outcome predictions
   - ⚖️ Bias — Check for hidden biases
   - ✅ Validate — Verify document integrity
   - 🔒 Privacy — Mask sensitive info
   - 📚 Search — Find relevant case laws
   - 📝 Summarize — Get quick summaries

---

## 🌱 Impact Vision

> *"ทิ้งอะไรไว้บนโลกใบนี้"*

โปรเจกต์นี้เกิดจากความเชื่อใจอย่างหนึ่ง:  
**มันไม่สำคัญว่าเรามาทำอะไรกันที่นี่ในโลกใบนี้**  
**แต่มันสำคัญกว่าว่าเราจะทิ้งอะไรไว้ที่นี่บนโลกใบนี้**

KadiRail AI ไม่ได้ถูกสร้างมาเพื่อชนะรางวัลหรือได้ชื่อเสียง  
แต่ถูกสร้างมาเพื่อเป็น "แผนที่นำทาง" เล็ก ๆ ที่ช่วยให้คนธรรมดา (โดยเฉพาะคนที่ไม่มีเงินจ้างทนาย)  
กล้าเริ่มต้นกระบวนการยุติธรรมได้ง่ายขึ้น แม้เพียงนิดเดียว

ถ้าคุณ fork repo นี้ไปต่อยอด หรือเอาไอเดียส่วนใดส่วนหนึ่งไปใช้  
ไม่ต้องให้เครดิตผมก็ได้เลยครับ  
แค่ช่วยให้คนไทยคนหนึ่งคนใดคนหนึ่ง เข้าใจคดีของตัวเองเร็วขึ้น 5 นาทีแทน 2 ชั่วโมง  
หรือลดความท้อแท้ลงได้สักนิด  
สำหรับผม นั่นคือความสำเร็จที่ใหญ่ที่สุดแล้ว

ขอให้ไอเดียนี้เดินทางไกลกว่าที่ผมเคยคิดไว้  
และขอให้โลกใบนี้ดีขึ้น แม้เพียงเล็กน้อย เพราะเราทุกคนช่วยกัน

ขอบคุณที่อ่านจนถึงตรงนี้ 🙏

### ทำไมถึง Open Source?

| เหตุผล | ผลกระทบ |
|--------|---------|
| **ความยุติธรรมไม่ควรเป็นสินค้าหรู** | ทุกคนเข้าถึงได้ฟรี |
| **AI ต้องโปร่งใส** | ดูโค้ดได้ ตรวจสอบได้ |
| **ความรู้ทางกฎหมายเป็นของสาธารณะ** | ไม่มีใครเป็นเจ้าของ |
| **Hackathon สร้าง ไม่ใช่จบ** | คนอื่นต่อยอดได้ |

### ใครได้ประโยชน์?

- 👷 **แรงงาน** — เข้าใจสิทธิ์ตัวเอง
- 👨‍⚖️ **ทนายความ** — เครื่องมือช่วยทำงาน
- 🏛️ **ศาล** — ลดคดีที่ไม่เข้าใจกระบวนการ
- 📚 **นักศึกษา** — เรียนรู้กฎหมายแรงงาน

---

## 📺 Live Demo & GIF Guide

ลองรันโปรเจกต์ดูได้เลยครับ (ใช้เวลาไม่ถึง 5 นาที)

### วิธีดู demo เร็ว ๆ

```bash
# 1. Clone repo
git clone https://github.com/Dr-SoloDev/kadirail-ai.git
cd kadirail-ai

# 2. ติดตั้ง dependencies
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 3. รัน Streamlit
streamlit run app/main.py
# → เปิด http://localhost:8501
```

### GIF แสดงการใช้งานหลัก

#### สร้างแผนที่รถไฟจากปัญหา
![Demo: Create Case Map](https://i.imgur.com/xxxxxx.gif)
*(พิมพ์ "โดนโกงค่าจ้าง 8000" → แผนที่ Mermaid ขึ้นทันที)*

#### What-If Simulator
![Demo: What-If Branching](https://i.imgur.com/yyyyyy.gif)
*(ลาก branch เปลี่ยนทางเลือก → % โอกาส + เวลาเปลี่ยนตาม)*

#### Document Scanner + Highlight
![Demo: AR Scanner](https://i.imgur.com/zzzzzz.gif)
*(อัพโหลดสัญญา → ไฮไลท์จุดเสี่ยงสีแดง)*

> **Note:** GIFs coming soon! PRs welcome 📸

---

## ✨ Features

### Core Features
| Feature | Description |
|---------|-------------|
| 📄 **Document Scanner** | LINE OCR API integration for Thai legal documents |
| 🗺️ **Case Map Engine** | Transform legal procedures into interactive Mermaid.js maps |
| 🔮 **WhatIf Simulator** | Predict case outcomes based on different choices |
| ⚖️ **Bias Engine** | Detect and correct bias in legal text |

### Challenge Modules
| Challenge | Module | Status |
|-----------|--------|---------|
| 2.1 | Document Validator | ✅ |
| 2.2 | Document Validation | ✅ |
| 3 | PII Masking | ✅ |
| 3 | Case Law Search | ✅ |
| 4 | Document Summarizer | ✅ |

---

## 📸 App Screenshots

| Page | Description |
|------|-------------|
| 🏠 **หน้าหลัก** | Hero section with case types overview |
| 📄 **สแกนเอกสาร** | LINE OCR integration + file upload |
| 🗺️ **แผนที่คดี** | Interactive Mermaid.js timeline with drag |
| 🔮 **ทำนายผล** | WhatIf simulator with outcome predictions |
| ⚖️ **ตรวจอคติ** | Bias detection dashboard |
| ✅ **ตรวจเอกสาร** | Document validation results |
| 🔒 **ปิดบังข้อมูล** | PII masking interface |
| 📚 **ค้นหาคำพิพากษา** | Case law search with filters |
| 📝 **สรุปเอกสาร** | AI-powered summarization |

> **Note:** Screenshots coming soon! PRs welcome 📸

---

## 📱 Supported Case Types (MVP)

| Type | Thai | Description |
|------|------|-------------|
| Wage Theft | โกงค่าจ้าง | Employer doesn't pay or pays incomplete |
| Unfair Termination | ถูกเลิกจ้าง | Unjust dismissal |
| Bonus Dispute | ไม่จ่ายโบนัส | Employer refuses to pay bonus |

---

## 🚀 Quick Start

```bash
# Clone or navigate to project
cd kadirail

# Create virtual environment
uv venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app/main.py
```

Open http://localhost:8501 in your browser.

---

## 📂 Project Structure

```
kadirail/
├── app/
│   └── main.py                 # Streamlit 9 pages
├── core/
│   ├── scanner.py              # LINE OCR integration
│   ├── map_engine.py          # Mermaid.js rendering
│   ├── simulator.py            # WhatIf simulation
│   ├── bias_engine.py         # Bias detection
│   └── document_validator.py   # Challenge 2.2
├── utils/
│   ├── thai_nlp.py            # Thai NLP utilities
│   ├── pii_masking.py         # Challenge 3 - Privacy
│   ├── case_law_search.py     # Challenge 3 - Search
│   ├── document_summarizer.py # Challenge 4
│   └── mermaid_gen.py
├── data/
│   └── mock_generator.py      # 10,000+ mock cases
├── agent.md                   # Agent specification
├── README.md                  # This file
└── requirements.txt
```

---

## 🖥️ App Pages

1. **🏠 หน้าหลัก** - Home
2. **📄 สแกนเอกสาร** - Document Scanner
3. **🗺️ แผนที่คดี** - Case Map
4. **🔮 ทำนายผล** - Outcome Prediction
5. **⚖️ ตรวจอคติ** - Bias Check
6. **✅ ตรวจเอกสาร** - Document Validation
7. **🔒 ปิดบังข้อมูลส่วนตัว** - PII Masking
8. **📚 ค้นหาคำพิพากษา** - Case Law Search
9. **📝 สรุปเอกสาร** - Document Summarizer

---

## 🔧 Configuration

### LINE OCR API (Optional - Demo Mode Works Without)

1. **Get LINE Credentials:**
   - Go to [LINE Developers Console](https://developers.line.biz/)
   - Create a Messaging API channel
   - Get `Channel ID`, `Channel Secret`, and `Access Token`

2. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

3. **Fill in your credentials in `.env`:**
   ```
   LINE_CHANNEL_ID=your_channel_id
   LINE_CHANNEL_SECRET=your_channel_secret
   LINE_ACCESS_TOKEN=your_access_token
   ```

> **Demo Mode:** The app works without LINE credentials using mock data. Set `DEMO_MODE=true` in `.env` to enable.

### Quick Start Without LINE OCR
```bash
# No API key needed for demo!
streamlit run app/main.py
```

---

## 📚 Thai Legal Domain Knowledge

### Key Terms
| Term | Meaning |
|------|---------|
| ค่าจ้าง (Wage) | Payment for work |
| ค่าชดเชย (Compensation) | Severance pay |
| ค่าล่วงเวลา (Overtime) | OT pay |
| การไล่ออก (Dismissal) | Termination |
| ศาลแรงงาน (Labor Court) | Labor disputes |

### Court Process Flow (Labor Case)
1. ยื่นฟ้อง (File Complaint)
2. ขานคำให้การ (Answer)
3. ไต่สวน (Hearing)
4. พิพากษา (Judgment)
5. อุทธรณ์/ฎีกา (Appeal)

---

## 🤖 AI/ML Integration

- **ThaiNLP** - Thai language processing
- **Transformers** - Legal text analysis
- **Mermaid.js** - Interactive visualization

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file.

---

## 👥 Team

**KadiRail AI Team**  
For Responsible AI Hackathon 2026

---

## 🙏 Acknowledgments

- ศาลยุติธรรม (Thailand Courts)
- ETDA (Electronic Transactions Development Agency)
- AWS Thailand
