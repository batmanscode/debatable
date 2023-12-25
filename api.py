from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from debatable import complete_suggestions

app = FastAPI()

class EmailContext(BaseModel):
    email: str
    product_context: str

@app.post("/complete-suggestions/")
def get_complete_suggestions(email_context: EmailContext):
    try:
        suggestions = complete_suggestions(email_context.email, email_context.product_context)
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Note: You will need to add 'fastapi' and 'pydantic' to your requirements.txt
# and run the FastAPI server to use this API.
