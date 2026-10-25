import json
import time
from google import genai
from src.config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a network security analyst. Analyze this network flow and decide if it is normal or an attack.

Respond ONLY in this JSON format:
{
  "verdict": "NORMAL" or "ATTACK",
  "attack_type": "brief type if attack, else NONE",
  "confidence": 0.0 to 1.0,
  "reasoning": "2-3 sentences explaining which features drove your decision"
}"""

def query_llm(flow: dict, retries: int = 6) -> dict:
    """Send one flow to Gemini and parse the JSON response."""
    feature_lines = "\n".join([f"- {k}: {v:.2f}" if isinstance(v, float) else f"- {k}: {v}" 
                                for k, v in flow.items()])
    prompt = f"{SYSTEM_PROMPT}\n\nNetwork flow:\n{feature_lines}\n\nYour JSON analysis:"
    
    for attempt in range(retries):
        try:
            # We use the new SDK syntax here
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())
        except Exception as e:
            print(f"\nAttempt {attempt+1} failed: {str(e)[:100]}...") # Truncate long errors
            # Wait longer between retries: 5s, 10s, 20s, etc.
            time.sleep(5 * (2 ** attempt)) 
            
    return {"verdict": "ERROR", "attack_type": "NONE", "confidence": 0.0, "reasoning": "API failed after max retries"}