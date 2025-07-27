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
