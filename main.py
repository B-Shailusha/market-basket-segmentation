from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Customer Segmentation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scaler = joblib.load("scaler.pkl")
kmeans = joblib.load("kmeans_model.pkl")

SEGMENT_INFO = {
    0: {
        "name": "Premium In-Store Loyalists",
        "emoji": "🏆",
        "color": "#FFD700",
        "description": "High-income, high-spending customers who prefer in-store shopping. Top candidates for loyalty programs and premium product offers.",
        "strategy": "Offer exclusive in-store events, loyalty rewards, and personalized premium recommendations.",
    },
    1: {
        "name": "Budget-Conscious Browsers",
        "emoji": "🔍",
        "color": "#87CEEB",
        "description": "Lower-income customers who visit the website frequently but purchase little. High web engagement without conversion.",
        "strategy": "Target with cart-abandonment emails, flash sales, and entry-level product bundles.",
    },
    2: {
        "name": "Omnichannel Mid-Spenders",
        "emoji": "🛒",
        "color": "#90EE90",
        "description": "Mid-income customers who actively shop both online and in-store with moderate spending.",
        "strategy": "Leverage click-and-collect promotions and cross-channel loyalty points.",
    },
    3: {
        "name": "High-Value Digital Shoppers",
        "emoji": "💻",
        "color": "#DDA0DD",
        "description": "High-income customers who prefer web purchases. Strong spenders with good store engagement too.",
        "strategy": "Personalized online recommendations, early access to new products, premium web experience.",
    },
    4: {
        "name": "Affluent Occasional Buyers",
        "emoji": "💎",
        "color": "#FFA07A",
        "description": "High income and high spending but infrequent — high recency days. May be drifting away.",
        "strategy": "Win-back campaigns, exclusive seasonal offers, personalized re-engagement emails.",
    },
    5: {
        "name": "Low-Engagement At-Risk",
        "emoji": "⚠️",
        "color": "#F08080",
        "description": "Low-income, low-spending customers with high recency. At risk of churning from the brand.",
        "strategy": "Re-engagement discounts, surveys to understand needs, low-cost entry offers.",
    },
}


class CustomerInput(BaseModel):
    income: float
    total_spending: float
    num_web_purchases: float
    num_store_purchases: float
    num_web_visits_month: float
    recency: float


@app.get("/")
def root():
    return {"message": "Customer Segmentation API is running", "clusters": 6}


@app.post("/predict")
def predict(customer: CustomerInput):
    features = np.array([[
        customer.income,
        customer.total_spending,
        customer.num_web_purchases,
        customer.num_store_purchases,
        customer.num_web_visits_month,
        customer.recency,
    ]])
    scaled = scaler.transform(features)
    cluster = int(kmeans.predict(scaled)[0])
    info = SEGMENT_INFO[cluster]
    return {
        "cluster": cluster,
        "segment_name": info["name"],
        "emoji": info["emoji"],
        "color": info["color"],
        "description": info["description"],
        "marketing_strategy": info["strategy"],
    }


@app.get("/segments")
def get_segments():
    return SEGMENT_INFO
