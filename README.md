# SQL LangChain Subway Chatbot with Groq Llama 3 (Direct Querying)

## Overview
For database setup, 


## Chatbot Architecture
The chatbot operates as an end-to-end SQL Q&A system, where users can ask questions about Subway outlets in Kuala Lumpur without needing SQL knowledge.

## System Architecture Overview  

The chatbot operates as an **end-to-end SQL Q&A system**, allowing users to ask questions about Subway outlets in Kuala Lumpur **without needing SQL knowledge**.  

As shown in the diagram below, the architecture is designed to be fast and efficient, enabling real-time query execution while staying flexible for future improvements. The system currently executes queries directly with the SQL Agent as an optional feature that could be added later for tasks like enhancing query accuracy or handling more complex requests.  

<h4 style="text-align: center;">Chatbot Query Processing Flow</h4>

<p align="center">
  <img src="chatbot-workflow.png" alt="Chatbot Query Processing Flow">
</p>

---

## Architecture Breakdown

The chatbot follows a four-step process to convert user queries into database-driven responses:

### **1️⃣ Natural Language Input (User Query)**  
- Users submit plain-text questions (e.g., *"How many outlets are located in Bangsar?"*).  
- The chatbot receives the natural language query and processes it using an LLM (Llama 3 via Groq).

---

### **2️⃣ SQL Query Generation (LLM + LangChain)**  
- The LLM converts the natural language query into a structured SQL query.  
- The SQL query is generated dynamically based on the database schema.  
- LangChain’s `SQLDatabaseChain` automates query construction and execution.  
- This allows non-technical users to query structured databases without writing SQL manually.

---

### 3️⃣ **Query Execution (Database Layer - MySQL)**
- The generated SQL query is executed against a MySQL database.
- The SQLAlchemy ORM (`get_db()`) manages database transactions, ensuring efficient data retrieval.
- The database returns structured results containing relevant outlet information.

---

### 4️⃣ **Answer Generation (LLM + Response Formatting)**
- The LLM formats the raw database results into a human-friendly response.
- The raw database results are formatted into a human-friendly response.
