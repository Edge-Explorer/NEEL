# NEEL: The Intelligent Life Coach & Productivity Strategist 🦾🧠

<p align="center">
  <img src="mobile/assets/images/icon.png" width="150" height="150" alt="NEEL Logo" style="border-radius: 30px;">
</p>

**NEEL** is a high-performance personal growth ecosystem powered by a Multi-Agent AI architecture. It transcends simple productivity tracking by acting as a sophisticated AI life coach that monitors your work patterns, calibrates your strategy, and provides high-level insights through a premium, glassmorphic interface.

---

## 🌐 Live Deployment
- **Backend API**: [https://neel-8ybz.onrender.com/docs](https://neel-8ybz.onrender.com/docs)
- **Status**: Live on Render (PostgreSQL)

---

## 🚀 Vision
NEEL stands for **Neural Evolution & Executive Logic**. It is designed for high-performers (Engineers, Researchers, Creators) who need a cognitive partner to optimize their deep-work patterns and long-term trajectory.

---

## 🏗️ Technical Architecture

### 1. **Intelligence Engine (Backend)**
- **Cloud Infrastructure**: Deployed on **Render** using FastAPI.
- **AI Orchestration**: LangChain + Google Gemini 1.5 Flash.
- **Multi-Agent Logic**: 
  - **Supervisor Agent**: Gates access to reasoning based on data sufficiency.
  - **Reasoning Agent**: The "Brain" that identifies trends and generates guidance.
  - **Reflection Agent**: An auditor that ensures response safety and tone quality.
- **Database**: PostgreSQL (Render Managed) for high-availability production storage.

### 2. **Mobile Experience (Frontend)**
- **Framework**: React Native (Expo SDK 54)
- **Build System**: EAS Build (Production Android APK)
- **UI/UX**: Premium Dark Mode, Glassmorphic components, and dynamic Linear Gradients.
- **Icons**: Custom Gemini-generated branding + Lucide-React-Native.

---

## ✨ Key Features

### 📊 **NEEL Pulse Dashboard**
A real-time command center showing your **Calibration Status**. It includes a dynamic **Activity Breakdown** that reveals exactly where your cognitive energy is being spent.

### 🧠 **Permanent Conversational Memory**
NEEL remembers your evolution. Your chat history is persisted in the cloud, allowing the AI to reference past goals and previous wins to provide context-aware coaching.

### 🪄 **Magic Auto-Logging**
Log work without filling out forms. Simply tell NEEL what you did, and the AI will automatically parse, categorize, and log the activity into your profile.

---

## �️ Local Development

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Configure `.env` with your `Google_Gemini_Api_Key`.
4. `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

### Mobile
1. `cd mobile`
2. `npm install`
3. Point `API_BASE_URL` in `services/api.js` to your local IP or the live Render URL.
4. `npx expo start`

---

## 📜 Principles
- **Aesthetic First**: Any UI change must follow the glassmorphic design system.
- **24-Hour Rule**: Activity logs can be adjusted within 24 hours to maintain data integrity.
- **Agent Audit**: Every word the AI speaks is audited by the Reflection Agent before delivery.

---

**Developed with ❤️ by Karan.**
