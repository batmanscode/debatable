from simpleaichat import AIChat
import ast


# agent
personality = """You're an award winning expert sales agent.
Identify and address the sales objections in the emails given to you.
You always keep things simple and concise"""


# an expert guide was written by AI after combining 3 guides
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


# cam's notes
# [18/12, 7:46 pm] Cameron Dower: they are longer yes, but adding things at the start like "I totally understand your concern" or "yes I agree, you should speak to your boss....."
# [18/12, 7:46 pm] Cameron Dower: ^ these are great sales techniqies
cams_notes = """**Notes**
-  sometimes adding things at the start like "I totally understand your concern" or "yes I agree, you should speak to your boss" are great sales techniques"""


ai = AIChat(
    console=True,
    save_messages=False,  # with schema I/O, messages are never saved
    # model="gpt-3.5-turbo-0613",
    # model="gpt-4-1106-preview",
    model="gpt-4",
    params={"temperature": 0.2},
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

    Helpful notes:
    {cams_notes}

    For each of the objections, suggest responses to handle them (more than one suggestion is ok but maximum four). Never make up or assume anything.
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
