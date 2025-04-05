import streamlit as st
import requests
import base64

if 'search_results' not in st.session_state:
    st.session_state['search_results'] = {}
if 'search_completed' not in st.session_state:
    st.session_state['search_completed'] = False

FASTAPI_URL = "http://127.0.0.1:8000"

def go_to_home():
    st.session_state['route'] = 'home'

def clear_input():
    st.session_state["input_url"] = ""
    st.session_state['search_results'] = {}
    st.session_state['search_completed'] = False

def handle_save():
    if st.session_state["input_url"] and st.session_state['search_completed'] and st.session_state.get('search_results'):
        results = st.session_state['search_results']
        try:
            save_payload = {
                "url": st.session_state["input_url"],
                "category": results['category'],
                "summary": results['summary']
            }
            save_response = requests.post(f"{FASTAPI_URL}/save", json=save_payload)

            if save_response.status_code == 200:
                st.success("Successfully saved")
                clear_input()
            else:
                st.error(f"Error saving data. Status code: {save_response.status_code}")
        except requests.exceptions.ConnectionError as e:
            st.error(f"Error connecting to the save service: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during save: {e}")
    elif not st.session_state["input_url"]:
        st.warning("Please enter a link to save.")
    elif not st.session_state['search_completed']:
        st.warning("Please perform a search before saving.")

def handle_exit():
    if st.session_state['search_completed']:
        clear_input()
    else:
        st.warning("Please perform a search before exiting.")

def home_page():
    st.title("LinkScribe 🔎")
    st.write("Welcome to your web searcher.")
    search_input_text = st.text_input("Enter your web link below ", key="input_url", value=st.session_state.get("input_url", ""))
    search_button = st.button("Search")
    progress_text = "Processing... please wait"

    if search_button and search_input_text:
        st.session_state['search_completed'] = False
        st.session_state['search_results'] = {}
        with st.spinner(progress_text):
            try:
                response = requests.post(f"{FASTAPI_URL}/process_url", json={"url": search_input_text})
                response.raise_for_status()
                st.session_state['search_results'] = response.json()
                st.session_state['search_completed'] = True
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the backend: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    if st.session_state.get('search_completed') and st.session_state.get('search_results'):
        results = st.session_state['search_results']
        if results.get('error'):
            st.error(results['error'])
        else:
            with st.expander("Search Results", expanded=True):
                if results.get('image_base64'):
                    image_bytes = base64.b64decode(results['image_base64'])
                    st.image(image_bytes, caption="Page Preview", use_container_width=True)
                else:
                    st.info("No preview image could be loaded.")
                if results.get('category'):
                    st.write(f"**Category:** {results['category']}")
                if results.get('summary'):
                    st.write(f"**Summary:** {results['summary']}")

                col1_expander, col2_expander = st.columns(2)
                with col1_expander:
                    st.button("Save", disabled=not st.session_state['search_completed'], key="save_button_expander", on_click=handle_save)
                with col2_expander:
                    st.button("Exit", disabled=not st.session_state['search_completed'], key="exit_button_expander", on_click=handle_exit)

def data_page():
    st.title("Data storage 🗂️")
    st.write("Here you will find the previous searches for a specific link or keyword.")
    keyword = st.text_input("Please enter a keyword to search saved links or descriptions:")
    search_button = st.button("Search")

    if search_button and keyword:

        response = requests.get(f"{FASTAPI_URL}/search", {"keyword": keyword})
        response.raise_for_status()
        search_data = response.json()

        if search_data and search_data.get("results"):
            st.subheader("Search Results:")
            for item in search_data["results"]:
                st.markdown(f"**Link:** {item.get('url', 'N/A')}")
                st.write(f"**Category**:{item.get('category')}")
                st.write(f"**Description:** {item.get('summary', 'N/A')}")                
                st.markdown("---")

        else:
            st.info("No matching saved links or descriptions found.")
    elif search_button and not keyword:
        st.warning("Please enter a keyword to search.")
def about_page():
    st.write("Please use the following learn to learn about us..")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home 🏠", "Data 🔍", "About ❔"))

if page == "Home 🏠":
    home_page()
elif page == "Data 🔍":
    data_page()
elif page == "About ❔":
    about_page()