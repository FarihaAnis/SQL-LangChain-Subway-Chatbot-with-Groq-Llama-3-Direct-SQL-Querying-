# Frontend Setup Guidelines
1. **Create chatbot.py**
    - This file serves as the frontend for the Subway KL chatbot using Streamlit.
2. **Install dependencies**
    - Refer to requirements.txt for the list of required packages.
3. **Define FastAPI backend URLs**
    - `POST /query` → Sends user questions to FastAPI.
    - `GET /outlets` → Fetches Subway outlet locations.
4. **Add custom Subway marker**
    - Ensure a `subway-marker.png` file exists in the same directory.
    - Define the icon size for display on the map.
5. **Setup Streamlit app configuration**
    - Configure the page title, icon, and layout to ensure proper UI setup.
6. **Create two-column layout**
    - Left Column: Chatbot interface for user interactions.
    - Right Column: Interactive Subway outlets map.
7. **Implement chatbot section**
    - Display a welcome message at the top.
    - Initialize and display chat history so users can see previous messages.
    - Use JavaScript auto-scroll to keep new messages visible at the bottom.
    - Provide a chat input box for user queries.
8. **Connect to FastAPI for responses**
    - Send user input to FastAPI's `/query` endpoint.
    - Receive and display responses in chat history.
    - Handle errors if the API is unreachable.
9. **Fetch Subway outlets data**
    - Use FastAPI’s /outlets endpoint to get outlet details.
    - Cache the data to improve performance and avoid redundant API calls.
10. **Implement interactive Subway map**
    - Use Folium to generate a dynamic map.
    - Mark Subway outlets with custom icons.
    - Draw 5KM radius circles around each outlet.
    - Highlight areas where multiple outlets overlap using a yellow overlay.
11. **Display the map in Streamlit**
    - Use `folium_static()` to render the interactive map inside Streamlit.
    - Adjust the map width and height for better visibility.
12. Run the Streamlit app
    - Start the frontend by running: `streamlit run chatbot.py`
    - This will open the chatbot interface in a browser.