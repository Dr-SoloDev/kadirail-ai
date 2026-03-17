# KadiRail AI Agent Specification

## Overview
**KadiRail AI** - Legal Case Navigation Tool for Thailand  
**Hackathon:** Responsible AI Hackathon 2026 (ศาลยุติธรรม × ETDA × AWS)  
**Goal:** Reduce case understanding time from 120 min → 5 min (-96%)

---

## Agent Capabilities

### Core Features
1. **Document Scanner** - LINE OCR API integration for Thai legal documents
2. **Case Map Engine** - Transform legal procedures into interactive Mermaid.js train station maps
3. **WhatIf Simulator** - Predict case outcomes based on different choices
4. **Bias Engine** - Detect and correct bias in legal text

### Challenge-Specific Modules

| Challenge | Module | Description |
|-----------|--------|-------------|
| 2.1 | Document Validator | Translate legal language → self-file capability |
| 2.2 | Document Validator | Check document completeness |
| 3 | PII Masking | Privacy protection for case data |
| 3 | Case Law Search | Search Thai court precedents |
| 4 | Document Summarizer | Summarize documents + draft reports |

---

## Technical Stack

- **Frontend:** Streamlit (Python)
- **NLP:** pythainlp, transformers
- **Visualization:** Mermaid.js, graphviz
- **Data:** Pandas, mock case generator (10,000+ cases)

---

## Supported Case Types (MVP)

| Type | Thai | Description |
|------|------|-------------|
| Wage Theft | โกงค่าจ้าง | Employer doesn't pay or pays incomplete |
| Unfair Termination | ถูกเลิกจ้าง | Unjust dismissal |
| Bonus Dispute | ไม่จ่ายโบนัส | Employer refuses to pay bonus |

---

## File Structure

```
kadirail/
├── app/main.py                 # Streamlit 9 pages
├── core/
│   ├── scanner.py              # LINE OCR
│   ├── map_engine.py           # Mermaid rendering
│   ├── simulator.py            # WhatIf simulation
│   ├── bias_engine.py         # Bias detection
│   └── document_validator.py  # Challenge 2.2
├── utils/
│   ├── thai_nlp.py            # Thai NLP utilities
│   ├── pii_masking.py        # Challenge 3
│   ├── case_law_search.py     # Challenge 3
│   ├── document_summarizer.py # Challenge 4
│   └── mermaid_gen.py
├── data/
│   └── mock_generator.py       # 10,000+ mock cases
└── requirements.txt
```

---

## Running the Agent

```bash
cd kadirail
uv venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

---

## API Integration Points

### LINE OCR API
- Endpoint: `https://api.line.me/v2/bot/message/reply`
- Used in: `core/scanner.py`

### (Future) Azure OpenAI
- For: Document summarization, legal translation
- Config: `utils/azure_config.py`

---

## Thai Legal Domain Knowledge

### Key Concepts
- **ค่าจ้าง (Wage):** Payment for work
- **ค่าชดเชย (Compensation):** Severance pay
- **ค่าล่วงเวลา (Overtime):** OT pay
- **การไล่ออก (Dismissal):** Termination
- **ศาลแรงงาน (Labor Court):** Labor disputes

### Court Process Flow (Labor Case)
1. ยื่นฟ้อง (File Complaint)
2. ขานคำให้การ (Answer)
3. ไต่สวน (Hearing)
4. พิพากษา (Judgment)
5. อุทธรณ์/ฎีกา (Appeal)

---

## Ethical Guidelines

1. **Privacy First** - Always mask PII before processing
2. **Bias Detection** - Check for gender, socioeconomic bias
3. **Transparency** - Show confidence scores for predictions
4. **Human Oversight** - Recommendations, not legal advice

---

## Contact

For Responsible AI Hackathon 2026  
Team: KadiRail AI  
