import streamlit as st
import asyncio

from debatable import complete_suggestions, categorise_input, get_suggestions_and_categorise, TEMP, MODEL, PRODUCT_CONTEXT_PLACEHOLDER, EMAIL_PLACEHOLDER
from db_utils import save_all_except_feedback, save_feedback_and_rating, create_key, get_count, contact_form, save_all_except_feedback_and_metadata, save_metadata


st.set_page_config(
    page_title="Debatable", page_icon="💡", initial_sidebar_state="auto", layout="wide"
)

st.title("Debatable 💡")

col1, col2 = st.columns([2, 1])
col1.write(
    """
    #### **:blue[Get expert responses to common objections that salespeople experience on their sales calls / conversations]**


    How to use:
    1. Paste your email/objection from the customer 📧
    2. Provide product context (What do you sell? Who is it for? Why is it good? etc.) 📦
    3. Get suggested responses 😊
    """
)
# show how many times the get suggestions button has been used
col2.metric(label="Times Used 🔢", value=get_count())

st.warning("This is an early prototype - apologies if we are a little slow sometimes.")
st.info("API available at https://debatable-api.onrender.com/")

st.markdown("---")


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
    product_context = st.text_area(
        "Product Context",
        placeholder=f"[Optional but recommended]\n{PRODUCT_CONTEXT_PLACEHOLDER}",
        height=200,
        value=st.session_state["product_context_placeholder"],
    )

with col2:
    # st.write("Email")
    email = st.text_area(
        "Email",
        placeholder=EMAIL_PLACEHOLDER,
        height=200,
        value=st.session_state["email_placeholder"],
    )


# keep showing text when page gets rerun after saving feedback
if "dict_output" not in st.session_state:
    st.session_state.dict_output = {}

# nice big button
if st.button("Get Suggestions", type="primary", use_container_width=True):
    # run the model
    with st.spinner("Generating suggestions..."):
        # st.write("hi :3")
        # st.session_state.dict_output = complete_suggestions(email, product_context)

        # save input and output to db

        # generate key for this ouput, save it to the session state
        # and use it later to add feedback and/or rating to the same entry
        # each output will have its own key
        # if "key" not in st.session_state:
        st.session_state.key = create_key()

        save_metadata(
            key=st.session_state.key,
            temperature=TEMP,
            model=MODEL,
        )

        # needs key so moved after create_key()
        st.session_state.dict_output = asyncio.run(get_suggestions_and_categorise(email, product_context, key=st.session_state.key))

        # save_all_except_feedback(
        #     product_context=product_context,
        #     email_text=email,
        #     output_dict=st.session_state.dict_output,
        #     key=st.session_state.key,
        #     model=MODEL,
        #     usage_source="streamlit",
        # )
        save_all_except_feedback_and_metadata(
            product_context=product_context,
            email_text=email,
            output_dict=st.session_state.dict_output,
            key=st.session_state.key,
            usage_source="streamlit",
        )

        # st.write(f"**Email**: \n{email}\n\n")
        # st.write(f"*Product Info*: \n\n{product_context}\n\n")

        # st.write("## Response")

# only show the output if there's something to show
if st.session_state.dict_output:
    for objection, suggestions in st.session_state.dict_output.items():
        st.write(f":blue[objection:] \n**{objection}**")
        st.write(":blue[suggestions:]")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")
        st.write("---")

    # rating and feedback
    with st.form("rating", border=False):
        # st.write("Rate and leave feedback")

        def format_rating(rating: int):
            "shows the 1-5 rating as emoji faces for the user"

            if rating == 1:
                return "😞"
            elif rating == 2:
                return "🙁"
            elif rating == 3:
                return "😐"
            elif rating == 4:
                return "🙂"
            elif rating == 5:
                return "😃"

        col1, col2 = st.columns(2)

        with col1:
            rating = st.radio(
                label="You're part of our early beta so any feedback you have is incredibly valuable",
                # label_visibility="collapsed",
                options=(1, 2, 3, 4, 5),
                horizontal=True,
                format_func=format_rating,
                index=4,
            )

        with col1:
            feedback = st.text_input(
                "feedback",
                label_visibility="collapsed",
                placeholder="[Optional] What did you think?",
            )

        submitted = st.form_submit_button("Save Feedback")

        if submitted:
            with st.spinner("Saving feedback..."):
                # save_all(
                #     product_context=product_context,
                #     email_text=email,
                #     output_dict=st.session_state.dict_output,
                #     rating=rating,
                #     feedback=feedback,
                # )
                save_feedback_and_rating(
                    feedback=feedback,
                    rating=rating,
                    key=st.session_state.key,
                )

                st.toast("Thank you for your feedback ❤️")

# contact form
with st.expander("Contact Us"):
    with st.form("contact_form"):
        # st.write("## Contact")
        # st.write("If you have any questions or feedback, please get in touch")
        email = st.text_input("Email", placeholder="you@example.com")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send", type="primary")

        if submitted:
            # check if everything is filled in
            if not email or not subject or not message:
                st.error("Please fill in all fields")
            # now check that email is valid
            elif not "@" in email:
                st.error("Please enter a valid email address")
            else:
                with st.spinner("Sending message..."):
                    # save to db
                    # contact_form(email, message, subject)
                    contact_form(email, message, subject)
                    st.success("Message sent! 🎉")
                    st.success("We'll get back to you as soon as possible")
