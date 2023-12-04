import os
import streamlit as st
from trubrics.integrations.streamlit import FeedbackCollector
import ulid

from debatable import complete_suggestions


st.set_page_config(page_title="Debatable", page_icon="💡", initial_sidebar_state="auto", layout="wide")

st.title("Debatable 💡")
st.write(
    """
    #### **:blue[Get expert responses to any sales objections you get]**


    How to use:
    1. Paste your email/objection 📧
    2. Provide product context [optional] 📦
    3. Press the button and enjoy 😊
    """
)

st.markdown("---")

# placeholders for the input boxes
PRODUCT_CONTEXT_PLACEHOLDER = """An AI tool that suggests responses to sales objections in emails
- free trials allowed
- 14 day refunds
- accepting partnerships on a case by case basis"""

EMAIL_PLACEHOLDER = "I don't have this problem right now"


# use the placesholders as the autofill if people want to try it out
if "product_context_placeholder" not in st.session_state:
    st.session_state.product_context_placeholder = None

if "email_placeholder" not in st.session_state:
    st.session_state.email_placeholder = None

use_example = st.toggle("Autofill with example", value=False)

if use_example:
    st.session_state.product_context_placeholder = PRODUCT_CONTEXT_PLACEHOLDER
    st.session_state.email_placeholder = EMAIL_PLACEHOLDER
else:
    st.session_state.product_context_placeholder = None
    st.session_state.email_placeholder = None

col1, col2 = st.columns([1, 2])

with col1:
    # st.write("Product Context")
    product_context = st.text_area("Product Context", placeholder=PRODUCT_CONTEXT_PLACEHOLDER, height=200, value=st.session_state["product_context_placeholder"])

with col2:
    # st.write("Email")
    email = st.text_area("Email", placeholder=EMAIL_PLACEHOLDER, height=200, value=st.session_state["email_placeholder"])


#### SET UP FEEDBACK COLLECTION
# https://github.com/trubrics/streamlit-feedback
# https://trubrics.github.io/trubrics-sdk/integrations/streamlit

# create a session ID so feedback and prompts can be aggregated by each user or use of the app
if "session_ulid" not in st.session_state:
    st.session_state["session_ulid"] = ulid.new().str

# authenticate with trubrics
@st.cache_data
def init_trubrics(email, password):
    try:
        collector = FeedbackCollector(email=email, password=password, project="debatable_streamlit")
        return collector
    except Exception:
        st.error(f"Error authenticating '{email}' with [Trubrics](https://trubrics.streamlit.app/). Please try again.")
        st.stop()

collector = init_trubrics(email=os.environ["TRUBRICS_EMAIL"], password=os.environ["TRUBRICS_PASSWORD"])

# when there's multiple uses per session, this will keep track
if "feedback_key" not in st.session_state:
    st.session_state.feedback_key = 0

### END FEEDBACK COLLECTION SETUP


# keep showing text when page gets rerun after saving feedback
if "dict_output" not in st.session_state:
    st.session_state.dict_output = {}

# nice big button
if st.button("Get Suggestions", type="primary", use_container_width=True):
    # run the model
    with st.spinner("Generating suggestions..."):
        # st.write("hi :3")
        st.session_state.dict_output = complete_suggestions(email, product_context)
        st.session_state.feedback_key += 1

        # st.write(f"**Email**: \n{email}\n\n")
        # st.write(f"*Product Info*: \n\n{product_context}\n\n")

        # st.write("## Response")

for objection, suggestions in st.session_state.dict_output.items():
    st.write(f":blue[objection:] \n**{objection}**")
    st.write(":blue[suggestions:]")
    for suggestion in suggestions:
        st.write(f"- {suggestion}")
    st.write("---")


# rating
save_feedback = collector.st_feedback(
    component="default",
    feedback_type="faces",
    open_feedback_label="[Optional] Provide additional feedback",
    model="gpt-4-1106-preview",
    tags=["streamlit demo"],
    key=f"feedback_{st.session_state.feedback_key}",
    save_to_trubrics=True,
    user_id=str(st.session_state["session_ulid"]),
    success_fail_message=True
)
print(save_feedback)

        # # save prompt
        # save_prompt = collector.log_prompt(
        #     config_model={"model": "gpt-4-1106-preview", "temperature": 0.4},
        #     prompt=prompt,
        #     generation=answer,
        #     tags=["hierarchical agent with tools"],
        #     session_id=str(st.session_state["session_ulid"]),
        #     user_id=str(st.session_state["session_ulid"]), # user id is the same as session id because individual users aren't tracked
        # )        