# NEEL: The Intelligent Life Coach & Productivity Strategist 🦾🧠

**NEEL** is a high-performance personal growth ecosystem powered by a Multi-Agent AI architecture. It transcends simple productivity tracking by acting as a sophisticated AI life coach that monitors your work patterns, calibrates your strategy, and provides high-level insights through a premium, glassmorphic interface.

![NEEL Header](https://source.unsplash.com/featured/?technology,abstract,dark)

## 🚀 Vision
NEEL stands for **Neural Evolution & Executive Logic**. It is designed for high-performers (Engineers, Researchers, Creators) who need a cognitive partner to optimize their deep-work patterns and long-term trajectory.

---

## 🏗️ Technical Architecture

The project is split into two primary components:

### 1. **Mobile Experience (Frontend)**
- **Framework**: React Native (Expo)
- **Navigation**: Expo Router (File-based routing)
- **Styling**: Vanilla CSS-in-JS with a core Design System (`constants/Theme.ts`)
- **UI/UX**: Premium Dark Mode, Glassmorphic components, Linear Gradients (`expo-linear-gradient`)
- **Icons**: Lucide-React-Native

### 2. **Intelligence Engine (Backend)**
- **Framework**: FastAPI (Python)
- **AI Orchestration**: LangChain + Google Gemini 2.0 Flash
- **Agentic Logic**: 
  - **Supervisor Agent**: Gates access to reasoning based on data sufficiency.
  - **Reasoning Agent**: The "Brain" that identifies trends and generates guidance.
  - **Reflection Agent**: An auditor that ensures response safety and tone quality.
- **Database**: SQLAlchemy ORM (PostgreSQL/SQLite)
- **Persistence**: Full chat history and activity tracking (Permanent Memory)

---

## ✨ Key Features

### 📊 **NEEL Pulse Dashboard**
A real-time command center showing your **Calibration Status**. It includes a dynamic **Activity Breakdown** (Visual Analytics) that reveals exactly where your cognitive energy is being spent.

### 🧠 **Permanent Conversational Memory**
NEEL remembers everything. Your chat history is persisted in the cloud, allowing the AI to reference past goals, previous wins, and ongoing struggles to provide context-aware coaching.

### 🪄 **Magic Auto-Logging**
Log work without filling out forms. Simply tell NEEL: *"I just finished a 2-hour coding session on the backend,"* and the AI will automatically parse, categorize, and log the activity into your profile.

### 🎯 **Strategy Calibration**
Set your **North Star** goal and define your focus areas. NEEL uses these as the primary directive for all coaching advice and performance audits.

### 🛡️ **Self-Healing Connectivity**
Built-in smart error handling and automated sync indicators ensure the connection between your mobile device and the backend is always transparent.

---

## 🛠️ Setup & Installation

### Backend
1. `cd backend`
2. `pip install -r requirements.txt`
3. Configure `.env` with your `Google_Gemini_Api_Key` and `SECRET_KEY`.
4. `python -m uvicorn main:app --reload`

### Mobile
1. `cd mobile`
2. `npm install`
3. Configure `services/api.js` with your backend URL.
4. `npx expo start`

---

## 📜 Development Guidelines
- **24-Hour Rule**: Activity logs can be edited or deleted within 24 hours to maintain data integrity.
- **Agent Audit**: All AI responses undergo a reflection phase to ensure they align with the user's primary goal.
- **Aesthetic First**: Any UI change must follow the glassmorphic design system.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed with ❤️ by Karan.**
