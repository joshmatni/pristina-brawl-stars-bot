import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Example DataFrame
data = {
    'highestTrophies': [4000, 3000, 4500, 3200],
    'expLevel': [100, 80, 120, 85],
    '3vs3Victories': [200, 150, 240, 180],
    'brawlerRank': [20, 15, 25, 18],
    'outcome': [1, 0, 1, 0]  # 1 for win, 0 for lose
}

df = pd.DataFrame(data)

# Assign weights
weights = {'highestTrophies': 0.4, 'expLevel': 0.2, '3vs3Victories': 0.2, 'brawlerRank': 0.2}
for column, weight in weights.items():
    df[column] *= weight

# Prepare data for training
X = df[['highestTrophies', 'expLevel', '3vs3Victories', 'brawlerRank']]
y = df['outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))
