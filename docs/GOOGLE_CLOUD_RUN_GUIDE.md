# คู่มือการ Deploy บน Google Cloud Run (Free Tier) & เชื่อมต่อ Google Flow

---

## 🌟 ทำไมต้อง Google Cloud Run?
- **ฟรี 100% ภายใต้ Free Tier**: Google ให้โควตาฟรี **2 ล้าน Requests ต่อเดือน**, 360,000 วินาที vCPU และ 180,000 GiB-วินาที Memory
- **Scale to Zero ($0 เมื่อไม่ใช้งาน)**: เมื่อไม่มีการใช้งาน ตัวเซิร์ฟเวอร์จะดับเองอัตโนมัติ ไม่มีการกินเงิน
- **ได้ลิงก์ HTTPS ถาวร**: สามารถเปิดใช้งานจากมือถือ, iPad, หรือคอมพิวเตอร์เครื่องไหนก็ได้ในโลก

---

## 🚀 วิธีการ Deploy ขึ้น Google Cloud Run (เลือก 1 วิธีที่สะดวกที่สุด)

### วิธีที่ A: Deploy ผ่านหน้าเว็บเบราว์เซอร์ (Google Cloud Console / Cloud Shell)
*(สะดวกที่สุด ไม่ต้องลงโปรแกรมอะไรในคอมเลย)*

1. เข้าไปที่ [Google Cloud Console](https://console.cloud.google.com/) (ล็อกอินด้วยบัญชี Google ของคุณ)
2. คลิกปุ่ม **Cloud Shell** (ไอคอน `>_` ที่มุมขวาบนของหน้าเว็บ)
3. เมื่อหน้าต่าง Terminal ด้านล่างเปิดขึ้นมา ให้อัปโหลดโฟลเดอร์โปรเจกต์ หรือรันคำสั่ง:
   ```bash
   # 1. ไปที่โฟลเดอร์ Backend และสั่ง Deploy
   cd affiliate-ai-platform/backend
   gcloud run deploy affiliate-backend \
     --source . \
     --region asia-southeast1 \
     --min-instances 0 \
     --max-instances 2 \
     --memory 512Mi \
     --allow-unauthenticated
   ```
4. ระบบจะแสดง URL ของ Backend (เช่น `https://affiliate-backend-xxx.a.run.app`)
5. จากนั้นสั่ง Deploy Frontend:
   ```bash
   cd ../frontend
   gcloud run deploy affiliate-frontend \
     --source . \
     --region asia-southeast1 \
     --min-instances 0 \
     --max-instances 2 \
     --memory 512Mi \
     --set-env-vars NEXT_PUBLIC_API_URL=https://affiliate-backend-xxx.a.run.app/api/v1 \
     --allow-unauthenticated
   ```
6. คุณจะได้ URL ของ Frontend ทันที (เช่น `https://affiliate-frontend-xxx.a.run.app`) นำไปเปิดใช้งานได้ทุกที่!

---

### วิธีที่ B: Deploy ด้วย 1-Click บนคอมพิวเตอร์ (ถ้ามี `gcloud CLI`)

1. ติดตั้ง [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (หากยังไม่มี)
2. เปิด Terminal แล้วพิมพ์ `gcloud auth login` (ล็อกอินด้วยบัญชี Google)
3. ดับเบิ้ลคลิกที่ไฟล์ **`deploy_google_cloud_run.bat`** ในโฟลเดอร์โปรเจกต์
4. สคริปต์จะทำการสร้าง Docker Container, อัปโหลด, ตั้งค่า Free Tier และเปิดหน้าเว็บให้คุณโดยอัตโนมัติ!

---

## 🔗 วิธีการเชื่อมต่อกับ Google Flow

ผมได้สร้างไฟล์ Schema แม่แบบไว้ให้ที่:
[google_flow_template.json](file:///c:/Users/user/Downloads/affiliate-ai-platform/google_flow_template.json)

### ขั้นตอนใน Google Flow:
1. ในหน้า Workflow ของ Google Flow ให้สร้าง **Webhook Trigger Node**
2. เมื่อกดปุ่ม **"ส่งออก JSON สำหรับ Google Flow"** จากหน้า Dashboard ของคุณ จะได้ข้อมูล 15 คลิป
3. ข้อมูลในแต่ละคลิปจะมีโครงสร้างพร้อมใช้งาน:
   - `duration_sec`: ความยาววิดีโอ (15s, 20s, 30s)
   - `aspect_ratio`: "9:16"
   - `thai_voice_actor`: เสียงพากย์ภาษาไทย เช่น `th-TH-PremwadeeNeural`
   - `visual_prompts`: Prompt ภาษาอังกฤษแยกแต่ละช็อต (สำหรับป้อนเข้า Imagen 3 / Veo Node)
   - `burned_captions`: ข้อความซับไตเติลภาษาไทยพร้อมช่วงเวลา (Timing Cues)
   - `webhook_callback_url`: URL สำหรับส่งสถานะกลับมาที่ Cloud Run เมื่อเรนเดอร์เสร็จ
