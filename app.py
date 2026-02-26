from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import xgboost as xgb
import json
import numpy as np

# Initialize FastAPI
app = FastAPI(title="Fraud Detection Gateway API")

# Allow your GitHub Pages frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your GitHub Pages URL later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML Model
print("Loading XGBoost Model...")
model = xgb.XGBClassifier()
model.load_model("payment_fraud_model.json")

# Load the Sandbox Database
print("Loading Sandbox Database...")
with open("sandbox_database.json", "r") as f:
    sandbox_db = json.load(f)

# Define the expected input from the web frontend
class PaymentRequest(BaseModel):
    card_number: str
    amount: float
    cvv: str
    expiry: str

@app.post("/process_payment")
def process_payment(request: PaymentRequest):
    # 1. Check if the card exists in our Sandbox Database
    if request.card_number not in sandbox_db:
        raise HTTPException(status_code=400, detail="Card declined: Unrecognized test card.")
    
    # 2. Retrieve the hidden 400+ features for this specific test card
    user_data = sandbox_db[request.card_number]
    features = np.array(user_data["features"])
    
    # 3. Dynamic Injection: Replace the old 'TransactionAmt' feature with the user's live input
    # In the Kaggle dataset, TransactionAmt is the 3rd column (index 2 after removing ID and isFraud)
    # We must format it as a 2D array for XGBoost
    features[2] = request.amount 
    features_2d = features.reshape(1, -1)
    
    # 4. Real-Time Inference
    # Get the probability of fraud (class 1)
    fraud_probability = model.predict_proba(features_2d)[0][1]
    
    # Apply the optimal threshold we calculated in Kaggle (0.0107)
    is_fraud = bool(fraud_probability >= 0.0107)
    
    # 5. Return the gateway response
    if is_fraud:
        return {
            "status": "DECLINED",
            "reason": "High risk of fraud detected.",
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

# --- To run this locally: ---
# uvicorn main:app --reload
