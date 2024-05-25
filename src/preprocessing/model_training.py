import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib  # Import joblib for model saving and loading


data = pd.read_csv('final_matchup_outcomes.csv')
data.dropna(inplace=True)  # Removes any rows with missing data

# Prepare features and labels
X = data[['Player1_Score', 'Player2_Score']]  # Features
y = data['Winner'] == data['Player1_Name']  # Labels: True if Player1 wins, else False

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
joblib.dump(scaler, 'scaler.pkl')

# Check if the model file exists to load; otherwise, create a new one
model_file_path = 'bs_1v1_predictor.pkl'
try:
    model = joblib.load(model_file_path)  # Try to load the existing model
    print("Model loaded successfully.")
except FileNotFoundError:
    print("No existing model found. Training a new model.")
    model = LogisticRegression()  # Create a new Logistic Regression model
    model.fit(X_train, y_train)  # Train the model
    joblib.dump(model, model_file_path)  # Save the newly trained model
    print("Model trained and saved.")

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model using accuracy and a classification report
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print("Accuracy:", accuracy)
print("Classification Report:\n", report)


