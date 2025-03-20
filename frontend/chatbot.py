import streamlit as st
import requests
import folium
import os
from streamlit_folium import folium_static
from geopy.distance import geodesic
from folium import CustomIcon

# ✅ FastAPI Backend URLs
FASTAPI_QUERY_URL = "http://127.0.0.1:8000/query"
FASTAPI_OUTLETS_URL = "http://127.0.0.1:8000/outlets"

# ✅ Subway Custom Marker Path
ICON_PATH = os.path.join(os.getcwd(), "subway-marker.png")  # Ensure this file exists
ICON_SIZE = (20, 30)  # Adjust marker size if needed

# ✅ Streamlit App Configuration
st.set_page_config(page_title="Subway KL Chatbot", page_icon="🥪", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center; margin-top: -50px; margin-bottom: 20px;'>Subway Kuala Lumpur Directory</h1>
    """,
    unsafe_allow_html=True
)

# ✅ Two-column layout (Chatbot Left, Map Right)
col1, col2 = st.columns([2, 2])  # Adjust the ratio if needed

# ✅ Chatbot Section (Left Side)
with col1:
    # ✅ Centered Welcome Message
    st.markdown(
        """
        <h3 style='text-align: center; font-size: 25px;'>Welcome to Subway Chat🤖!</h3>
        <p style='text-align: center; font-size: 14px;'>Ask me anything about Subway outlets in Kuala Lumpur!</p>
        """,
        unsafe_allow_html=True
    )

    # ✅ Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ✅ Scrollable Chat History with Messages INSIDE the Container
    chat_container = st.container(height=400)  # ✅ Ensures messages are inside the scrollable area

    with chat_container:
        st.markdown(
            """
            <style>
                .chat-container {
                    max-height: 50vh;  /* Fixed chat height */
                    overflow-y: auto;  /* Enables scrolling */
                    display: flex;
                    flex-direction: column-reverse;  /* Keeps latest messages at the bottom */
                }
            </style>
            <div class="chat-container" id="chat-box">
            """,
            unsafe_allow_html=True
        )

        # ✅ Display Messages (ENSURE They Appear Inside)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"], unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # ✅ Close chat container

    # ✅ JavaScript to Auto-Scroll to Bottom on New Messages
    st.markdown(
        """
        <script>
            setTimeout(function() {
                var chatBox = document.getElementById("chat-box");
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 100);
        </script>
        """,
        unsafe_allow_html=True
    )

    # ✅ Static Input Box (ALWAYS Stays at the Bottom)
    user_input = st.chat_input("Type your question here...", key="unique_chat_input")

    if user_input:
        # ✅ Append User Message FIRST
        st.session_state.messages.append({"role": "user", "content": user_input})

        # ✅ Call FastAPI to Get Response
        try:
            response = requests.post(FASTAPI_QUERY_URL, json={"question": user_input})
            response_json = response.json()
            chatbot_response = response_json.get("summary", "⚠️ Sorry, I couldn't find an answer to that.")
        except requests.exceptions.RequestException as e:
            chatbot_response = f"🚨 **API Connection Error:** {e}"

        # ✅ Append Assistant Response AFTER User Query
        st.session_state.messages.append({"role": "assistant", "content": chatbot_response})

        # ✅ Rerun to Refresh Chat Box
        st.rerun()


        
# ✅ Fetch Subway Outlets Data from API
@st.cache_data
def get_outlets():
    """Fetch Subway outlets' coordinates from FastAPI."""
    try:
        response = requests.get(FASTAPI_OUTLETS_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Subway outlet data: {e}")
        return []

@st.cache_data(ttl=0, max_entries=1)
def get_fresh_data():
    return None  # Forces cache to clear
get_fresh_data()

outlets = get_outlets()

# ✅ Map Section (Right Side)
with col2:
    st.markdown(
        """
        <div style="text-align: center;">
            <h3 style='font-size: 25px;'>KL Subway Outlets Map🥪</h3>
            <p style="font-size: 12px; margin-top: -10px;">
                <span style="color:#028940; font-weight:bold;">🟢 Green Circle</span> – Represents the 5KM service area around each Subway outlet.
            </p>
            <p style="font-size: 12px; margin-top: -10px;">
                <span style="color:#FFC20D; font-weight:bold;">🟡 Yellow Overlay</span> – Indicates locations where multiple outlets’ 5KM service areas overlap.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    if outlets:
        # ✅ Set the first outlet as the map center
        first_outlet = outlets[0]
        map_center = [first_outlet["latitude"], first_outlet["longitude"]]
        m = folium.Map(location=map_center, zoom_start=11)  # Reduce zoom for better visibility

        # ✅ Function to check if two outlets are within 5KM radius
        def is_within_radius(outlet1, outlet2, radius_km=5):
            return geodesic(
                (outlet1["latitude"], outlet1["longitude"]),
                (outlet2["latitude"], outlet2["longitude"])
            ).km <= radius_km

        # ✅ Track overlapping outlets
        overlapping_outlets = set()

        # ✅ Plot Subway Outlets with Custom Markers and 5KM Catchment
        for outlet in outlets:
            folium.Marker(
                location=[outlet["latitude"], outlet["longitude"]],
                popup=f"<b>{outlet['name']}</b><br>{outlet['address']}",
                tooltip=outlet["name"],
                icon=CustomIcon(ICON_PATH, icon_size=ICON_SIZE)  # Use Subway marker
            ).add_to(m)

            # ✅ Add 5KM Radius Catchment 
            folium.Circle(
                location=[outlet["latitude"], outlet["longitude"]],
                radius=5000,  # 5KM radius
                color="#028940",
                fill=True,
                fill_color="#028940",
                weight=8,
                fill_opacity=0.3  # Reduce opacity for better visualization
            ).add_to(m)

        # ✅ Highlight Outlets with Overlapping 5KM Radius
        for i, outlet1 in enumerate(outlets):
            for j, outlet2 in enumerate(outlets):
                if i != j and is_within_radius(outlet1, outlet2):
                    overlapping_outlets.add((outlet1["latitude"], outlet1["longitude"]))

        # ✅ Draw a **subtle yellow border** for overlapping areas
        for lat, lon in overlapping_outlets:
            folium.Circle(
                location=[lat, lon],
                radius=5000,
                color="#FFC20D",  # Yellow for less distraction
                fill=True,
                fill_color="#FFC20D",
                fill_opacity=0.07,  # More transparent fill
                weight=1.5,  # Thin border
            ).add_to(m)

        folium_static(m, width=600, height=445)
        st.markdown("</div>", unsafe_allow_html=True)  # Close the center alignment div
