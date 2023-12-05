from simpleaichat import AIChat
import ast


# agent
personality="""You're an award winning expert SaaS sales agent.
Identify and address the sales objections in the emails given to you.
You always keep things simple and concise"""

ai = AIChat(
    console=True,
    save_messages=False,  # with schema I/O, messages are never saved
    # model="gpt-3.5-turbo-0613",
    model="gpt-4-1106-preview",
    params={"temperature": 0.4},
    system=personality
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

    For each of the objections, suggest responses to handle them (more than one suggestion is ok but maximum four).
    Your output MUST ONLY be a dict where each key is an objection and it's value is a list with all the suggestions.

    your output as dict WITHOUT syntax highlighting:"""

    suggestions = ai(full_prompt)

    return suggestions


def complete_suggestions(email, product_context):
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