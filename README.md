# **AI-Powered Resume Tailoring Website**

## **Project Overview**
This project is a web-based tool designed to help users tailor their resumes to specific job postings. Users can upload their resumes, search for jobs through the **Indeed API**, and receive **AI-powered resume recommendations**. The system analyzes job descriptions and provides suggestions to improve alignment between the resume and job requirements. Users can also track their job applications using a personalized **Job Tracking Dashboard**.

---

## **Features**
### **User Features**
- **User Authentication**
  - Register, login, and logout functionality with encoded passwords.
  - User data stored in a **SQLite database**.

- **Resume Upload & Parsing**
  - Accepts **PDF, DOCX, and TXT** resume formats.
  - Extracts structured text and stores it in the database.

- **Job Search Integration**
  - Uses **Indeed API** for job searches.
  - Allows users to search and retrieve job postings based on title and location.

- **AI-Powered Resume Analysis**
  - Compares the **resume content** with job postings.
  - Highlights **missing qualifications and skills**.
  - Assigns a **match score** based on resume-job alignment.
  - Future plans to allow users to **edit AI-generated recommendations** directly in the UI.

- **Job Tracking Dashboard**
  - Users can save job postings to track their applications.
  - Automatically **scores each saved job** based on the resume.

- **Resume Download**
  - Users can download **AI-enhanced resumes**.

---

## **Tech Stack**
### **Frontend**
- **React** (Frontend framework)
- **React Router** (Navigation)
- **Axios** (API calls)
- **Context API** (User state management)

### **Backend**
- **Flask** (REST API)
- **Flask-CORS** (Handles cross-origin requests)
- **Werkzeug** (Secure file handling)
- **SQLite** (Database for user, job, and resume storage)

### **AI & Resume Analysis**
- **OpenAI API** (For generating resume suggestions)
- **Resume Scoring Logic** (Custom AI-based scoring system)

### **Job Data**
- **Indeed API** (For job searching and job posting retrieval)

### **Storage**
- Local file storage for resumes *(potential AWS S3 integration in the future)*.

---

## **Project Setup**
### **Backend Setup**
1. **Clone the repository**  
   ```
   git clone [repository_url]
   cd backend
   ```

2. **Create a virtual environment and activate it**  
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

4. **Set up the database**  
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. **Run the Flask server**  
   ```
   flask run --host=0.0.0.0 --port=5001
   ```

### **Frontend Setup**
1. **Navigate to the frontend folder**  
   ```
   cd frontend
   ```

2. **Install dependencies**  
   ```
   npm install
   ```

3. **Start the React app**  
   ```
   npm start
   ```

---

## **API Endpoints**
### **Authentication**
- `GET /users` – Retrieve all users.  
- `GET /users/<user_id>` – Retrieve a specific user.  
- `POST /users/register_user` – Register a new user.  


### **Resume Handling**
- `POST /upload` – Upload a resume file.  
- `GET /download/<int:user_id>` – Download a resume.  
- `POST /resume_score` – Returns resume score for specific job and resume
- `POST /resumes/suggestions` – Returns resume suggestions for specific job and resume
- `Get /view/<int:user_id>` – Returns Users Resume to view

### **Job Search**
- `POST /job_search` – Fetch jobs using the **Indeed API**.  
- `GET /jobs` – Retrieve stored job listings.  
- `GET /jobs/<int:job_id>` – Retrieves details for specific job

### **AI-Powered Resume Optimization**
- `POST /resume_score` – Get AI-based resume suggestions and a match score.  

### **Job Handling**
- `GET /<int:user_id>/saved_jobs` - returns saved jobs
- `POST /<int:user_id>/saved_jobs/<int:job_id>/delete` - removes saved job
- `POST <int:user_id>/saved_jobs/<int:job_id>/save` - saves a selected job
---

## **Database Schema**
The project uses **SQLite** for data storage. Below is an overview of the database schema:

### **Users Table**
| Column | Type | Description |
|--------|------|------------|
| id | INTEGER | Primary Key |
| username | TEXT | Unique identifier |
| email | TEXT | User email |
| password | TEXT | Hashed password |
| first_name | TEXT | First name |
| last_name | TEXT | Last name |
| phone | TEXT | Optional phone number |
| city | TEXT | User city |
| zipcode | TEXT | User ZIP code |
| job_titles | TEXT | User’s job preferences |

### **Resumes Table**
| Column | Type | Description |
|--------|------|------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key (Users Table) |
| file_path | TEXT | Path to stored resume file |
| parsed_text | TEXT | Extracted resume content |

### **Jobs Table**
| Column | Type | Description |
|--------|------|------------|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key (Users Table) |
| job_title | TEXT | Job title from Indeed API |
| company | TEXT | Company name |
| job_description | TEXT | Full job description |
| location | TEXT | Job location |
etc
---

## **Development Roadmap**
### **Phase 1: Core Functionality (Completed/In Progress)**
- [X] Flask backend setup  
- [X] Resume upload and parsing  
- [X] Job search via Indeed API  
- [X] Database setup with `users`, `resumes`, and `jobs` tables  
- [ ] AI-based resume recommendation system *(In Progress)*  
- [ ] Implement AI match score logic in the UI *(Not yet integrated)*  

### **Phase 2: Enhancements**
- [ ] Integrate AI-generated suggestions into UI  
- [ ] Implement job tracking dashboard  
- [ ] Improve AI model accuracy with fine-tuning  
- [ ] UI/UX improvements for a better user experience  

---

## **Next Steps**
1. **Complete AI-Powered Resume Analysis**  
   - Connect OpenAI API responses to the UI for real-time suggestions.  

2. **Develop Job Tracking Dashboard**  
   - Allow users to save jobs and track application progress.  

3. **Improve Resume Optimization Model**  
   - Fine-tune keyword and qualification matching for better results.  

4. **Enhance Resume Storage Behavior**  
   - Decide if multiple resumes per user should be allowed or overwritten.  

---

## **Project Notes**
- **This project is NOT being deployed** (for capstone class use only).  
- **Authentication is implemented** but does not follow OAuth/JWT standards.  

---

## **Contributors**

* Eduardo Benjamin
* Jaden Castle
* Jackson Giezma

---

## **License**
MIT License
