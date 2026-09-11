import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("dataset/Crop_recommendation.csv")

# Input features
X = data.drop("label", axis=1)

# Output label
y = data["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model/crop_model.pkl", "wb"))

print("Model Trained Successfully")