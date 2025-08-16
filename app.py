from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GROQ_API_KEY = "GROQ_API_KEY"  # Replace with your Groq API key 

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Groq OpenAI-compatible endpoint

def ai_generate_response(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3-70b-8192",  # Change model as needed
        "messages": [
            {"role": "system", "content": "You are an AI Assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }
    response = requests.post(GROQ_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    feedback = ""
    if request.method == "POST":
        task = request.form.get("task", "")
        user_input = request.form.get("user_input", "")

        if task == "qa":
            prompt = f"Answer the following question clearly:\n{user_input}"
        elif task == "summary":
            prompt = f"Summarize the following text in 3-4 sentences:\n{user_input}"
        elif task == "creative":
            prompt = f"Be creative! {user_input}"
        else:
            prompt = "Invalid option."

        try:
            result = ai_generate_response(prompt)
        except Exception as e:
            result = f"Error: {str(e)}"

        if "feedback" in request.form:
            fb = request.form["feedback"]
            with open("feedback_log.txt", "a", encoding="utf-8") as f:
                f.write(f"User Query: {user_input}\nAI Response: {result}\nFeedback: {fb}\n\n")
            feedback = "Thanks for your feedback!"

    return render_template("index.html", result=result, feedback=feedback)


if __name__ == "__main__":
    app.run(debug=True)
