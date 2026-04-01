# Voya AI: Intelligent Wildlife Registry

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Cloud%20Run-blue?style=for-the-badge&logo=google-cloud)](https://neighbor-loop-73358856972.us-central1.run.app/)
[![License](https://img.shields.io/badge/License-Apache%202.0-orange?style=for-the-badge)](LICENSE)

Voya AI is a sophisticated **Intelligent Wildlife Registry** designed to catalog and identify wildlife species. By leveraging **AI-enabled database features** and a cloud-native architecture, it provides a scalable platform for biodiversity data management and research.

---

## 🚀 Key Features

* **Intelligent Identification:** Leverages AI to provide smart data associations within the registry.  
* **Real-time Tracking:** A dynamic dashboard for immediate species metadata management.  
* **Scalable Infrastructure:** Fully containerized and deployed via **Google Cloud Run**.  
* **Modern UI:** A responsive, professional interface optimized for all devices.  

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Python (Flask / Streamlit) |
| **Database** | AlloyDB for PostgreSQL (AI-Enabled) |
| **Cloud/DevOps** | Docker, Google Cloud Build, GCP Run |
| **Version Control** | Git & GitHub |

---

## 📂 Project Structure
```text
neighbor-loop/
├── app.py              # Core application logic
├── templates/          # HTML frontend templates
├── static/             # CSS and Image assets
├── Dockerfile          # Containerization instructions
├── requirements.txt    # Python dependency manifest
└── .gitignore          # Protected configuration (Excludes .env)
```
---

## ⚙️ Installation & Local Setup  

### 1. Clone the Project
```bash
git clone [https://github.com/Swagata191/Voya-AI.git](https://github.com/Swagata191/Voya-AI.git)
cd Voya-AI
```
### 2. Configure Environment  
Create a .env file in the root directory to store the Project ID:
```bash
PROJECT_ID=voya-491216
```
### 3. Deploy with Docker  
```bash
docker build -t voya-ai .
docker run -p 8080:8080 voya-ai
```
---

## 📄 License  
Distributed under the Apache-2.0 License.

--- 

## Developed by Swagata Maji
