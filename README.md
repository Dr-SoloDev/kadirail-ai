# 🚂 KadiRail AI

> **แผนที่นำทางคดีความสำหรับคนไทย**  
> Legal Case Navigation Tool with Responsible AI  
> Inspired by Responsible AI Innovation Hackathon 2026 (ศาลยุติธรรม × ETDA × AWS)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-ff4b4b.svg)](https://streamlit.io/)

### 🎯 ลดเวลาเข้าใจคดี: 120 นาที → 5 นาที (96% faster)

เปลี่ยนกระบวนการยุติธรรมไทยที่ซับซ้อนให้กลายเป็น "แผนที่รถไฟ" ที่คนธรรมดาเข้าใจได้ทันที

---

## 💭 Impact Vision

**มันไม่สำคัญว่าเรามาทำอะไรกันที่นี่ แต่มันสำคัญกว่าว่าเราจะทิ้งอะไรไว้**

KadiRail AI ถูกสร้างมาเพื่อเป็น "แผนที่นำทาง" ที่ช่วยให้คนธรรมดา — โดยเฉพาะคนที่ไม่มีเงินจ้างทนาย — **กล้าเริ่มต้นกระบวนการยุติธรรมได้ง่ายขึ้น**

> ถ้าคุณ fork ไปใช้ แค่ช่วยให้คนไทยคนหนึ่งเข้าใจคดีตัวเองเร็วขึ้น 5 นาที — สำหรับผม นั่นคือความสำเร็จที่ใหญ่ที่สุดแล้ว

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **Document Scanner** | LINE OCR สำหรับเอกสารกฎหมายไทย - highlight จุดเสี่ยง |
| 🗺️ **Case Map Engine** | แปลงขั้นตอนคดีเป็นแผนที่ interactive ด้วย Mermaid.js - ลาก branch ได้ |
| 🔮 **WhatIf Simulator** | จำลองทางเลือกต่างๆ พร้อม % โอกาสสำเร็จ + เวลา + ต้นทุน |
| ⚖️ **Bias Engine** | ตรวจจับ bias ในข้อความกฎหมาย (แยก train มีทนาย vs ไม่มีทนาย) |
| 🔒 **PII Masking** | ปิดบังข้อมูลส่วนบุคคลอัตโนมัติ |
| 📚 **Case Law Search** | ค้นหาคำพิพากษาที่เกี่ยวข้อง |
| 📝 **Document Summarizer** | สรุปเอกสารยาวๆ ให้เข้าใจง่าย |

### Supported Case Types (MVP)

| ประเภทคดี | English |
|-----------|---------|
| โกงค่าจ้าง | Wage Theft |
| ถูกเลิกจ้างไม่เป็นธรรม | Unfair Termination |
| ไม่จ่ายโบนัส | Bonus Dispute |

---

## ⚡ Quick Start (3 ขั้นตอน)

```bash
# Clone repo
git clone https://github.com/Dr-SoloDev/kadirail-ai.git
cd kadirail-ai

# สร้าง virtual environment (แนะนำ uv หรือ venv)
uv venv && source .venv/bin/activate
# หรือ python -m venv venv && source venv/bin/activate

# ติดตั้ง dependencies
uv pip install -r requirements.txt
# หรือ pip install -r requirements.txt

# รันแอพ
streamlit run streamlit_app.py
# เปิดเบราว์เซอร์ที่ http://localhost:8501
```

### LINE OCR Setup (สำหรับ Document Scanner)

สร้างไฟล์ `.env` ใน root folder แล้วใส่:

```env
LINE_CHANNEL_ID=your_channel_id
LINE_CHANNEL_SECRET=your_channel_secret
LINE_ACCESS_TOKEN=your_access_token
```

---

## Live Demo

### 🚀 Deploy to Hugging Face Spaces (Free)

```bash
# วิธีที่ 1: ผ่าน Web (แนะนำ)
1. ไปที่ https://huggingface.co/spaces
2. Create new Space → เลือก Streamlit
3. เลือก GitHub repository: Dr-SoloDev/kadirail-ai
4. เลือก Branch: master
5. เลือก App file: streamlit_app.py
6. กด Create!

# วิธีที่ 2: ผ่าน CLI
pip install huggingface_hub
huggingface-cli space create Dr-SoloDev/kadirail-ai \
  --sdk streamlit \
  --emoji ⚖️
```

### 📺 Live Demo Link

<!-- แทนที่ด้วย URL จริงหลัง deploy -->
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%8F%97%20Hugging%20Face-KadiRail%20AI-blue)](https://huggingface.co/spaces/Dr-SoloDev/kadirail-ai)

### GIF แสดงการใช้งานหลัก (ตัวอย่าง placeholder – แทนด้วย GIF จริงของคุณ)

#### สร้างแผนที่คดีจากปัญหา
![Demo: Create Case Map](https://via.placeholder.com/800x450?text=Demo:+Create+Case+Map)
*(พิมพ์ "โดนโกงค่าจ้าง 8000" → แผนที่ Mermaid ขึ้นทันที + สถานีต่าง ๆ)*

#### What-If Simulator
![Demo: What-If Simulator](https://via.placeholder.com/800x450?text=Demo:+What-If+Simulator)
*(ลาก branch เปลี่ยนทางเลือก → % โอกาส + เวลาเปลี่ยนตามทันที)*

#### Document Scanner + Highlight
![Demo: Document Scanner](https://via.placeholder.com/800x450?text=Demo:+Document+Scanner)
*(อัพโหลดสัญญา → ไฮไลท์จุดเสี่ยงสีแดง + แทรกเข้าแผนที่)*

> **วิธีสร้าง GIF เองง่าย ๆ:**
> - ใช้ [Loom](https://www.loom.com/) (ฟรี) บันทึกหน้าจอขณะรัน Streamlit
> - หรือ [Peek](https://github.com/JohnWong/peek) (Linux) / [Kap](https://getkap.co/) (macOS)
> - แล้วอัพโหลดขึ้น [imgur.com](https://imgur.com/) หรือ GitHub Issues
> - แทนลิงก์ด้านบนด้วย URL จริง

---

## Project Structure

```
kadirail-ai/
├── app/                  # Streamlit application (9 หน้า)
│   └── main.py
├── core/                 # Logic หลัก
│   ├── scanner.py
│   ├── map_engine.py
│   ├── simulator.py
│   ├── bias_engine.py
│   └── document_validator.py
├── utils/                # Utilities
│   ├── thai_nlp.py
│   ├── pii_masking.py
│   ├── case_law_search.py
│   ├── document_summarizer.py
│   └── mermaid_gen.py
├── data/                 # Mock data
│   └── mock_generator.py # สร้าง mock case 10,000+ คดี
├── .env.example
├── agent.md
├── CONTRIBUTING.md
├── LICENSE               # MIT
├── README.md
├── requirements.txt
└── ruff.toml
```

---

## How to Contribute

โปรเจกต์นี้เปิดกว้าง 100% สำหรับทุกคนที่อยากช่วยพัฒนาต่อ  
ไม่ว่าจะเป็น:

- 🗣️ เพิ่ม dialect support (อีสาน/ใต้/เหนือ)
- 🎮 เพิ่ม gamification (badge, Justice Quest)
- ⚖️ ปรับปรุง bias engine ให้แม่นยำขึ้น
- 🔗 เพิ่ม integration กับราชกิจจาฯ หรือเว็บศาลจริง

**Workflow:**
```
Fork → Create branch → Commit → Open Pull Request
```

ทุก contribution จะช่วยให้ไอเดียนี้ไปถึงคนที่ต้องการมากขึ้น

ดูรายละเอียดเพิ่มเติมได้ที่ [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## License

MIT License – ดูรายละเอียดใน [LICENSE](./LICENSE)

---

ขอบคุณทุกคนที่สนใจและช่วยกันทำให้โลกนี้ดีขึ้นแม้เพียงเล็กน้อย 🚂⚖️
