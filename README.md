Voya AI: Intelligent Wildlife Registry
Live Demo: neighbor-loop-73358856972.us-central1.run.app

🐾 Overview
Voya AI is an Intelligent Wildlife Registry designed to streamline the identification and cataloging of wildlife species using AI-enabled database features. Built with a focus on scalability and modern web standards, the application provides an intuitive interface for researchers and conservationists to manage biodiversity data effectively.

🚀 Key Features
AI-Powered Insights: Leverages AI to enhance database queries and provide intelligent data associations.
Real-time Registry: A dynamic dashboard for tracking wildlife sightings and metadata.
Cloud-Native Architecture: Fully containerized using Docker and deployed on Google Cloud Run for high availability and auto-scaling.
Responsive Design: Optimized for both desktop and mobile viewing using modern CSS and HTML5.

🛠️ Tech Stack
Frontend: HTML5, CSS3, JavaScript
Backend: Python (Flask/Streamlit framework)
Database: AlloyDB for PostgreSQL with AI-enabled features
DevOps: Docker, Google Cloud Build, Google Cloud Run
Version Control: Git & GitHub

📦 Project Structure
neighbor-loop/
├── app.py              # Main application logic
├── app.html            # Frontend template
├── static/             # Assets (images/CSS)
├── templates/          # HTML templates
├── Dockerfile          # Container configuration
└── requirements.txt    # Python dependencies

🛠️ Installation & Setup
Clone the repository:
git clone https://github.com/Swagata191/Voya-AI.git
cd Voya-AI

Set up environment variables:
Create a .env file (ignored by Git) and add your Project ID:
PROJECT_ID=voya-491216

Run with Docker:
docker build -t voya-ai .
docker run -p 8080:8080 voya-ai

📄 License
This project is licensed under the Apache-2.0 License.
