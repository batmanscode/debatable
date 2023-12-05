"""
Database utils. Using Base by https://deta.space

docs: https://deta.space/docs/en/build/reference/sdk/base
"""

from datetime import datetime
from typing import List
from deta import Deta
import ulid


# auth
deta = Deta()  # DETA_PROJECT_KEY is in env
db = deta.Base("data")  # name of table
# db = deta.Base("test") # test table


def create_key() -> str:
    """
    Generate a new key for the db. Use once per entry
    """
    return str(ulid.new().str)


# def save_metadata(
#     prompt_template: str, model: str, temperature: float, system_message: str, key: str
# ) -> None:
#     """
#     Save model details and prompt template to the db
#     """

#     # save to db
#     output = db.put(
#         {
#             "prompt_template": prompt_template,
#             "model": model,
#             "temperature": temperature,
#             "system_message": system_message,
#             "key": key,
#             "date": datetime.now().strftime("%d-%m-%Y %H:00"),
#         }
#     )

#     return output


def save_metadata(key: str, model: str = "gpt-4-1106-preview", temperature: float = 0.4) -> None:
    """
    Save model details and prompt template to the db
    """

    # save to db
    output = db.put(
        {
            "model": model,
            "temperature": temperature,
            "key": key,
            "date": datetime.now().strftime("%d-%m-%Y %H:00"),
        }
    )

    return output


def save_input(product_context: str, email_text: str, key: str) -> None:
    """
    Save user input to the db
    """

    # the key would have been used to create an entry (in `save_metadata`) in the db already so the same should be used
    check = db.fetch({"key": key}).items

    if check:
        print("key exists, saving input")

        try:
            db.update(
                {
                    "input_product_context": product_context,
                    "input_email_text": email_text,
                },
                key=key,
            )
            print("input saved")

        except Exception as e:
            print("error saving input", e)

    else:
        raise ValueError("key does not exist, can't save input")


def save_output(output_dict: dict[str, List[str]], key: str) -> None:
    """
    Save model output to the db
    """

    # the key would have been used to create an entry (in `save_metadata`) in the db already so the same should be used
    check = db.fetch({"key": key}).items

    if check:
        print("key exists, saving output")

        try:
            db.update(
                {
                    "output_dict": output_dict,
                },
                key=key,
            )
            print("output saved")

        except Exception as e:
            print("error saving output", e)

    else:
        raise ValueError("key does not exist, can't save output")


def get_output_dict(key: str) -> dict or None:
    """
    Get model output from the db
    """

    # get from db
    output = db.fetch({"key": key}).items

    if output:
        return output[0]["output_dict"]
    else:
        print("key doesn't exist, can't get output")
        return None


def save_rating(rating: int, key: str) -> None:
    """
    Save user rating to the db after checking that the output exists
    """

    # the key would have been used to create an entry (in `save_metadata`) in the db already so the same should be used
    check = db.fetch({"key": key}).items

    if check:
        print("key exists, saving rating")

        if get_output_dict(key=key):
            print("output exists, saving rating for it")

            try:
                db.update(
                    {
                        "rating": rating,
                    },
                    key=key,
                )
                print("rating saved")

            except Exception as e:
                print("error saving rating", e)

        else:
            raise ValueError("output doesn't exist, can't save rating for it")

    else:
        print("key does not exist, can't save rating")


def save_feedback(feedback: str or None, key: str) -> None:
    """
    Save user feedback to the db after checking that the output exists
    """

    # the key would have been used to create an entry (in `save_metadata`) in the db already so the same should be used
    check = db.fetch({"key": key}).items

    if check:
        print("key exists, saving feedback")

        if get_output_dict(key=key):
            print("output exists, saving feedback for it")

            try:
                db.update(
                    {
                        "feedback": feedback,
                    },
                    key=key,
                )
                print("feedback saved")

            except Exception as e:
                print("error saving feedback", e)

        else:
            raise ValueError("output doesn't exist, can't save feedback for it")

    else:
        print("key does not exist, can't save feedback")


def save_all(
    product_context: str,
    email_text: str,
    output_dict: dict[str, List[str]],
    rating: int,
    feedback: str or None,
    key: str = create_key(),
    model: str = "gpt-4-1106-preview",
    temperature: float = 0.4,
) -> None:
    """
    Save all data to the db. this is a convenience function to save everything at once
    """

    # save metadata
    save_metadata(key=key, model=model, temperature=temperature)

    # save input
    save_input(product_context=product_context, email_text=email_text, key=key)

    # save output
    save_output(output_dict=output_dict, key=key)

    # save rating
    save_rating(rating=rating, key=key)

    # save feedback
    save_feedback(feedback=feedback, key=key)

    print("inputs, outputs and feedback saved")