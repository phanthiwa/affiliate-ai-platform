# คู่มือการรันและ Deploy ระบบ (ฉบับไม่มี Server ของตัวเอง)

---

## 💡 สรุปทางเลือก 3 รูปแบบ (ฟรี 100% ไม่ต้องเช่า Server)

### ทางเลือกที่ 1: รันบนคอมพิวเตอร์ตัวเองแบบ 1-Click (แนะนำที่สุด สะดวกและเร็วที่สุด)
คุณไม่จำเป็นต้องมี Server เลย สามารถรันบนโน้ตบุ๊กหรือคอมพิวเตอร์ของคุณเองได้โดยตรง:

1. เปิดโฟลเดอร์ `c:\Users\user\Downloads\affiliate-ai-platform\`
2. ดับเบิ้ลคลิกที่ไฟล์ **`start_app.bat`**
3. ระบบจะเปิดโปรแกรมและเปิดหน้าเว็บ **`http://localhost:3001`** ขึ้นมาใช้งานได้ทันที 100% ฟรี

---

### ทางเลือกที่ 2: Deploy ขึ้น Cloud ฟรี (Vercel + Render.com)

หากต้องการให้เปิดใช้งานได้จากทุกที่ (ผ่านมือถือ/แท็บเล็ต) โดยไม่ต้องเปิดคอมพิวเตอร์:

#### 1. Frontend (Next.js) -> Deploy ฟรีบน **Vercel**
- สมัครบัญชีฟรีที่ [Vercel.com](https://vercel.com)
- กด **"Add New Project"** เลือกโฟลเดอร์ `frontend` หรือเชื่อม GitHub Repo
- กำหนด Environment Variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1`
- กด **Deploy** (ได้ URL สวยๆ เช่น `https://my-affiliate-os.vercel.app` ฟรีตลอดชีพ)

#### 2. Backend (FastAPI) -> Deploy ฟรีบน **Render.com** หรือ **Railway**
- สมัครบัญชีฟรีที่ [Render.com](https://render.com)
- กด **"New Web Service"** เลือกโฟลเดอร์ `backend`
- ใส่คำสั่ง Build: `pip install -r requirements.txt`
- ใส่คำสั่ง Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- ได้ URL Backend ฟรีทันที

---

### ทางเลือกที่ 3: ใช้งานร่วมกับ Google Cloud Run / Google Flow (Google Ecosystem)

เนื่องจากคุณใช้ **Google Flow** อยู่แล้ว สามารถรัน Backend บน **Google Cloud Run (Free Tier)** ได้:
- Google Cloud ให้โควตาฟรี **2 ล้าน Requests ต่อเดือน** (สำหรับครีเอเตอร์ใช้งานคนเดียวไม่เสียเงินเลย)
- สามารถเชื่อมต่อ Webhook ตรงกับ Google Flow ได้แบบ Zero-latency
