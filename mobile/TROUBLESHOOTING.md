# NEEL Mobile App - Troubleshooting Guide

## If you're seeing errors and can't access login/signup:

### Quick Fixes to Try:

1. **Clear Everything and Restart:**
   ```bash
   # Stop the Expo server (Ctrl+C)
   # Then run:
   npx expo start --clear
   ```

2. **Check Your Phone/Emulator:**
   - Make sure you're connected to the same WiFi network as your computer
   - If using Expo Go app, make sure it's updated to the latest version
   - Try shaking your device and selecting "Reload"

3. **Common Error Solutions:**

   **Error: "Unable to resolve module"**
   - Run: `npm install`
   - Then: `npx expo start --clear`

   **Error: "Element type is invalid"**
   - This usually means a component import is wrong
   - Check that all imports in login.tsx and signup.tsx are correct

   **Blank Screen:**
   - Check if the app is stuck on the splash screen
   - Try reloading the app (shake device → Reload)

   **"Network request failed" when trying to login:**
   - This is normal if the backend is sleeping on Render
   - Wait 50-60 seconds and try again

4. **Verify the App Structure:**
   - app/index.tsx ✓ (entry point)
   - app/login.tsx ✓ (login page)
   - app/signup.tsx ✓ (signup page)
   - app/_layout.tsx ✓ (root layout)
   - app/(tabs)/_layout.tsx ✓ (tabs layout)

## What Should Happen:

1. App opens → Shows loading spinner (purple)
2. Redirects to Login page automatically
3. You can tap "Create Account" to go to Signup
4. After login/signup, you go to the main app

## If Still Having Issues:

Please provide:
- Screenshot of terminal errors
- Screenshot of what you see on your phone
- Any error messages from the Expo Go app
