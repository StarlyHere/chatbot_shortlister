import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader



# Configure the API key
genai.configure(api_key=st.secrets["GEMINI_API"])


chat_model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me Anything"
        }
    ]

container = st.container()
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with container.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(query, uploaded_files=None):
    text = ""
    if uploaded_files:
        for uploaded_file in uploaded_files:
            reader = PdfReader(uploaded_file)
            text += "\n\n".join([page.extract_text() for page in reader.pages]) + "\n\n"
    response = chat.send_message(query + "\n\n" + text)

    # Displaying the Assistant Message
    with container.chat_message("assistant"):
        st.markdown(response.text)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # Storing the Assistant Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text
        }
    )

chat = chat_model.start_chat(history=[])

col1, col2 = st.columns((1, 4))

with col2:
    # Accept user input
    query = st.chat_input("What's up?")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
with col1:
    # Create a button for file upload
    st.button('Upload files', on_click=lambda: st.session_state.update(clicked=not(st.session_state.clicked)))
if st.session_state.clicked:
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
    st.session_state.uploaded_files = uploaded_files
    if uploaded_files:
        st.write("Uploaded files")
        st.session_state.clicked = False

if query:
    # Displaying the User Message
    with container.chat_message("user"):
        st.markdown(query)

    llm_function(query, st.session_state.get('uploaded_files', None))
