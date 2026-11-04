import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Get the backend folder path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset location
DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "Concrete_Data.xls"
)

# Load dataset
print("Loading dataset...")
df = pd.read_excel(DATASET_PATH)

# Clean column names
df.columns = df.columns.str.strip()

print("\nDataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

# Features = all columns except the last one
X = df.iloc[:, :-1]

# Target = last column (Concrete Strength)
y = df.iloc[:, -1]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create and train the model
print("\nTraining Random Forest model...")
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Calculate metrics
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\n----- MODEL RESULTS -----")
print(f"MAE: {mae:.2f} MPa")
print(f"RMSE: {rmse:.2f} MPa")
print(f"R² Score: {r2:.4f}")

# Save model
MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "concrete_strength_model.pkl"
)

joblib.dump(model, MODEL_PATH)

print(f"\nModel saved successfully!")
print(f"Location: {MODEL_PATH}")