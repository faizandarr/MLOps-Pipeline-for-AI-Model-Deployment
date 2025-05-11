# MLOps Pipeline for Weather Data Analysis

This repository contains a complete MLOps pipeline for weather data collection, preprocessing, model training, and deployment. The pipeline incorporates tools such as DVC, Apache Airflow, MLFlow, and CI/CD practices to ensure reproducibility, scalability, and seamless deployment.

## **Table of Contents**

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Airflow Pipeline](#running-the-airflow-pipeline)
  - [Model Training and Versioning](#model-training-and-versioning)
  - [Full-Stack Application Deployment](#full-stack-application-deployment)
- [Project Structure](#project-structure)
- [Key Learnings](#key-learnings)
- [Contributing](#contributing)

---

## **Introduction**

This project demonstrates the implementation of MLOps principles to handle live weather data and predict temperature based on weather conditions. It includes:

- Automated workflows using **Apache Airflow**.
- Dataset and model versioning with **DVC**.
- Model logging and registration using **MLFlow**.
- CI/CD pipelines for seamless development, testing, and deployment.

---

## **Features**

- **Data Collection:** Fetches live weather data from the [WeatherAPI](https://www.weatherapi.com/).
- **Data Preprocessing:** Handles missing values and normalizes weather features.
- **Model Training:** Predicts temperature using a linear regression model.
- **Version Control:** Tracks datasets and models with DVC.
- **Workflow Automation:** Utilizes Airflow to automate data collection and preprocessing.
- **Full-Stack Application:** Includes a React frontend and Flask API for user interactions.
- **CI/CD Pipelines:** Automates testing, Docker image building, and deployment on Kubernetes.

---

## **Technologies Used**

- **Programming Languages:** Python, JavaScript (React)
- **Version Control:** Git, DVC
- **Workflow Automation:** Apache Airflow
- **Model Management:** MLFlow
- **Frontend Framework:** React
- **Backend Framework:** Flask
- **Database:** SQLite
- **Deployment:** Docker, Kubernetes (Minikube)

---

## **Getting Started**

### **Prerequisites**

Ensure you have the following installed:

- Python 3.8+
- Node.js and npm (for React frontend)
- Docker
- Kubernetes with Minikube
- Apache Airflow

### **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/SMuhammadMustafa/mlops-project.git
   cd mlops-project
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize DVC and set up remote storage:
   ```bash
   dvc init
   dvc remote add -d myremote gdrive://<your-remote-path>
   ```

4. Install Node.js dependencies for the frontend:
   ```bash
   cd frontend
   npm install
   ```

5. Start the Airflow webserver and scheduler:
   ```bash
   airflow db init
   airflow webserver &
   airflow scheduler &
   ```

---

## **Usage**

### **Running the Airflow Pipeline**

1. Define Airflow variables for WeatherAPI key and DVC paths.
2. Trigger the DAG from the Airflow UI to collect and preprocess data.

### **Model Training and Versioning**

1. Train the model and log with MLFlow:
   ```bash
   python model.py
   ```

2. Track the model with DVC:
   ```bash
   dvc add model.pkl
   git commit -m "Add trained model"
   ```

### **Full-Stack Application Deployment**

1. Build and run the Docker container:
   ```bash
   docker build -t weather-app .
   docker run -p 5000:5000 weather-app
   ```

2. Deploy the application to Kubernetes using Minikube:
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

---

## **Project Structure**

```
weather-mlops-pipeline/
├── airflow/                # Airflow DAGs and configs
├── data/                   # Raw and processed data
├── frontend/               # React frontend
├── models/                 # Model files and logs
├── scripts/                # Data collection and preprocessing scripts
├── requirements.txt        # Python dependencies
├── train_model.py          # Model training script
├── log_model.py            # MLFlow logging script
├── Dockerfile              # Docker configuration
└── k8s-deployment.yaml     # Kubernetes deployment file
```

---

## **Key Learnings**

1. Effective use of **DVC** for dataset and model versioning.
2. Leveraging **Apache Airflow** for workflow automation.
3. Streamlined model lifecycle management with **MLFlow**.
4. CI/CD pipelines to ensure reproducibility and smooth deployment.

---

## **Contributing**

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Add feature description"`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.
