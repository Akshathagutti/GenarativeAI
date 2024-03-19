from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from io import StringIO
import streamlit as st
from dotenv import load_dotenv
import time
import base64


#This function is typically used in Python to load environment variables from a .env file into the application's environment.
load_dotenv()

st.title("Let's do code review for your python code")
st.header("Please upload your .py file here:")


# Function to download text content as a file using Streamlit
def text_downloader(raw_text):
    # Generate a timestamp for the filename to ensure uniqueness
    timestr = time.strftime("%Y%m%d-%H%M%S")
    
    # Encode the raw text in base64 format for file download
    b64 = base64.b64encode(raw_text.encode()).decode()
    
    # Create a new filename with a timestamp
    new_filename = "code_review_analysis_file_{}_.txt".format(timestr)
    
    st.markdown("#### Download File ✅###")
    
    # Create an HTML link with the encoded content and filename for download
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    
    # Display the HTML link using Streamlit markdown
    st.markdown(href, unsafe_allow_html=True)

# Capture the .py file data
data = st.file_uploader("Upload python file",type=".py")

if data:

    # Create a StringIO object and initialize it with the decoded content of 'data'
    stringio = StringIO(data.getvalue().decode('utf-8'))

    # Read the content of the StringIO object and store it in the variable 'read_data'
    fetched_data = stringio.read()

    # Optionally, uncomment the following line to write the read data to the streamlit app
    st.write(fetched_data)

    # Initialize a ChatOpenAI instance with the specified model name "gpt-3.5-turbo" and a temperature of 0.9.
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

    # Create a SystemMessage instance with the specified content, providing information about the assistant's role.
    systemMessage = SystemMessage(content="You are a code review assistant. Provide detailed suggestions to improve the given Python code along by mentioning the existing code line by line with proper indent")

    # Create a HumanMessage instance with content read from some data source.
    humanMessage = HumanMessage(content=fetched_data)

    # Call the chat method of the ChatOpenAI instance, passing a list of messages containing the system and human messages.
    finalResponse = chat([systemMessage, humanMessage])

    
    #Display review comments
    st.markdown(finalResponse.content)


    text_downloader(finalResponse.content)

