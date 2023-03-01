from flask import Flask, request, abort, render_template
import os
import openai
import article_parser


openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        result = ""
        title = ""
        try:
            title, content = article_parser.parse(
                url=message, output='markdown', timeout=5)
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Summarize this for a college student:\n\n{content}",
                temperature=0.7,
                max_tokens=64,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            result = response["choices"][0]["text"]

        except:
            result = "invalid URL"

    return render_template('home.html', news_title=title,  message=result)


if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/", methods=['GET'])
# def home():
#     return 'Hello World'


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8080)
