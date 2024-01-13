# Run the API server with: uvicorn api:app --reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

from debatable import get_suggestions_and_categorise, MODEL, TEMP, EMAIL_PLACEHOLDER, PRODUCT_CONTEXT_PLACEHOLDER
from db_utils import save_metadata, save_all_except_feedback_and_metadata, create_key


description = """ ## This is a prototype API for Debatable. It is not intended for production use.
args:
- **email**: The email you want to get suggestions for.

- **product_context**: The product context you want to get suggestions for.

<details>
<summary>Example request in javascript</summary>
```javascript
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
    "email": "",
    "product_context": "",
    });

var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
};

fetch("http://<your-api-url>/suggest/", requestOptions)
    .then(response => response.json())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));
```
</details>

<details>
<summary>Example request in curl</summary>
```bash
curl --location --request POST 'http://<your-api-url>/suggest/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "",
    "product_context": ""
}'
```
</details>

<details>
<summary>Example request in python</summary>
```python
import requests
import json

url = "http://<your-api-url>/suggest/"

payload = json.dumps({
    "email": "",
    "product_context": ""
    })

headers = {
    'Content-Type': 'application/json'
    }

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
</details>
"""

app = FastAPI(
    title="Debatable API",
    description=description,
    version="0.1.0",
)

@app.get("/")
def root():
    return "welcome to the debatable api! :) Add /docs to the URL to see Swagger docs or /redoc to see ReDoc docs."

class EmailContext(BaseModel):
    email: str = EMAIL_PLACEHOLDER
    product_context: str = PRODUCT_CONTEXT_PLACEHOLDER

@app.post("/suggest/")
def get_suggestions(email_context: EmailContext):
    try:
        # suggestions = complete_suggestions(email_context.email, email_context.product_context)

        key = create_key()

        save_metadata(
            key=key,
            temperature=TEMP,
            model=MODEL,
        )

        suggestions = asyncio.run(
            get_suggestions_and_categorise(
                email=email_context.email,
                product_context=email_context.product_context,
                key=key
                )
                )

        # save the email and product context to the database
        # save_all_except_feedback(
        #     product_context=email_context.product_context,
        #     email_text=email_context.email,
        #     output_dict=suggestions,
        #     key=create_key(),
        #     model=MODEL,
        #     usage_source="api",
        # )
        save_all_except_feedback_and_metadata(
            product_context=email_context.product_context,
            email_text=email_context.email,
            output_dict=suggestions,
            key=key,
            usage_source="api",
        )
        
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

# Note: You will need to add 'fastapi' and 'pydantic' to your requirements.txt
# and run the FastAPI server to use this API.
