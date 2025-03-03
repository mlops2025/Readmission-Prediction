# Prediction of Readmission for Hyperglycemia Patients

# Introduction
Diabetes is a chronic disease where a person suffers from an extended level of blood glucose in the body. Diabetes is affected by height, race, gender, age but a major reason is considered to be a sugar concentration. The present analysis of a large clinical database was undertaken to examine historical patterns of diabetes care in patients with diabetes admitted to a US hospital and to inform future directions which might lead to improvements in patient safety. Reducing early hospital readmissions is a policy priority aimed at improving healthcare quality. In this case study we will see how machine learning can help us solve the problems caused due to readmission.

## Business Problem and Constaints:
It is estimated that 9.3% of the population in the United States have diabetes , 28% of which are undiagnosed. The 30-day readmission rate of diabetic patients is 14.4 to 22.7 % . Estimates of readmission rates beyond 30 days after hospital discharge are even higher, with over 26 % of diabetic patients being readmitted within 3 months and 30 % within 1 year. Costs associated with the hospitalization of diabetic patients in the USA were $124 billion, of which an estimated $25 billion was attributable to 30-day readmissions assuming a 20 % readmission rate. Therefore, reducing 30-day readmissions of patients with diabetes has the potential to greatly reduce healthcare costs while simultaneously improving care.

### Constraints:
Interpretability of model is very important Interpretability is always important in health care domain if model predict that some patient will readmit but cant explain why it came to this conclusion the doctor will be clueless about such decision and also doctor wont be able to tell the patient why he needs to readmit practically it will create lots of inconvenience to doctor as well as patient.
Latency is not strictly important Most of the health care related applications are not latency dependant.
The cost of misclassification is high If the patient that doesnt need to readmit if model says “yes to readmit” that will will put financial burden on the patient. If patient need to readmit but model say “no to readmit” then that will cause readmission cost to the hospital so, misclasification rate should be as low as possible.

## Git repository structure
```plaintext
.
├── README.md
├── airflow
│   ├── logs
│   │   └── __init__.py
│   └── src
│       ├── __init__.py
│       ├── data_processing
│       │   └── __init__.py
│       ├── data_validation
│       │   └── __init__.py
│       └── model
│           └── __init__.py
├── assets
│   └── plots
│       └── test.png
├── data
│   ├── processed
│   └── raw
│       ├── IDs_mapping.csv
│       ├── description.pdf
│       └── diabetic_data.csv
├── gcpdeploy
│   └── app.py
├── src
│   └── __init__.py
└── tests
    └── test_data.py

```

Each module is designed to be modular and testable, ensuring that the entire pipeline is both scalable and maintainable.

###Installation and Setup
Prerequisites

    Python: Version 3.8 or higher
    Docker: Ensure Docker or Docker Desktop is installed and running
    Git: For cloning the repository

###Steps for User Installation

    Clone the Repository:
    git clone https://github.com/your-repo/diabetic-readmission-prediction.git
    cd diabetic-readmission-prediction

    Verify Python Version:
    python --version

    Docker Setup:
    Ensure Docker is installed and that you have allocated sufficient memory (at least 4GB recommended) and CPU resources for the containers to run smoothly.

###Deployment and Execution

This project is containerized using Docker and orchestrated with Apache Airflow. Follow the steps below to deploy and run the full pipeline:

###Detailed Guide to Deployment

    Build Docker Images:
        Open a terminal in the project directory and execute:
        docker compose build

    Initialize Airflow:

        Run the following command to initialize Airflow. This step sets up the database, creates necessary directories, and prepares the environment:
        docker compose up airflow-init

    Run the Pipeline:

        Start all services by running:
        docker compose up

    Accessing the Airflow Dashboard:

        - Open your browser and navigate to http://localhost:8080 to access the Airflow dashboard.
        - Use the credentials specified in the docker-compose.yaml (default: username airflow, password airflow or as configured) to log in.
        - From the dashboard, you can monitor the status of your DAGs, view logs, and trigger manual runs if needed.
    
    Email Notifications (Optional):

        - The pipeline supports email notifications via SMTP settings defined in the docker-compose.yaml. Make sure to update the SMTP configuration (host, port, user, password) with valid credentials.
        - Notifications will alert you upon the successful completion of tasks or in case of failures.
    
    Shutting Down the Pipeline:

        - To stop the running containers, press Ctrl+C in the terminal where docker compose up is running.
        - To remove the containers (if needed), execute:
        docker compose down

    Environment and Configuration Variables

        User IDs:
        Adjust the user settings in the docker-compose.yaml file if you encounter permission issues. For example, set:
        user: "1000:0"

        Volume Mounts:
        The volumes are mounted to share the project files between your local machine and the containers. Update the paths if your project structure changes.
        SMTP Settings:
        Modify the SMTP environment variables for email alerts:
        AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
        AIRFLOW__SMTP__SMTP_PORT: 587
        AIRFLOW__SMTP__SMTP_USER: your-email@gmail.com
        AIRFLOW__SMTP__SMTP_PASSWORD: your-email-password
        AIRFLOW__SMTP__SMTP_MAIL_FROM: your-email@gmail.com

    Usage and Testing

        Running the Pipeline

        Once deployed, the Airflow scheduler will execute the pipeline as defined in the DAG. You can:

        - Monitor task progress through the Airflow UI.
        - Manually trigger DAG runs if immediate execution is required.

    Running Tests
    To ensure the reliability of each component:

        Unit Tests:
        Execute tests using a command like:
        pytest test_data.py

    Integration Tests:
    Run the integration tests for the entire pipeline by triggering the test_pipeline dag

###Logs and Error Monitoring

    - Logs are managed through the custom logging module (logger.py) and are available via the Airflow UI and container logs.
    - Custom exceptions in exceptions.py help in pinpointing issues during data ingestion, processing, or model prediction phases.

###Future Enhancements

    Model Training and Deployment:
    Extend the pipeline to include a training module and automate the deployment of the predictive model.
    Real-Time Processing:
    Incorporate real-time data ingestion for up-to-date readmission predictions.
    Advanced Bias Mitigation:
    Implement additional fairness techniques and explainability tools to further ensure the model's transparency and reliability.

    




