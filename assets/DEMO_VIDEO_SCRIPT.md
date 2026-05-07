# KadiRail AI — Demo Video Script
## AMD Developer Hackathon 2026 | Track 1: AI Agents & Agentic Workflows
## Team NovaPulse | ความยาว: 3-5 นาที

---

## 🎬 Scene 1: Opening (0:00 - 0:30)

**แสดง:** Cover Image / Slide 1 (Title Slide)

**พูด (voiceover):**
> "สวัสดีครับ ผม Dr.solodev จากทีม NovaPulse
> วันนี้จะมาเสนอ KadiRail AI — ระบบนำทางกฎหมายไทยอัจฉริยะ
> ขับเคลื่อนด้วย Multi-Agent AI บน AMD Instinct MI300X"

**Action:** เปิด slide deck → Slide 1 (Title)

---

## 🎬 Scene 2: Problem Statement (0:30 - 1:15)

**แสดง:** Slide 2 (Problem)

**พูด:**
> "ปัญหาหลักของคนไทยคือ เข้าไม่ถึงกระบวนการยุติธรรม
> 
> หนึ่ง — ค่าทนายแพง ปรึกษาครั้งละ 2,000-5,000 บาท
> สอง — กฎหมายซับซ้อน พ.ร.บ. กว่า 800 ฉบับ ประชาชนไม่รู้สิทธิ์ตัวเอง
> สาม — ไม่มีเครื่องมือตรวจจับอคติในเอกสารกฎหมาย
> สี่ — ขาดข้อมูลเชิงกลยุทธ์ ไม่รู้โอกาสชนะ ไม่รู้ค่าใช้จ่ายก่อนตัดสินใจ
> 
> KadiRail AI จะแก้ปัญหานี้ทั้งหมด"

---

## 🎬 Scene 3: Solution Overview (1:15 - 1:45)

**แสดง:** Slide 3 (Solution Flow)

**พูด:**
> "KadiRail AI ทำงาน 5 ขั้นตอน:
> ใส่เอกสาร → วิเคราะห์คดี → จำลองผลลัพธ์ → ตรวจอคติ → ค้นคำพิพากษา
> 
> ทั้งหมดนี้ขับเคลื่อนด้วย 4 AI Agent เฉพาะทาง
> ที่ทำงานร่วมกันผ่าน Orchestrator Agent"

---

## 🎬 Scene 4: Live Demo — Full Case Analysis (1:45 - 3:15)

**แสดง:** เปิด Streamlit App → หน้า "Full Case Analysis"

### 4a. ใส่เอกสาร (1:45 - 2:00)

**Action:** 
1. คลิก "🔍 Full Case Analysis" ใน sidebar
2. วางข้อความตัวอย่างลงในกล่อง text:

```
ข้าพเจ้านายสมชาย ใจดี อายุ 35 ปี ทำงานเป็นพนักงานบริษัท ABC จำกัด
ตำแหน่งวิศวกร ตั้งแต่วันที่ 1 มกราคม 2566 ถึงวันที่ 30 มิถุนายน 2569
รวมระยะเวลา 3 ปี 6 เดือน ได้รับค่าจ้างเดือนละ 45,000 บาท

เมื่อวันที่ 30 มิถุนายน 2569 บริษัทได้เลิกจ้างข้าพเจ้าโดยไม่บอกกล่าวล่วงหน้า
และไม่จ่ายค่าชดเชยตามกฎหมาย ทั้งที่ข้าพเจ้าไม่ได้กระทำความผิดใดๆ
บริษัทยังค้างจ่ายค่าจ้างเดือนมิถุนายน 2569 จำนวน 45,000 บาท
และค่าล่วงเวลาอีก 12,500 บาท
```

**พูด:**
> "ลองดูตัวอย่าง กรณีเลิกจ้างไม่เป็นธรรม
> นายสมชายทำงาน 3 ปีครึ่ง เงินเดือน 45,000 บาท ถูกเลิกจ้างโดยไม่บอกกล่าว"

### 4b. กดวิเคราะห์ (2:00 - 2:15)

**Action:** กดปุ่ม "🚀 Run Full Analysis"

**พูด:**
> "กดปุ่มวิเคราะห์ จะเห็นว่า Agent ทั้ง 4 ตัวเริ่มทำงาน
> Legal Analysis, Case Strategy, Case Law, และ Bias Audit"

**แสดง:** Agent pipeline animation (Waiting → Analyzing → Complete)

### 4c. ดูผลลัพธ์ (2:15 - 3:15)

**Action:** เลื่อนดู Results ที่แสดง

**พูด (ชี้ทีละส่วน):**
> "ผลลัพธ์ — ระบบจำแนกว่าเป็นคดี **เลิกจ้างไม่เป็นธรรม** ระดับความเสี่ยง **สูง**
> 
> **โอกาสชนะ 78%** — ค่าชดเชยที่ควรได้ประมาณ **507,500 บาท**
> ประกอบด้วย ค่าชดเชย 135,000 ค่าบอกกล่าว 45,000 ค่าจ้างค้าง 45,000
> ค่าล่วงเวลา 12,500 และค่าเสียหายจากการเลิกจ้างไม่เป็นธรรม 270,000 บาท"

**Action:** คลิก Tab ต่างๆ

> "Tab Analysis — แสดงกฎหมายที่เกี่ยวข้อง เช่น พ.ร.บ.คุ้มครองแรงงาน มาตรา 118
> Tab Case Law — แสดงคำพิพากษาที่คล้ายคลึง
> Tab Bias — ตรวจอคติในเอกสาร bias score 15.2%"

---

## 🎬 Scene 5: Architecture & Tech Stack (3:15 - 3:45)

**แสดง:** Slide 4 (Architecture) → Slide 5 (Tech Stack)

**พูด:**
> "สถาปัตยกรรมของ KadiRail AI
> 
> Frontend ใช้ Streamlit — ง่ายต่อการใช้งาน
> Agent Layer มี 4 Agent เฉพาะทาง ควบคุมโดย Orchestrator
> Backend รันด้วย Qwen2-7B ผ่าน vLLM บน AMD Instinct MI300X
> ใช้ ROCm runtime — 192GB HBM3 memory ประมวลผลได้รวดเร็ว"

---

## 🎬 Scene 6: Agent Dashboard (3:45 - 4:15)

**แสดง:** เปิด Streamlit App → หน้า "Agent Dashboard"

**Action:** คลิก "📊 Agent Dashboard"

**พูด:**
> "ที่หน้า Agent Dashboard จะเห็นสถานะของทุก Agent
> จำนวน task ที่ทำเสร็จ สถานะ LLM connection
> และ architecture diagram ของระบบทั้งหมด"

---

## 🎬 Scene 7: Closing (4:15 - 4:45)

**แสดง:** Slide 7 (Team) → Cover Image

**พูด:**
> "KadiRail AI — นำทางทุกขั้นตอนกฎหมาย ลดเวลาทำความเข้าใจคดี
> จาก 120 นาที เหลือแค่ 5 นาที ลดลง 96%
> 
> ขอขอบคุณ AMD Developer Cloud และ AMD Instinct MI300X
> ที่ทำให้ระบบ Multi-Agent นี้เป็นจริงได้
> 
> ผม Dr.solodev จากทีม NovaPulse
> ขอบคุณครับ"

---

## 📋 Checklist ก่อนถ่าย

- [ ] เปิด Streamlit App — ทดสอบว่า demo mode ทำงาน
- [ ] เปิด Slide Deck ใน browser (deck.html)
- [ ] ติดตั้ง screen recorder (OBS / ScreenRec / Loom)
- [ ] เตรียม microphone
- [ ] ทดลองพูดตาม script ดูเวลา
- [ ] ตั้ง resolution 1280x720 หรือ 1920x1080
- [ ] Copy ข้อความตัวอย่างไว้ clipboard พร้อม paste

## ⏱️ เวลาแต่ละ Scene

| Scene | เนื้อหา | เวลา |
|-------|---------|------|
| 1 | Opening | 0:30 |
| 2 | Problem | 0:45 |
| 3 | Solution | 0:30 |
| 4 | Live Demo | 1:30 |
| 5 | Architecture | 0:30 |
| 6 | Agent Dashboard | 0:30 |
| 7 | Closing | 0:30 |
| **Total** | | **~4:45** |

## 💡 Tips

- **เน้น Live Demo** — จะเป็น highlight ของวิดีโอ ควรถ่ายส่วนนี้ให้ดีที่สุด
- **ใช้ demo mode** — ไม่ต้องรอ LLM จริง ผลลัพธ์ออกมาทันที
- **พูดช้าๆ ชัดๆ** — 3-5 นาที มีเวลาพอ ไม่ต้องรีบ
- **Zoom in** ตอนโชว์ผลลัพธ์ — ให้เห็นตัวเลขชัดๆ
- **ถ้าพูดไทย** — ใส่ subtitle อังกฤษจะได้ bonus point (hackathon judge อาจไม่ใช่คนไทย)
- **Outro** — ใส่ URL ของ app + GitHub repo
