import streamlit as st

from debatable import complete_suggestions


st.set_page_config(page_title="Debatable", page_icon="💡", initial_sidebar_state="auto", layout="wide")

st.title("Debatable 💡")
# st.write(
#     """
#     #### **:blue[Talk about your bra problems, see what issues other people have and run surveys for your bra ideas!]**


#     How to use:
#     1. Have a chat 💬 :grey[- the bot will let you know when it's done but if it's taking too long, just say end the convo]
#     2. Please wait while your report is being generated ❤️ :grey[- under 10 seconds ⏲]
#     2. Check the sidebar (top left) to see the report 📋 :grey[- the bot will tell you when it's written!]
#     3. Leave a rating ⭐️
#     4. See the stats page to see things like the most common problems and frequently mentioned brands 🔍
#     """
# )
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


# nice big button
if st.button("Get Suggestions", type="primary", use_container_width=True):
    # run the model
    with st.spinner("Generating suggestions..."):
        # st.write("hi :3")
        dict_output = complete_suggestions(email, product_context)

        # st.write(f"**Email**: \n{email}\n\n")
        # st.write(f"*Product Info*: \n\n{product_context}\n\n")

        # st.write("## Response")

        for objection, suggestions in dict_output.items():
            st.write(f":blue[objection:] \n**{objection}**")
            st.write(":blue[suggestions:]")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
            st.write("---")
