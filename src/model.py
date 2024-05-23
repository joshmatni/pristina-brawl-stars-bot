from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

# Simulated DataFrame (replace this with actual data fetching and preprocessing)
data = pd.DataFrame({
    '3vs3Victories': np.random.randint(100, 500, 1000),
    'expLevel': np.random.randint(1, 300, 1000),
    'highestTrophies': np.random.randint(1000, 5000, 1000),
    'rank': np.random.randint(1, 35, 1000),
    'won_1v1': np.random.choice([0, 1], 1000)  # 0 for loss, 1 for win
})

# Feature and target separation
X = data[['3vs3Victories', 'expLevel', 'highestTrophies', 'rank']]
y = data['won_1v1']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict on test data
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

# Save model for later use
import joblib
joblib.dump(model, 'logistic_regression_model.pkl')

