import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Create OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("WARNING: OPENAI_API_KEY is not configured")

client = OpenAI(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Agent</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
            }

            h1 {
                text-align: center;
            }

            textarea {
                width: 100%;
                height: 120px;
                padding: 10px;
                font-size: 16px;
                box-sizing: border-box;
            }

            button {
                margin-top: 10px;
                padding: 12px 25px;
                font-size: 16px;
                cursor: pointer;
            }

            #response {
                margin-top: 20px;
                padding: 15px;
                background: #f2f2f2;
                border-radius: 5px;
                min-height: 50px;
                white-space: pre-wrap;
            }
        </style>
    </head>

    <body>

        <h1>🤖 AI Agent</h1>

        <textarea id="message"
                  placeholder="Ask something..."></textarea>

        <br>

        <button onclick="askAI()">Ask AI</button>

        <div id="response">
            AI response will appear here...
        </div>

        <script>
            async function askAI() {

                const message =
                    document.getElementById("message").value;

                if (!message.trim()) {
                    alert("Please enter a question.");
                    return;
                }

                document.getElementById("response").innerText =
                    "Thinking...";

                try {

                    const response = await fetch("/ask", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            message: message
                        })
                    });

                    const data = await response.json();

                    if (data.error) {
                        document.getElementById("response").innerText =
                            "AI service error: " + data.error;
                    } else {
                        document.getElementById("response").innerText =
                            data.response;
                    }

                } catch (error) {

                    document.getElementById("response").innerText =
                        "Error connecting to AI service: " + error;

                }
            }
        </script>

    </body>
    </html>
    """


@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({
                "error": "Message is required"
            }), 400

        user_message = data["message"]

        if not client:
            return jsonify({
                "error": "OPENAI_API_KEY is not configured"
            }), 500

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        return jsonify({
            "response": answer
        })

    except Exception as e:

        print("AI Error:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))

    app.run(
        host="0.0.0.0",
        port=port
    )
