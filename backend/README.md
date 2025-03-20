# Backend Setup Guide
1. **Create app.py**
    - This is the main backend file for the FastAPI application.
2. **Install dependencies**
    - Refer to `requirements.txt` for the list of required packages.
3. **Setup API key**
    - In .env file, add `GROQ_API_KEY=your_api_key_here`.
    - Load this key inside app.py using load_dotenv() to enable Llama 3.
4. **Initialize FastAPI instance**
5. **Connect Llama 3 with Groq**
    - Use ChatGroq to generate SQL from user questions.
6. **6. Convert Natural Language to SQL Queries**
    - Use LangChain’s SQLDatabaseChain to generate and execute SQL queries.
    - The AI will use the `subway_outlets` table from the MySQL database.
7. **Handle user input**
    - Use `pydantic` to validate user requests.
8. **Setup database connection**
    - Import the database connection from database.py.
9. **Create API endpoints**
    - `POST /query` - Convert user question into an SQL query and fetch results
        - Takes a natural language question.
        - Uses Llama 3 to generate an SQL query.
        - Returns the structured results.
    - `GET /outlets` - Retrieve all Subway outlets
        - Fetches all outlets from the MySQL database using SQLAlchemy.
        - Returns outlet details (name, address, operating hours, location, etc.).
10. **Run the server**
    - Start the backend with: `uvicorn app:app --reload`
