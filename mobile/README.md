# NEEL Mobile: The Glassmorphic Command Center 📱✨

The NEEL Mobile app is a premium React Native application built with **Expo**. It provides a high-fidelity interface for interacting with your AI Life Coach and visualizing your productivity metrics.

## 🎨 Design Philosophy
- **Glassmorphism**: Using `LinearGradient` and semi-transparent surfaces to create depth.
- **Dark Mode Excellence**: A curated #050505 to #0F172A base palette with vibrant primary (`#8B5CF6`) and secondary (`#06B6D4`) accents.
- **Micro-Animations**: Smooth transitions and loading states (Thinking indicators) for an "alive" feel.

## 📁 Key Directories
- `/app`: Expo Router file-based system.
  - `(tabs)`: The core experience (Dashboard & Intelligence).
  - `log-activity.tsx`: Interactive logging screen.
  - `edit-activity.tsx`: Secure 24-hour log management.
  - `set-goals.tsx`: Strategy calibration interface.
- `/components`: Reusable UI modules based on the atomic Design System.
- `/constants/Theme.ts`: The source of truth for colors, spacing, and typography.
- `/services/api.js`: Axios-based API client with smart interceptors for error handling.

## 🚀 Key Patterns
- **Permanent History**: The Intelligence chat fetches its full history from the backend on load, ensuring a seamless experience.
- **Smart Dashboard**: The "Intelligence Feed" automatically truncates to 3 items and allows for "Expand All/Show Less" interaction.
- **Calibration Tracking**: Detailed visual bars show progress toward the 120-minute/7-day "Deep Intelligence" threshold.

## 🛠️ Commands
- `npm start`: Launch Expo developer tools.
- `npx expo run:android`: Build and run on Android emulator/device.
- `npx expo run:ios`: Build and run on iOS simulator/device.

---
**NEEL Mobile v1.0.8**
**Developed by Karan**
