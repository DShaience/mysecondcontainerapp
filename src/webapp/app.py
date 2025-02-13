import base64
import datetime as dt
import json
import logging
import os
from io import BytesIO
import sys
sys.path.append(os.getcwd())  # workaround for now
import streamlit as st

from utils.consts import PROMPT
from joke_meal_class import JokeMeal

import pandas as pd
from PIL import Image


# https://github.com/PablocFonseca/streamlit-aggrid/blob/main/st_aggrid/__init__.py
# https://github.com/PablocFonseca/streamlit-aggrid/blob/main/st_aggrid/AgGridReturn.py
# https://github.com/PablocFonseca/streamlit-aggrid/blob/main/st_aggrid/grid_options_builder.py


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

LLM_CONFIG_PATH = 'webapp/llm_config.json'
AUTHOR_NAME = "Chuck Norris"
HOMEPAGE = "https://chucknorris.com"


def st_meal_inference(uploaded_file):
    llm_config = json.load(open(LLM_CONFIG_PATH))
    prompt = PROMPT

    chat_meal = JokeMeal(llm_config, prompt)
  
    logger.info(f"Reading image data.")
    image = uploaded_file.read()
    image_base64 = base64.b64encode(image).decode('utf-8')

    result = chat_meal.infer(image_base64)
    logger.debug(f"RESULTS TO DEBUG: {result}")  

    print(result)
    parsed_results = result

    logger.info(f"Parsing complete.")  
    return parsed_results  


def app():
    st.set_page_config(
        page_title="DadJokerAI",
        page_icon="🍔",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    homepage = HOMEPAGE
    st._is_running_with_streamlit = True  # Set a flag for Streamlit compatibility
    st.title('DadJokerAI Incorrigeble Dad-Joker')
    st.write(f"This site is developed and maintained by [{AUTHOR_NAME}]({homepage})")

    st.markdown(f"""
    Feel free to reach out or ping me on <a href="{homepage}">my homepage</a>! 🚀""", unsafe_allow_html=True)

    logger.info("DadJokerAI App Started")
    col1, col2, col3 = st.columns([3, 1, 1])
    
    # Adjust the file uploader width in the second column
    with col1:
        uploaded_file = st.file_uploader("Upload a file", type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'heic', 'heif'], 
                                        accept_multiple_files=False, label_visibility="collapsed")
        
        # subcol1, subcol2, = st.columns([1, 3])

        # Check if new files are uploaded
        if uploaded_file:
            logger.info(f"Processing file {uploaded_file.name}")
            parsed_results = st_meal_inference(uploaded_file)

            logger.info(f"Parsing complete.")
            st.session_state.inference_done = True

        # Add a Help button
        if 'show_help' not in st.session_state:
            st.session_state.show_help = False

        if st.button('Help'):
            st.session_state.show_help = not st.session_state.show_help

        if st.session_state.show_help:
            st.markdown("""
            ### Help Information
            - **Upload a file**: You can upload an images of your meal, and DadJokerAI will generate a dad-joke based on the meal or the eater.""")

if __name__ == '__main__':
    app()


