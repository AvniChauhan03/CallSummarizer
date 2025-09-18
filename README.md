# CallSummarizer

This accepts a call transcript via a POST request, sends it to the Groq API to summarize and detect sentiment, extracts the summary and aentiment, normalizes them, saves everything in a CSV file and retuns the result as a JSON response.

# Working
1. Activate the python virtual environment: 
   .\venv\Scripts\Activate.ps1
   
2. Install required packages:
   pip install fastapi uvicorn pydantic groq

3. Put the Api key:
   $env:GROQ_API_KEY="API_KEY_HERE"

4. Start the server:
   python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000

5. Open the swagger UI in browser:
   http://127.0.0.1:8000/docs

6. Test the /analyze endpoint by pasting the transcript and click execute. Check the CSV file that will now get created in VS code. It will contain the final result.

