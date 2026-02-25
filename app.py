from flask import Flask, request, jsonify, render_template_string
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import IsolationForest
import time

app = Flask(__name__)

# 1. INITIALIZE DUMMY MODELS (For live deployment, load your .pkl models here)
# We use the Hybrid Architecture recommended for real-time <3ms latency
xgb_model = xgb.XGBClassifier(scale_pos_weight=97)
iso_forest = IsolationForest(contamination=0.01)

# 2. THE FRONTEND PAYMENT GATEWAY (HTML/JS)
# This serves the "Separate Page" where users input card details
checkout_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Payment Gateway</title>
    <style>
        body { font-family: Arial; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .payment-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); width: 350px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box;}
        button { width: 100%; padding: 10px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px;}
        button:hover { background: #218838; }
        #status { margin-top: 15px; font-weight: bold; text-align: center; }
    </style>
</head>
<body>

<div class="payment-box">
    <h2>Complete Your Purchase</h2>
    <p>Item: <strong>Running Shoes</strong> | Total: <strong>$120.00</strong></p>
    
    <label>Card Number</label>
    <input type="text" id="cardNumber" placeholder="0000 0000 0000 0000" maxlength="16">
    
    <label>CVV</label>
    <input type="password" id="cvv" placeholder="123" maxlength="3">
    
    <button onclick="processPayment()">Pay Now</button>
    <div id="status"></div>
</div>

<script>
    // BEHAVIORAL BIOMETRICS: Track how fast the user types [Source: 278]
    let keystrokes = 0;
    let startTime = null;

    document.getElementById('cardNumber').addEventListener('keydown', function() {
        if (keystrokes === 0) startTime = new Date().getTime();
        keystrokes++;
    });

    async function processPayment() {
        document.getElementById('status').innerText = "Processing in lightning speed...";
        document.getElementById('status').style.color = "blue";
        
        // Calculate typing speed (milliseconds per keystroke)
        let typingSpeed = 0;
        if (keystrokes > 0 && startTime) {
            let endTime = new Date().getTime();
            typingSpeed = (endTime - startTime) / keystrokes;
        }

        // Gather Payload (Transaction + Behavioral + Device Data)
        const payload = {
            amount: 120.00,
            card_length: document.getElementById('cardNumber').value.length,
            typing_speed_ms: typingSpeed,
            device_os: navigator.platform, // Basic device fingerprinting [Source: 279]
            time_of_day: new Date().getHours()
        };

        // Send to AI Backend
        const response = await fetch('/api/pay', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        
        // Display AI Decision
        let statusDiv = document.getElementById('status');
        if (result.decision === 'APPROVED') {
            statusDiv.innerText = "✅ Payment Approved!";
            statusDiv.style.color = "green";
        } else if (result.decision === 'FLAGGED') {
            statusDiv.innerText = "⚠️ OTP Required (Suspicious Activity)";
            statusDiv.style.color = "orange";
        } else {
            statusDiv.innerText = "❌ Payment Blocked (Fraud Detected)";
            statusDiv.style.color = "red";
        }
        
        console.log("AI Rationale:", result.explanation);
    }
</script>

</body>
</html>
"""

@app.route('/')
def checkout():
    return render_template_string(checkout_page)

# 3. THE LIGHTNING-SPEED AI DECISION ENGINE [Source: 318, 319]
@app.route('/api/pay', methods=['POST'])
def process_payment():
    start_time = time.time()
    data = request.json
    
    # Extract features sent from the web frontend
    amount = data.get('amount', 0)
    typing_speed = data.get('typing_speed_ms', 0)
    
    # ---------------------------------------------------------
    # HYBRID AI LOGIC (Simulated for this demo) [Source: 321]
    # ---------------------------------------------------------
    
    # 1. Rule-Based Check (PCI-DSS/Basic checks)
    if data.get('card_length') < 16:
        return jsonify({"decision": "BLOCKED", "explanation": "Invalid Card Length"})

    # 2. Behavioral Biometrics Check [Source: 252, 278]
    # Fraudsters using copy-paste or bots have a typing speed near 0ms
    # Normal humans type between 100ms and 400ms per key
    is_bot = typing_speed < 20 
    
    # 3. Supervised Model Score (Known Fraud Patterns)
    supervised_risk = 0.95 if amount > 5000 else 0.10
    
    # 4. Unsupervised Anomaly Score (Zero-Day/Novel Fraud)
    unsupervised_risk = 0.85 if is_bot else 0.05
    
    # 5. Ensemble Voting
    hybrid_risk_score = (supervised_risk * 0.6) + (unsupervised_risk * 0.4)
    
    # 6. Decision Thresholds [Source: 258]
    if hybrid_risk_score > 0.80:
        decision = "BLOCKED"
    elif 0.50 <= hybrid_risk_score <= 0.80:
        decision = "FLAGGED" # Triggers Step-Up Authentication (OTP)
    else:
        decision = "APPROVED"

    processing_time_ms = (time.time() - start_time) * 1000

    return jsonify({
        "decision": decision,
        "risk_score": float(hybrid_risk_score),
        "latency_ms": round(processing_time_ms, 2),
        "explanation": f"Typing speed was {typing_speed:.2f}ms. Bot suspected: {is_bot}."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
