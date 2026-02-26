from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import xgboost as xgb
import json
import numpy as np

# Initialize FastAPI
app = FastAPI(title="Fraud Detection Gateway API")

# Allow the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML Model
print("Loading XGBoost Model...")
model = xgb.XGBClassifier()
model.load_model("payment_fraud_model.json")

# Load the Sandbox Database (We now use this purely as a structural baseline)
print("Loading Sandbox Database...")
with open("sandbox_database.json", "r") as f:
    sandbox_db = json.load(f)

# Define expected input
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
        raise HTTPException(status_code=400, detail="Card declined: Invalid card length.")
        
    # L1 SECURITY: Check if the card is mathematically a real credit card
    if not is_valid_luhn(card):
        raise HTTPException(status_code=400, detail="Card declined: Fake or invalid credit card number.")
        
    # 2. Load a structural baseline array
    # In a real production system, this queries a massive SQL database for the user's history.
    # For our prototype, we load a baseline 432-feature array to hold our dynamic injections.
    baseline_profile = "4000123456789010" 
    features = np.array(sandbox_db[baseline_profile]["features"])
    
    # 3. TRUE DYNAMIC INJECTION
    # We map the live web inputs directly into the mathematical features the AI expects.
    
    # Feature 2 is 'TransactionAmt' in the IEEE dataset
    features[2] = request.amount 
    
    # Feature 3 is 'card1' (Categorical BIN number)
    features[3] = int(card[:6]) % 10000 
    
    # Feature 4 is 'card2' 
    features[4] = int(card[-4:]) % 1000 
    
    # Simulate dynamic behavioral velocity features using the CVV
    cvv_num = int(request.cvv) if request.cvv.isdigit() else 123
    features[10] = cvv_num * 1.5 
    
    # Reshape the 1D array into a 2D array for XGBoost
    features_2d = features.reshape(1, -1)
    
    # 4. Real-Time Inference
    # The AI is now evaluating the unique combination of your random card + amount
    fraud_probability = model.predict_proba(features_2d)[0][1]
    
    # Apply the optimal threshold we calculated in Kaggle (0.0107)
    is_fraud = bool(fraud_probability >= 0.0107)
    
    # 5. Return response based entirely on the AI's math
    if is_fraud:
        return {
            "status": "DECLINED",
            "reason": "High risk of fraud detected by AI.",
            "risk_score": float(fraud_probability),
            "latency": "sub-second"
        }
    else:
        return {
            "status": "APPROVED",
            "reason": "Transaction successful.",
            "risk_score": float(fraud_probability),
            "latency": "sub-second"
        }
