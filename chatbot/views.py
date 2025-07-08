import os
import json
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import google.generativeai as genai
from concurrent.futures import TimeoutError

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model with timeout settings
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={
        "max_output_tokens": 100,  # Limit response length
        "temperature": 0.7,
    }
)

def detect_emotion(text):
    """Detect emotional tone (simplified)"""
    text_lower = text.lower()
    if any(word in text_lower for word in ["sad", "upset", "cry", "hurt", "depressed", "lonely", "alone","bad day","bored","i hate myself","boredom","feel sad"]):
        return "sad"
    elif any(word in text_lower for word in ["happy", "joy", "yay", "excited", "celebrate", "party","became happy","happy morning"]):
        return "happy"
    elif any(word in text_lower for word in ["angry", "mad", "frustrated"]):
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
        if user_input in ['hi', 'hello', 'hi there', 'greet','vanakam','good morning','good evening','hii','hiii','hiiii','yo','say hi','good afternoon','Goodd morning','say hi','do hi','hi emote']:
            return JsonResponse({'reply': "[H] Hello there! 👋"})
        
        if user_input in ['dance', 'lets dance','dance karo','dance madu','dance emote','show some moves','i am happy','can u dance','dance now','dance bro']:
            return JsonResponse({'reply': "[C] Let's dance! 💃"})
        
        if user_input in ['jump','jumping','jump emote','can u jump','jump now','jump bro']:
            return JsonResponse({'reply': "[J] Jumping! 🤸"})
        
        if user_input in ['laugh', 'that\'s funny','i made a joke','laugh now','laughhh','laughh','laughhhh','lets laugh together','laugh with me ','can u laugh']:
            return JsonResponse({'reply': "[S] Haha! 😂"})
        
        if user_input in ['sleep', 'good night','go to sleep','sleep now','rest now','sleep with me','can u sleep']:
            return JsonResponse({'reply': "[L] Time to sleep! 😴"})
        
        # Then check for partial matches
        if any(word in user_input for word in ['hi', 'hello', 'hi there', 'greet','vanakam','good morning','good evening','hii','hiii','hiiii','yo','say hi','good afternoon','Goodd morning','say hi','do hi','hi emote']):
            return JsonResponse({'reply': "[H] Hi! How are you? 👋"})
            
        if any(word in user_input for word in ['dance', 'lets dance','dance karo','dance madu','dance emote','show some moves','i am happy','can u dance','dance now','dance bro']):
            return JsonResponse({'reply': "[C] I love dancing! 💃"})
            
        if any(word in user_input for word in ['jump','jumping','jump emote','can u jump','jump now','jump bro']):
            return JsonResponse({'reply': "[J] Wheee! 🤸"})
            
        if any(word in user_input for word in ['laugh', 'that\'s funny','i made a joke','laugh now','laughhh','laughh','laughhhh','lets laugh together','laugh with me ','can u laugh']):
            return JsonResponse({'reply': "[S] Hahaa! 😂"})
            
        if any(word in user_input for word in ['sleep', 'good night','go to sleep','sleep now','rest now','sleep with me','can u sleep']):
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
        
        # Default response with timeout protection
        try:
            response = model.generate_content(
                f"Respond warmly and friendly to this: {user_input}",
                request_options={"timeout": 5}  # 5 second timeout
            )
            return JsonResponse({'reply': f" {response.text}"})
        except TimeoutError:
            return JsonResponse({
                'reply': "[I] I'm thinking hard... please try again in a moment!",
                'error': "Response timeout"
            }, status=504)
        except Exception as api_error:
            return JsonResponse({
                'reply': "[I] Having trouble thinking right now...",
                'error': str(api_error)[:100]  # Truncate long errors
            }, status=503)

    except Exception as e:
        return JsonResponse({
            'reply': "[I] Oops! Something went wrong. Let's try again.",
            'error': str(e)[:100]  # Truncate error message
        }, status=500)
