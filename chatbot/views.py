import os
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def detect_emotion(text):
    """Detect emotional tone (simplified)"""
    text_lower = text.lower()
    if any(word in text_lower for word in ["sad", "upset", "cry", "hurt", "depressed", "lonely", "alone"]):
        return "sad"
    elif any(word in text_lower for word in ["happy", "joy", "yay", "excited", "celebrate", "party"]):
        return "happy"
    elif any(word in text_lower for word in ["angry", "mad", "hate", "frustrated"]):
        return "angry"
    return "neutral"

@csrf_exempt
def chatbot_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are accepted.'}, status=405)

    try:
        data = json.loads(request.body)
        user_input = data.get('message', '').strip().lower()  # Convert to lowercase
        
        # First check for exact matches of commands
        if user_input in ['hi', 'hello', 'hi there', 'greet']:
            return JsonResponse({'reply': "[H] Hello there! 👋"})
        
        if user_input in ['dance', 'lets dance']:
            return JsonResponse({'reply': "[C] Let's dance! 💃"})
        
        if user_input in ['jump']:
            return JsonResponse({'reply': "[J] Jumping! 🤸"})
        
        if user_input in ['laugh', 'that\'s funny']:
            return JsonResponse({'reply': "[S] Haha! 😂"})
        
        if user_input in ['sleep', 'good night']:
            return JsonResponse({'reply': "[L] Time to sleep! 😴"})
        
        # Then check for partial matches
        if any(word in user_input for word in ['hi', 'hello', 'greet']):
            return JsonResponse({'reply': "[H] Hi! How are you? 👋"})
            
        if 'dance' in user_input:
            return JsonResponse({'reply': "[C] I love dancing! 💃"})
            
        if 'jump' in user_input:
            return JsonResponse({'reply': "[J] Wheee! 🤸"})
            
        if any(word in user_input for word in ['laugh', 'funny', 'haha']):
            return JsonResponse({'reply': "[S] That's hilarious! 😂"})
            
        if any(word in user_input for word in ['sleep', 'night', 'bed']):
            return JsonResponse({'reply': "[L] Sleep tight! 😴"})
        
        # Questions
        if "?" in user_input or any(word in user_input for word in ["what", "why", "how", "when", "who", "did you eat"]):
            if "did you eat" in user_input or "did u eat" in user_input:
                return JsonResponse({'reply': "[I] I just had some digital snacks! 🍕"})
            return JsonResponse({'reply': "[I] That's an interesting question! 🤔"})
        
        # Emotional responses
        emotion = detect_emotion(user_input)
        if emotion == "sad":
            return JsonResponse({'reply': "[I] I'm here for you 🫂"})
        elif emotion == "happy":
            return JsonResponse({'reply': "[I] That's wonderful! 😊"})
        elif emotion == "angry":
            return JsonResponse({'reply': "[I] That sounds frustrating 😠"})
        
        # Default response
        return JsonResponse({'reply': "[I] Tell me more! 😊"})

    except Exception as e:
        return JsonResponse({
            'reply': "[I] Oops! Something went wrong. Let's try again.",
            'error': str(e)
        }, status=500)