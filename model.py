import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import mlflow
import mlflow.sklearn

# Load the preprocessed data
df = pd.read_csv('./data/processed_data.csv')

# Define features and target variable
X = df[['Humidity', 'Wind Speed']]  # Add other features as needed
y = df['Temperature']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start an MLflow run
with mlflow.start_run():
    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Log model parameters
    mlflow.log_param("random_state", 42)
    mlflow.log_param("test_size", 0.2)

    # Log model metrics
    score = model.score(X_test, y_test)
    mlflow.log_metric("score", score)

    # Log the model
    mlflow.sklearn.log_model(model, "model")

    # Register the model
    mlflow.register_model(
        "runs:/{}/model".format(mlflow.active_run().info.run_id),
        "LinearRegressionModelProd"
    )

    print("Model trained, logged, and registered with MLflow")

# Save the model as a pickle file
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")