import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv('matchup_outcomes.csv')

# Prepare features and labels
# 'Player1_Score' and 'Player2_Score' features, and 'Winner' is the label
X = data[['Player1_Score', 'Player2_Score']]
y = data['Winner'] == data['Player1_Name']  # binary variable: 1 if Player1 wins, 0 otherwise

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LogisticRegression()

# Train model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print("Accuracy:", accuracy)
print("Classification Report:\n", report)
