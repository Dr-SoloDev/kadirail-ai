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

### LINE OCR API
Set your LINE credentials in `.env`:
```
LINE_CHANNEL_ID=your_channel_id
LINE_CHANNEL_SECRET=your_channel_secret
LINE_ACCESS_TOKEN=your_access_token
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
