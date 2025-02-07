### **Frontend Development for AI-Powered Resume Tailoring Website**
The frontend will have an interactive **Grammarly-style editing system** and a **job tracking system** with a spreadsheet-like interface. Users will also receive **email/SMS notifications** for saved jobs.

---

## **1. Tech Stack for the Frontend**
- **Framework:** React (or Next.js for SSR benefits)
- **State Management:** React Context API / Redux (if complex)
- **UI Library:** Tailwind CSS + shadcn/ui for an interactive design
- **Notification Handling:** Firebase, Twilio (for SMS), Nodemailer (for email)
- **Spreadsheet-like Job Tracker:** React Table or Handsontable for grid-based job tracking

---

## **2. Frontend Features & Components**
### **2.1. Main Components**
1. **User Authentication Page**
   - OAuth (Google Sign-In) or email/password-based login.

2. **Dashboard**
   - Resume Upload Section
   - Job Tracking Section (Spreadsheet-like)
   - Settings (Notification Preferences)

3. **Resume Editing Page**
   - **Grammarly-style AI Suggestions**
     - Show **underlined** keyword mismatches.
     - Provide **inline suggestions** with an "Accept" or "Reject" button.
   - **Preview Mode**
     - Toggle between **raw text view** and **formatted preview**.

4. **Job Tracking System**
   - Users **add jobs** via a job posting URL.
   - The system **auto-fills** details using the scraper.
   - Editable **spreadsheet view** (React Table or Handsontable) with:
     - Job Title
     - Company
     - Status (Applied, Interviewing, Offer, Rejected)
     - Application Date
     - Follow-up Reminder Date

5. **Notification System**
   - Users **set reminders** for follow-ups.
   - Send **email/SMS notifications** for:
     - Upcoming interviews.
     - Follow-up deadlines.
     - New AI suggestions for stored resumes.

---

## **3. UI/UX Breakdown**
### **3.1. Resume Editing (Grammarly-Style)**
✅ **Interactive Text Highlighting**
- Underlines issues like **missing skills, weak wording, keyword mismatches**.
- Click on suggestions to apply changes.

✅ **Accept/Reject System**
- Users click **"Accept"** to apply AI suggestions instantly.
- Users click **"Reject"** to keep original wording.

✅ **Side Panel for Changes**
- Show all **pending AI suggestions**.
- Toggle **before/after comparison**.

✅ **Live ATS Score**
- Display a **job match score** based on extracted keywords.

---

### **3.2. Job Tracking (Spreadsheet-Like UI)**
✅ **Editable Table View**
- Users can **edit job application details** (company, status, date).
- Use **React Table** or **Handsontable** for grid functionality.

✅ **Job Auto-Fill**
- Scrape job details from LinkedIn or Indeed URLs.
- Auto-populate **title, company, location, and requirements**.

✅ **Status Filters**
- Users filter jobs by **status (Applied, Interviewing, Offer, etc.).**

✅ **Export to CSV**
- Users export job tracking data as **CSV for Excel or Google Sheets**.

---

### **3.3. Notification System (Email/SMS)**
✅ **Reminder Scheduling**
- Users **set reminders** for:
  - Follow-ups (1 week after applying)
  - Interviews (24-hour reminder)

✅ **Notification Methods**
- **Email:** Use **Nodemailer** (or Firebase for bulk emails).
- **SMS:** Use **Twilio** for text reminders.

✅ **Customizable Alerts**
- Users select **how they want to receive alerts** (email, SMS, or both).

---

## **4. API Endpoints for Frontend Integration**
### **4.1. Resume Processing**
```plaintext
POST /upload-resume 
- Uploads resume file 
- Returns parsed text for AI analysis
```
```plaintext
POST /analyze-resume
- Takes resume text & job description
- Returns AI suggestions
```

### **4.2. Job Tracking**
```plaintext
POST /add-job
- Adds a new job entry to the database
```
```plaintext
GET /jobs
- Fetches all jobs saved by the user
```
```plaintext
PUT /update-job
- Updates job application status
```
```plaintext
DELETE /delete-job
- Removes a job from tracking
```

### **4.3. Notifications**
```plaintext
POST /set-reminder
- Schedules an email/SMS reminder
```
```plaintext
POST /send-notification
- Sends immediate notifications for upcoming events
```

---

## **5. Development Roadmap for Frontend**
### **Phase 1: Core UI**
✅ Setup React & Next.js  
✅ Create Authentication (OAuth or Email/Password)  
✅ Design Dashboard UI (Resume Upload + Job Tracker)

### **Phase 2: Grammarly-Style Resume Editing**
✅ Implement AI-powered **text highlighting**  
✅ Create **Accept/Reject UI** for suggestions  
✅ Display **AI-generated missing qualifications**  

### **Phase 3: Job Tracker System**
✅ Build **spreadsheet-style table UI**  
✅ Auto-fill job details from URLs  
✅ Implement **filters for tracking applications**  

### **Phase 4: Notification System**
✅ Implement **email notifications** (Nodemailer)  
✅ Integrate **Twilio SMS reminders**  
✅ Add **reminder scheduling** in the UI  

---

## **6. Next Steps**
1. **Develop Backend Endpoints** (FastAPI)
2. **Connect AI Resume Analysis to Frontend**
3. **Build Spreadsheet Job Tracker with React Table**
4. **Integrate Notifications & Deploy MVP**
