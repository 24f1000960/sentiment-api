from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ✅ CORS - allows any website/tool to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all origins
    allow_credentials=True,
    allow_methods=["*"],       # allow GET, POST, etc.
    allow_headers=["*"],       # allow all headers
)

# --- Define what the incoming JSON looks like ---
class SentimentRequest(BaseModel):
    sentences: List[str]

# --- Define what one result looks like ---
class SentimentResult(BaseModel):
    sentence: str
    sentiment: str

# --- Define what the full response looks like ---
class SentimentResponse(BaseModel):
    results: List[SentimentResult]


# --- The actual sentiment logic (rule-based, no ML needed!) ---
def analyze_sentiment(text: str) -> str:
    text_lower = text.lower()

    happy_words = [
        "love", "great", "excellent", "amazing", "wonderful", "fantastic",
        "happy", "joy", "excited", "best", "awesome", "good", "beautiful",
        "brilliant", "superb", "perfect", "glad", "delighted", "thrilled",
        "pleasant", "enjoy", "fun", "nice", "like", "positive", "thank",
        "thanks", "win", "winning", "success", "celebrate", "yay", "hooray",
        "blessed", "grateful", "fabulous", "outstanding", "magnificent",
        "incredible", "extraordinary", "smile", "laugh", "cheerful"
    ]

    sad_words = [
        "hate", "terrible", "awful", "horrible", "bad", "sad", "unhappy",
        "depressed", "miserable", "angry", "upset", "disappointed", "worst",
        "failure", "fail", "boring", "disgusting", "frustrated", "anxious",
        "worried", "fear", "scared", "cry", "crying", "tears", "pain",
        "hurt", "broken", "lost", "alone", "lonely", "ugly", "stupid",
        "dumb", "useless", "hopeless", "disaster", "problem", "trouble",
        "sorry", "regret", "shame", "wrong", "miss", "dying", "dead",
        "sick", "tired", "exhausted", "nightmare", "poor", "suffer"
    ]

    # Count how many happy vs sad words appear
    happy_count = sum(1 for word in happy_words if word in text_lower)
    sad_count = sum(1 for word in sad_words if word in text_lower)

    if happy_count > sad_count:
        return "happy"
    elif sad_count > happy_count:
        return "sad"
    else:
        return "neutral"


# --- The POST endpoint ---
@app.post("/sentiment", response_model=SentimentResponse)
def get_sentiment(request: SentimentRequest):
    results = []
    for sentence in request.sentences:
        sentiment = analyze_sentiment(sentence)
        results.append(SentimentResult(sentence=sentence, sentiment=sentiment))
    return SentimentResponse(results=results)


# --- Health check (optional but useful) ---
@app.get("/")
def root():
    return {"status": "Sentiment API is running!"}