from sklearn.linear_model import LinearRegression
import pickle

# Training data
X = [
    [1000, 2],
    [1500, 3],
    [2000, 3],
    [2500, 4],
    [3000, 4]
]

# House prices
y = [
    200000,
    300000,
    400000,
    500000,
    600000
]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained and saved.")