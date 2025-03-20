# SQL LangChain Subway Chatbot with Groq Llama 3 (Direct Querying)

This repository focuses on building the Subway AI Chatbot using SQL LangChain (Direct Querying). For details on MySQL Database Setup, Web Scraping Workflow, and Geocoding Extraction, refer to the [Backend Guide Setup](https://github.com/FarihaAnis/subway-aichatbot/tree/master/backend).

## Chatbot Architecture
The chatbot operates as an end-to-end SQL Q&A system, where users can ask questions about Subway outlets in Kuala Lumpur without needing SQL knowledge.

As shown in the diagram below, the chatbot processes natural language questions using an LLM (Llama 3 via Groq) to generate an SQL query. The query is then executed on a database, and the results are converted into a natural language answer. The system currently follows a direct execution approach, while the SQL Agent remains optional for future enhancements, such as improving query accuracy or handling more complex requests.

<div align="center">
    <h3><b>Chatbot Query Processing Flow</b></h3>
    <img src="chatbot-workflow.png" alt="Chatbot Query Processing Flow">
    <p style="font-size: 12px; color: gray;">
        Source: <a href="https://python.langchain.com/docs/tutorials/sql_qa/#system-prompt" target="_blank">
        LangChain SQL Q&A Documentation</a>
    </p>
</div>


---

## Architecture Breakdown

The chatbot follows a four-step process to convert user queries into database-driven responses:

#### **1️⃣ Natural Language Input (User Query)**  
- Users submit plain-text questions (e.g., *"How many outlets are located in Bangsar?"*).  
- The chatbot receives the natural language query and processes it using an LLM (Llama 3 via Groq).

---

#### **2️⃣ SQL Query Generation (LLM + LangChain)**  
- The LLM converts the natural language query into a structured SQL query.  
- The SQL query is generated dynamically based on the database schema.  
- LangChain’s `SQLDatabaseChain` automates query construction and execution.  
- This allows non-technical users to query structured databases without writing SQL manually.

---

#### 3️⃣ **Query Execution (Database Layer - MySQL)**
- The generated SQL query is executed against a MySQL database.
- The SQLAlchemy ORM (`get_db()`) manages database transactions, ensuring efficient data retrieval.
- The database returns structured results containing relevant outlet information.

---

#### 4️⃣ **Answer Generation (LLM + Response Formatting)**
- The LLM formats the raw database results into a human-friendly response.

---

## Tools & Technologies
◽**Backend (FastAPI & SQL LangChain)**
- FastAPI – Web framework for handling API requests
- Llama 3 via Groq – Large Language Model for SQL query generation
- SQL LangChain (SQLDatabaseChain) – Converts natural language questions into SQL queries
- SQLAlchemy – ORM for database transactions
- MySQL – Database for storing Subway outlet data
- dotenv (python-dotenv) – Manages environment variables
- Uvicorn – ASGI server to run FastAPI
  
◽**Frontend (Streamlit)**
- Streamlit – UI framework for chatbot interface
- Requests – Fetches data from FastAPI backend
- Folium – Maps Subway outlets visually
- Streamlit-Folium – Integrates Folium maps with Streamlit
geopy – Calculates distances between locations

◽**Additional Modules**
- os – Handles file paths and environment variables
- re – Extracts SQL from LLM responses

---

## Why Use Groq, SQL LangChain, Llama 3, and Streamlit?
This chatbot is built using free-tier resources, making it an efficient and cost-effective solution for handling SQL queries through natural language input.
- Groq (Free Version) provides fast inference for Llama 3 without the need for expensive GPUs, making real-time query generation possible.
- SQL LangChain converts user questions into SQL queries and executes them directly, eliminating the need for manual query writing.
- Llama 3 (via Groq) is a free, high-performance language model that helps interpret user queries and structure SQL statements accurately.
- Streamlit is used for the frontend to quickly deploy an AI chatbot with a simple UI, thanks to its Python-native support, built-in UI components, and easy integration with the FastAPI backend.
  
By combining these tools, the chatbot can process natural language questions, generate SQL queries, and fetch relevant results—all while keeping the setup lightweight and accessible.

---

## 📽️ Demo Video  

[Watch the Demo](https://github.com/FarihaAnis/SQL-LangChain-Subway-Chatbot-with-Groq-Llama-3-Direct-SQL-Querying-/blob/master/demo.mp4)


## 📚 References  

- [LangChain SQL Q&A Documentation](https://python.langchain.com/docs/tutorials/sql_qa/#system-prompt)  
- [Groq API Documentation](https://console.groq.com/docs/overview)  
