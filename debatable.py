from simpleaichat import AIChat
import ast
import streamlit as st
import asyncio
import time

from db_utils import get_categories, save_categories


# agent
personality = """You're an award winning expert sales agent.
Identify and address the sales objections in the emails given to you.
You always keep things simple and concise"""


# an expert guide was written by AI after combining 3 guides using another project
# https://bamf.com/how-to-conquer-sales-objections-15-script-examples/
# https://www.reddit.com/r/sales/comments/jpe5zb/objectionhandling_cheat_sheet_the_15_top/
# https://mailshake.com/blog/sales-objections-2/
expert_guide = """**The Expert's Guide to Mastering Sales Objections**

1. **Embrace Objections**: View objections as opportunities to deepen understanding and refine your approach.

2. **Listen Fully**: Hear out concerns without interruption, anticipating potential objections.

3. **Clarify and Understand**: Paraphrase objections to ensure comprehension and uncover underlying issues.

4. **Acknowledge and Respond**: Validate concerns and address them with authority or propose a follow-up.

5. **Confirm Resolution**: Verify that overcoming the objection will lead to a commitment.

6. **Educate and Inform**: Use objections to underscore the unique value and benefits of your product.

7. **Be Honest and Transparent**: If unsure, admit it and pledge to provide answers posthaste.

8. **Provide Evidence**: Support your responses with concrete data, case studies, and testimonials.

9. **Stay Positive**: Keep the conversation constructive and focused on problem-solving.

10. **Know When to Walk Away**: Recognize when an objection indicates a poor fit and disengage gracefully.

11. **Keep Learning**: Continuously refine your sales techniques based on objection handling experiences."""


boss_notes = """**Notes**
- sometimes adding things at the start like "I totally understand your concern" or "yes I agree, you should speak to your boss" are great sales techniques
- move on if customer made clear they don't want or are angry"""

MODEL = "gpt-4o"
TEMP = 0.2

ai = AIChat(
    console=True,
    save_messages=False,  # with schema I/O, messages are never saved
    model=MODEL,
    params={"temperature": TEMP},
    system=personality,
)


def identify_objections(email):
    """Identify sales objections from the given email"""

    objections_prompt = f"""Identify sales objections from the following customer email:
    {email}

    Your identified objections as bullet points:"""

    objections = ai(objections_prompt)

    return objections


def generate_responses(email, product_context, objections):
    """Generate responses to the given email and product context"""

    if product_context is None:
        product_context = "none"

    full_prompt = f"""Identify sales objections from the following customer email:
    {email}

    Your identified objections as bullet points:
    {objections}

    Product info:
    {product_context}

    ONLY IF you need any help, please refer to the guide below:
    {expert_guide}

    Notes from boss:
    {boss_notes}

    For each of the objections, suggest responses to handle them (more than one suggestion is ok but maximum four). Never make up or assume anything.
    Your output MUST ONLY be a dict where each key is an objection and it's value is a list with all the suggestions.

    your output as dict WITHOUT syntax highlighting:"""

    suggestions = ai(full_prompt)

    return suggestions


async def complete_suggestions(email, product_context) -> dict:
    """
    combine the two functions above, `identify_objections` and `generate_responses`
    then format the output string into a dict
    """

    # identify objections
    objections = identify_objections(email)

    # generate responses
    suggestions = generate_responses(email, product_context, objections=objections)

    # format the output string into a dict
    suggestions = ast.literal_eval(suggestions)

    return suggestions


# placeholders for the input boxes
PRODUCT_CONTEXT_PLACEHOLDER = """I sell CRM software for small businesses.
It helps small businesses organise all of their data and customers in one central place, allowing them to streamline business operations, increase revenue per customer, and build stronger brand connection between them and their customers.
It has a free forever plan but also has 2 tiers, one being $35 per month and the other being $100 per month."""

EMAIL_PLACEHOLDER = """Hi Sarah, thanks for reaching out. 

CRM sounds interesting but I'm not sure this is really what we need right now. We already know a lot of our customers by name and, for the price you're charging, it seems a little expensive. 

Maybe I'm not understanding the value of the tool but I don't see a truly compelling reason as to why we need this tool. 

Thanks but I'm not sure this is the right fit. 
Robert"""


async def categorise_input(email, product_context, key):
    "categorises input by industry"

    prompt = f"""Categorise the following for data organisation purposes:

Product context:
{product_context}

Email:
{email}


Output MUST be a lowercase string where each tag/category is comma separated.
Keep things extremely concise and PRECISE as possible. One to four words per tag. Fewer the better.
Example: real estate, finance, insurance, health, education, etc
If there's more than one cagetory, incl them as well. Example: "real estate, insurance" for a real estate insurance company
The industry is important.
Unless it's about the product itself NEVER use "sales objections" as a category because its obvious since that's your job.

These are existing problem tags: {get_categories(key=key)}

Reuse similar tags

categories:"""

    categories = ai(prompt)

    # str to list
    # remove leading and trailing spaces
    # remove double, single quotes and underscores
    categories_list = [item.strip().replace('"', '').replace("'", '').replace('_', ' ') for item in categories.split(",")]

    # append "example" if email and product_context are the same as the placeholders
    if email == EMAIL_PLACEHOLDER and product_context == PRODUCT_CONTEXT_PLACEHOLDER:
        categories_list.append("example")

    # save categories to db
    save_categories(categories=categories_list, key=key)
    print(categories_list)

    # return "categories saved"
    return categories_list


async def get_suggestions_and_categorise(email, product_context, key):
    """
    combine the two functions above in async, `complete_suggestions` and `categorise_input`
    """

    start_time = time.time()

    suggestions, _ = await asyncio.gather(
        complete_suggestions(email, product_context),
        categorise_input(email, product_context,key=key),
    )
    
    end_time = time.time()

    st.toast(f"That took {end_time - start_time:.2f} seconds, thanks for waiting!", icon="🙏🏻")

    print("suggestions generated and categorised")

    return suggestions
