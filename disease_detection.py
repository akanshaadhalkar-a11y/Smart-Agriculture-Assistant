import os
import cv2
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

dataset_path = "dataset"

classes = [
    "Healthy",
    "Leaf_Blight",
    "Leaf_Spot"
]

X = []
y = []

for label in classes:

    folder_path = os.path.join(dataset_path, label)

    for image_name in os.listdir(folder_path):

        image_path = os.path.join(folder_path, image_name)

        img = cv2.imread(image_path)

        if img is not None:

            img = cv2.resize(img, (100,100))

            img = img.flatten()

            X.append(img)

            y.append(label)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier()

model.fit(X_train, y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Accuracy:", accuracy)

joblib.dump(model, "disease_model.pkl")

print("Disease model saved successfully")