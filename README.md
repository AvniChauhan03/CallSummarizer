# CallSummarizer

This accepts a call transcript via a POST request, sends it to the Groq API to summarize and detect sentiment, extracts the summary and aentiment, normalizes them, saves everything in a CSV file and retuns the result as a JSON response.
