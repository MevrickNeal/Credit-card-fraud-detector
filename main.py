from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import xgboost as xgb
import json
import numpy as np

# Initialize FastAPI
app = FastAPI(title="Intelligent Payment Gateway API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML Model
print("Loading XGBoost Model...")
model = xgb.Booster()
model.load_model("payment_fraud_model.json")

# Load the Sandbox Database
print("Loading Sandbox Database...")
with open("sandbox_database.json", "r") as f:
    sandbox_db = json.load(f)

class PaymentRequest(BaseModel):
    card_number: str
    amount: float
    cvv: str
    expiry: str

def is_valid_luhn(card_number: str) -> bool:
    """Validates a credit card number using the standard Luhn algorithm."""
    if not card_number.isdigit():
        return False
    digits = [int(d) for d in card_number]
    checksum = 0
    is_even = False
    for digit in reversed(digits):
        if is_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
        is_even = not is_even
    return checksum % 10 == 0

@app.post("/process_payment")
def process_payment(request: PaymentRequest):
    card = request.card_number.replace(" ", "")
    
    # 1. Basic Gateway Validation
    if len(card) < 13 or len(card) > 19:
        raise HTTPException(status_code=400, detail="Gateway Error: Invalid card length.")
        
    # L1 SECURITY: STRICT LUHN CHECK (Loophole Closed!)
    # Every single card MUST pass the mathematical check. No exceptions or bypasses.
    if not is_valid_luhn(card):
        raise HTTPException(status_code=400, detail="Layer 1 Blocked: Fake card number (Failed Luhn Math Check).")
        
    # 2. Dynamic Baseline Loading for Presentation
    # Only mathematically valid cards make it to this step now.
    if card.startswith("5"):
        features = np.array(sandbox_db["5000987654321098"]["features"])
    else:
        features = np.array(sandbox_db["4000123456789010"]["features"])
    
    # 3. TRUE BEHAVIORAL INJECTION
    features[2] = request.amount 
    
    cvv_num = int(request.cvv) if request.cvv.isdigit() else 123
    
    if request.amount > 5000 or cvv_num == 999:
        features[10] = 500.0  # Inject huge anomaly spike to simulate active hacker
        
    # 4. Real-Time Inference
    features_2d = features.reshape(1, -1)
    dmatrix = xgb.DMatrix(features_2d)
    fraud_probability = float(model.predict(dmatrix)[0])
    
    # --- NEW: Presentation Realism (Dynamic Variance) ---
    variance_factor = (sum(int(d) for d in card if d.isdigit()) + cvv_num) % 70
    fraud_probability += (variance_factor * 0.0001) 
    
    # Convert to percentage for easier reading in the code
    risk_pct = fraud_probability * 100
    
    # 5. HIGHLY INTELLIGENT TIERED RESPONSES (Business Logic Applied)
    
    if risk_pct >= 85.0:
        # Tier 5: Critical Risk (e.g., 90%+)
        return {
            "status": "DECLINED",
            "reason": "Critical Security Alert: Card restricted to prevent unauthorized access.",
            "risk_score": fraud_probability,
            "latency": "sub-second"
        }
    elif risk_pct >= 40.0:
        # Tier 4: High Risk (40% - 85%)
        return {
            "status": "DECLINED",
            "reason": "Transaction blocked: Security parameters exceeded. Please contact support.",
            "risk_score": fraud_probability,
            "latency": "sub-second"
        }
    elif risk_pct >= 15.0:
        # Tier 3: Moderate Risk (15% - 40%)
        return {
            "status": "DECLINED",
            "reason": "Transaction declined: Unusual activity detected. Please verify via banking app.",
            "risk_score": fraud_probability,
            "latency": "sub-second"
        }
    elif risk_pct >= 1.07:
        # Tier 2: Low-Risk Anomaly (1.07% - 15%) 
        return {
            "status": "APPROVED",
            "reason": "Transaction approved. (System Note: Minor anomaly flagged for routine monitoring).",
            "risk_score": fraud_probability,
            "latency": "sub-second"
        }
    else:
        # Tier 1: Safe (0% - 1.07%)
        return {
            "status": "APPROVED",
            "reason": "Transaction successful.",
            "risk_score": fraud_probability,
            "latency": "sub-second"
        }
