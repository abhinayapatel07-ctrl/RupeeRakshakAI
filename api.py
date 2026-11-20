import re
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="RupeeRakshak AI API",
    description="Financial Fraud Detection Backend",
    version="1.0"
)

class MessageRequest(BaseModel):
    message: str


def analyze_message(message):

    text = message.lower()

    risk_score = 0
    warnings = []

    reward_words = [
        "won", "winner", "prize",
        "lottery", "reward", "congratulations"
    ]

    if any(word in text for word in reward_words):
        risk_score += 20
        warnings.append("Unexpected prize or reward claim detected.")

    urgency_words = [
        "urgent", "immediately", "hurry",
        "act now", "limited time"
    ]

    if any(word in text for word in urgency_words):
        risk_score += 20
        warnings.append("Message creates urgency or pressure.")

    sensitive_words = [
        "otp", "password", "pin",
        "cvv", "bank details"
    ]

    if any(word in text for word in sensitive_words):
        risk_score += 30
        warnings.append("Message requests sensitive financial information.")

    payment_words = [
        "pay", "payment", "transfer",
        "send money", "processing fee"
    ]

    if any(word in text for word in payment_words):
        risk_score += 20
        warnings.append("A payment or money transfer request was detected.")

    urls = re.findall(
        r"https?://\S+|www\.\S+",
        text
    )

    if urls:
        risk_score += 20
        warnings.append("Message contains a link. Verify it independently.")

    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        risk_level = "High Risk"
    elif risk_score >= 30:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return risk_score, risk_level, warnings


@app.get("/")
def home():
    return {
        "message": "RupeeRakshak AI API is running!",
        "status": "success"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
def analyze(request: MessageRequest):

    score, level, warnings = analyze_message(request.message)

    return {
        "risk_score": score,
        "risk_level": level,
        "warnings": warnings
    }