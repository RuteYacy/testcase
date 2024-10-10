import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

model = None


def train_model():
    """
    Train the model and return the trained model.
    """
    global model

    # Generate example data for training the model
    num_samples = 1000
    np.random.seed(42)
    data = {
        "total_income": np.random.uniform(2000, 10000, num_samples),
        "total_spending": np.random.uniform(500, 8000, num_samples),
        "balance_fluctuation": np.random.uniform(100, 2000, num_samples),
        "intensity": np.random.uniform(0, 1, num_samples),
        "emotion": np.random.choice(
            ["anger", "anxiety", "stress", "happiness", "calm", "neutral",
             "sadness", "fear", "surprise"],
            num_samples
        )
    }

    emotion_map = {
        "anger": 0, "anxiety": 1, "stress": 2,
        "happiness": 3, "calm": 4, "neutral": 5,
        "sadness": 6, "fear": 7, "surprise": 8
    }

    df = pd.DataFrame(data)
    df["emotion_encoded"] = df["emotion"].map(emotion_map)

    # Create a synthetic risk score based on features
    df["risk_score"] = (
        0.3 * df["total_spending"] / (df["total_income"] + 1) +
        0.2 * df["balance_fluctuation"] / 1000 +
        0.5 * df["intensity"] * df["emotion_encoded"] / 8
    )
    df["risk_score"] = df["risk_score"].clip(0, 1)

    # Features (X) and target (y)
    X = df[["total_income", "total_spending", "balance_fluctuation",
            "intensity", "emotion_encoded"]]
    y = df["risk_score"]

    # Train the RandomForestRegressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    print("Model trained successfully.")
    return model
