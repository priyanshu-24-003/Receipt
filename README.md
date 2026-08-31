# Receipt

## About
- An app that Uses Prediction pipeline to respond back the Insurance Premium 
- More on Mlops Aspect less on Data Science
---

## App + Prediction Pipline
- Takes user input from WebUi.
- Fetches the model from S3 bucket.
- predicts the output.
- responds back

---

## Training Pipline
- Data Ingestion (Mongodb data import --> TrainTestsplit --> Logged Artifacts)
- Data Validation (Validated the Imported data)
- Data Transformation (Scaling, OrdinalEncoding --> Logged Artifact)
- Model Training (Random Forest --> Logged Artifact)
- Model Evaluation (evaluates model , save metrics, ---> pass metrics to Pusher)
- Model Pusher  (compare with AWS previous model) --> push to aws(if found better))


## 📊 Experimentation

* Exploratory Data Analysis (EDA)
* Model Selection (Random Forest)
---

## ⚙️ Environment Setup

* Conda virtual environment (`python=3.10`)
* Dependency management via `requirements.txt`
* Package verification using `pip list`

---


## 🧱 Project Setup & Packaging

* Python package setup using:

  * `setup.py`
  * `pyproject.toml`
* Local package import using `-e .`

---

## 🪵 Logging & Exception Handling

* Centralized logging module
* Custom exception handling
---


## 🧰 Utility Functions

* Common helper functions in `utils`

---

## ☁️ MongoDB Integration

* MongoDB Atlas setup
* Data storage & retrieval
* Environment variable configuration (`MONGODB_URL`)

---

## ☁️ AWS S3 Integration

* IAM user & access setup
* S3 bucket for model storage
* AWS connection module
* Model push & pull from S3

* Environment variable configuration (`AWS_ACCESS_KEY_ID`)
* Environment variable configuration (`AWS_SECRET_ACCESS_KEY`)

---

## 🚀 Production Deployment (MLOps)

* Docker containerization
* Port exposure (5000)

* AWS Services:

  * ECR (Docker registry)
  * EC2 (deployment server)

---

## 🔁 CI/CD Pipeline

* CI/CD pipeline using GitHub Actions
* Self-hosted GitHub runner on EC2
* GitHub secrets for AWS credentials
---

## 🌍 Deployment

* AWS EC2 instance hosting FastApi app

---

## 🧰 Tools & Technologies Used
* python (hardcoded the pipeline without any standard MLops tool)
* Modules (logging, sys, exception, os, yaml, boto, pymongo, FastApi)
* MongoDB Atlas (cloud for data)
* AWS (IAM, S3, ECR, EC2)



## ✅ Project Status

* MVP1 Completed
* Fully functional training & prediction pipeline deployed on cloud

---

## 🧰 Scope of Improvments

* Feature If enabled Runs the pipeline from any specified point
* Better Experiment Tracking using MlFlow
