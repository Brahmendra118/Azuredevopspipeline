from flask import Flask, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    response = ""

    if request.method == "POST":

        user_text = request.form.get("text")

        if user_text:

            try:
                api_key = os.getenv("OPENAI_API_KEY")

                if not api_key:
                    response = "OpenAI API key is not configured."
                else:
                    Client = OpenAI(api_key=api_key)
                    
                completion = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant."
                        },
                        {
                            "role": "user",
                            "content": user_text
                        }
                    ]
                )

                response = completion.choices[0].message.content

            except Exception as e:
                response = f"AI service error: {str(e)}"

    return render_template(
        "index.html",
        response=response
    )


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )