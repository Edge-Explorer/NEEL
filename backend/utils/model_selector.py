import os
from google import genai
from dotenv import load_dotenv

def get_best_flash_model():
    load_dotenv()
    api_key = os.getenv("Google_Gemini_Api_Key")
    try:
        client = genai.Client(api_key=api_key)
        models = client.models.list()
        # Prefer 2.0-flash, then 1.5-flash, then any flash
        flash_models = [m.name for m in models if "flash" in m.name.lower()]
        
        # Look for 2.0-flash
        for m in flash_models:
            if "2.0-flash" in m and "lite" not in m and "exp" not in m:
                return m.replace("models/", "")
        
        # Look for 1.5-flash
        for m in flash_models:
            if "1.5-flash" in m:
                return m.replace("models/", "")
                
        # Look for any stable flash
        for m in flash_models:
            if "lite" not in m and "exp" not in m:
                return m.replace("models/", "")
        
        if flash_models:
            return flash_models[0].replace("models/", "")
            
        return "gemini-1.5-flash" # Fallback
    except Exception:
        return "gemini-1.5-flash"

if __name__ == "__main__":
    print(get_best_flash_model())
