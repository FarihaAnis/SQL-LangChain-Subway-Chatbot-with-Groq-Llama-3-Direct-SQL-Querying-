from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from langchain_groq import ChatGroq
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
import os
from schemas import SubwayOutletSchema
from typing import List
from database import get_db 

# ✅ Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Ensure it's set in your .env file.")

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Initialize Llama 3 with Groq API Key
llm = ChatGroq(model="llama-3.3-70b-versatile", 
               api_key=GROQ_API_KEY,
               temperature=0,
               top_p=0.9)

# ✅ Define API request model
class QueryRequest(BaseModel):
    question: str

# ✅ Define API route for querying Subway outlets using SQL LangChain
@app.post("/query")
def query_database(request: QueryRequest, db: Session = Depends(get_db)):  # ✅ Use existing database session
    try:
        # ✅ Initialize SQLDatabase with the existing SQLAlchemy session
        sql_database = SQLDatabase(engine=db.bind)  # Uses the existing database connection
        sql_chain = SQLDatabaseChain.from_llm(llm, sql_database, verbose=True)

        # ✅ Generate and execute SQL query using LangChain
        query_result = sql_chain.run(request.question)

        return {"query": request.question, "results": query_result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Subway Outlet API Endpoints
@app.get("/outlets", response_model=List[SubwayOutletSchema])
def get_all_outlets(db: Session = Depends(get_db)):  # ✅ Use existing database session
    try:
        # ✅ Fetch all Subway outlets using SQLAlchemy session
        outlets = db.execute("SELECT name, address, operating_hours, waze_link, latitude, longitude FROM subway_outlets;").fetchall()

        if not outlets:
            raise HTTPException(status_code=404, detail="No Subway outlets found")

        # ✅ Convert query result into a list of dictionaries
        column_names = ["name", "address", "operating_hours", "waze_link", "latitude", "longitude"]
        result = [dict(zip(column_names, row)) for row in outlets]

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
