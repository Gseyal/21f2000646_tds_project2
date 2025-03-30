import os
import json
from flask import Flask, request, render_template
import openai
from flask_cors import CORS

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    answer = None  # Initialize answer as None
    if request.method == "POST":
        # Get the question from the form
        question = request.form.get("question")
        file = request.files.get("file")

        if not question:
            return render_template("home.html", answer="Please provide a question.")

        # Read the file content if a file is uploaded
        file_content = ""
        if file:
            try:
                file_content = file.read().decode("utf-8")
            except Exception as e:
                return render_template("home.html", answer=f"Error reading file: {str(e)}")

        # Send the question and file content (if any) to ChatGPT API
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Question:'send only answer', {question}"}
            ]
            if file_content:
                messages.append({"role": "user", "content": f"File Content:\n{file_content}"})

            # Use the new OpenAI API interface
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )
            answer = response.choices[0].message["content"]
        except Exception as e:
            return render_template("home.html", answer=f"Error communicating with ChatGPT API: {str(e)}")

    # Render the home.html template with the answer
    return render_template("home.html", answer=answer)
@app.route("/api/", methods=["POST"])
def api():
    if request.method == "POST":
        # Get the question from the form
        question = request.form.get("question")
        file = request.files.get("file")

        if not question:
            return {"error": "Please provide a question."}, 400

        # Read the file content if a file is uploaded
        file_content = ""
        if file:
            try:
                file_content = file.read().decode("utf-8")
            except Exception as e:
                return {"error": f"Error reading file: {str(e)}"}, 400

        # Send the question and file content (if any) to ChatGPT API
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Question:'send only answer', {question}"}
            ]
            if file_content:
                messages.append({"role": "user", "content": f"File Content:\n{file_content}"})

            # Use the new OpenAI API interface
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )
            answer = response.choices[0].message["content"]
            return {"answer": answer}, 200
        except Exception as e:
            return {"error": f"Error communicating with ChatGPT API: {str(e)}"}, 500

    return {"error": "Invalid request method."}, 405
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))