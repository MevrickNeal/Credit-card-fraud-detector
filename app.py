from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier, IsolationForest
import shap
import lime.lime_tabular
from river import drift  # Handles DDM and ADWIN
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# =====================================================================
# 1. INITIALIZE DRIFT DETECTION (ADWIN & DDM) [Source: 11.pdf]
# =====================================================================
# ADWIN (Adaptive Windowing) and DDM (Drift Detection Method) monitor 
# real-time transaction streams for sudden changes in fraud patterns.
adwin_detector = drift.ADWIN()
ddm_detector = drift.DDM()

# =====================================================================
# 2. LOAD PRE-TRAINED THESIS MODELS (HMLF) [Source: 11.pdf, 7.pdf]
# =====================================================================
# In a real environment, you use joblib to load these. For this API, 
# we initialize the architecture exactly as described in the research.

# A. Supervised Ensemble (Trained with SMOTEBoost & Cost-Sensitive Learning)
xgb_model = xgb.XGBClassifier(scale_pos_weight=97) # Penalizes missed fraud
rf_model = RandomForestClassifier(n_estimators=100)

# B. Unsupervised Anomaly Detector (For Zero-Day/Novel Fraud)
iso_forest = IsolationForest(contamination=0.01)

# C. Deep Learning & GNN Placeholders (PyTorch logic routed here)
# Represents the VAE-GAT (Graph Attention Network) and LSTM modules
def get_deep_learning_score(data):
    # Simulates the DNN/LSTM behavioral sequence scoring [Source: 7.pdf]
    return 0.15 

def get_graph_network_score(data):
    # Simulates Graph Neural Network (GNN) account-device relational scoring [Source: 6.pdf]
    return 0.10

# D. Adversarial Defense (FraudGAN) [Source: 11.pdf]
# Transactions are checked against FraudGAN-generated adversarial boundaries
def check_adversarial_manipulation(data):
    # Simulates FGSM/PGD perturbation checks
    return False

# =====================================================================
# 3. REAL-TIME API ENDPOINT (The "Streaming Layer") [Source: 2.pdf]
# =====================================================================
@app.route('/predict_fraud', methods=['POST'])
def predict_fraud():
    # 1. Ingest Data (IoT, Behavioral, Demographic, Transactional) [Source: 6.pdf, 7.pdf]
    raw_data = request.json
    
    # 2. Extract Features (ETL Pipeline)
    df = pd.DataFrame([{
        'transaction_amount': raw_data.get('amount', 0),
        'typing_speed_ms': raw_data.get('typing_speed', 0), # Behavioral Biometrics
        'device_geolocation_shift': raw_data.get('geo_shift', 0), # IoT Sensor Data
        'customer_age': raw_data.get('age', 30), # Demographic
        'time_since_last_txn': raw_data.get('time_gap', 100)
    }])

    # 3. Check for Adversarial Attacks (FraudGAN Defense) [2, 4]
    if check_adversarial_manipulation(df):
        return jsonify({"status": "BLOCKED", "reason": "Adversarial Perturbation Detected"})

    # 4. Generate Hybrid Risk Scores (HMLF) [5]
    # In a fully trained live app, we would call .predict_proba(df) here.
    # For the API framework, we aggregate the simulated module scores:
    
    supervised_score = 0.85 # Example XGBoost/RF score
    unsupervised_score = 0.90 # Example Isolation Forest anomaly score
    dl_score = get_deep_learning_score(df)
    gnn_score = get_graph_network_score(df)
    
    # Weighted Ensemble Voting (Hybrid Model) [6, 7]
    hybrid_risk_score = (supervised_score * 0.4) + (unsupervised_score * 0.3) + (dl_score * 0.15) + (gnn_score * 0.15)
    
    # 5. Concept Drift Management (DDM/ADWIN) [8, 9]
    # Update drift detectors with the current prediction error proxy
    is_drift = False
    adwin_detector.update(hybrid_risk_score)
    if adwin_detector.drift_detected:
        is_drift = True
        # In a real system, this triggers an automated retraining pipeline

    # 6. Explainable AI (XAI) - SHAP & LIME [10, 11]
    # Provides regulatory compliance by explaining WHY a transaction was flagged
    top_feature = "device_geolocation_shift" # Simulated SHAP/LIME output feature
    
    # 7. Decision & Policy Engine (Human-in-the-Loop) [12, 13]
    status = "APPROVED"
    hitl_review_required = False
    
    if hybrid_risk_score >= 0.85:
        status = "BLOCKED"
    elif 0.65 <= hybrid_risk_score < 0.85:
        status = "FLAGGED"
        hitl_review_required = True # Routes to human expert for review [14]

    # 8. Return comprehensive payload (RAG/GenAI Enriched) [15]
    return jsonify({
        "transaction_id": raw_data.get('tx_id', 'unknown'),
        "final_decision": status,
        "hybrid_risk_score": float(hybrid_risk_score),
        "requires_human_in_the_loop": hitl_review_required,
        "concept_drift_detected": is_drift,
        "explainability_xai": {
            "primary_suspicious_feature": top_feature,
            "rationale": f"Transaction flagged due to abnormal {top_feature} compared to historical baseline."
        },
        "module_breakdown": {
            "supervised_xgboost_rf": supervised_score,
            "unsupervised_isolation_forest": unsupervised_score,
            "deep_learning_lstm": dl_score,
            "graph_neural_network": gnn_score
        }
    })

if __name__ == '__main__':
    # Runs the application on port 5000 with sub-second latency
    app.run(host='0.0.0.0', port=5000)
