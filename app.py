import re
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="RupeeRakshak AI",
    page_icon="🛡️",
    layout="centered"
)

# Application heading
st.title("🛡️ RupeeRakshak AI")
st.subheader("AI-Powered Financial Fraud Awareness")

st.write(
    "Analyze suspicious financial messages "
    "and understand their warning signs."
)

st.divider()

# Detection function
def analyze_message(message):

    text = message.lower()

    risk_score = 0
    warnings = []

    # Suspicious reward or prize claims
    reward_words = [
        "won", "winner", "prize",
        "lottery", "reward", "congratulations"
    ]

    if any(word in text for word in reward_words):
        risk_score += 20
        warnings.append(
            "Unexpected prize or reward claim detected."
        )

    # Urgency indicators
    urgency_words = [
        "urgent", "immediately", "hurry",
        "act now", "limited time"
    ]

    if any(word in text for word in urgency_words):
        risk_score += 20
        warnings.append(
            "Message creates urgency or pressure."
        )

    # Requests for sensitive information
    sensitive_words = [
        "otp", "password", "pin",
        "cvv", "bank details"
    ]

    if any(word in text for word in sensitive_words):
        risk_score += 30
        warnings.append(
            "Message requests sensitive financial information."
        )

    # Payment requests
    payment_words = [
        "pay", "payment", "transfer",
        "send money", "processing fee"
    ]

    if any(word in text for word in payment_words):
        risk_score += 20
        warnings.append(
            "A payment or money transfer request was detected."
        )

    # Suspicious link indicator
    urls = re.findall(
        r"https?://\S+|www\.\S+",
        text
    )

    if urls:
        risk_score += 20
        warnings.append(
            "Message contains a link. Verify it independently."
        )

    # Keep score within 0-100
    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        risk_level = "High Risk"
    elif risk_score >= 30:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return risk_score, risk_level, warnings


# User input
st.subheader("🔍 Scan a Financial Message")

message = st.text_area(
    "Paste your suspicious message here:",
    height=150,
    placeholder="Enter a message to analyze..."
)

# Analyze button
if st.button("Analyze Message", type="primary"):

    if not message.strip():

        st.warning("Please enter a message first.")

    else:

        score, level, warnings = analyze_message(message)

        st.divider()

        st.subheader("Analysis Results")

        st.metric("Risk Score", f"{score}/100")

        st.progress(score / 100)

        if level == "High Risk":
            st.error("🚨 High Risk")

        elif level == "Medium Risk":
            st.warning("⚠️ Medium Risk")

        else:
            st.success("✅ Low Risk")

        st.write("### Warning Indicators")

        if warnings:

            for warning in warnings:
                st.write("⚠️", warning)

        else:

            st.info(
                "No indicators from our current "
                "detection rules were identified."
            )

        st.caption(
            "This is a preliminary rule-based assessment, "
            "not a guarantee that a message is safe or fraudulent."
        )

        st.info(
            "Safety tip: Never share OTPs, passwords, "
            "PINs or CVVs with anyone."
        )

st.divider()

st.caption("RupeeRakshak AI | Arthaton 2026")