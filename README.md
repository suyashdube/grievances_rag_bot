# grievances_rag_bot
## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

##  Step 2: Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

##  Step 3: Configure Environment

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```
## Step 4: Run the server 

run the backend server in terminal 1 with the command "python run_api.py"
and in the terminal 2 start the streamlit server with the command "python -m streamlit run streamlit_app.py"

##  How to Use

### Register a Complaint

1. Start with messages like:
   - "I have issues with my laptop"
   - "Register a complaint for me"
   - "My computer is not working"

2. Follow the guided steps:
   - Provide your full name
   - Enter your mobile number
   - Describe your complaint in detail

3. Receive your unique Complaint ID

### Check Complaint Status

1. Ask about status:
   - "What's the status of my complaint?"
   - "Check status for complaint ID 123"
   - "Status for mobile 9876543210"

2. Get detailed status information including:
   - Complaint ID and details
   - Current status (Registered, In Progress, Under Review, Resolved, Closed)
   - Registration date

## 🔧 API Endpoints

### POST `/register_complaint`
Register a new grievance
```json
{
  "name": "John Doe",
  "mobile": "9876543210",
  "complaint_details": "Laptop screen is flickering"
}
```

### GET `/complaint_status/{complaint_id}`
Get complaint status by ID

### GET `/complaint_status_by_mobile/{mobile}`
Get latest complaint status by mobile number


## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **LLM**: Google Gemini Flash
- **Vector Store**: ChromaDB
- **Embeddings**: SentenceTransformers (all-MiniLM-L6-v2)
- **Language**: Python 3.8+

