from flask import Flask, redirect, render_template, request, flash, url_for
from langdetect import detect, detect_langs, LangDetectException
from googletrans import LANGUAGES, Translator

users = {}

app = Flask(__name__,template_folder='templates')
app.secret_key = 'qwertyuiop1234567890'

@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return render_template('home.html', languages=LANGUAGES, username=username)
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Username already exists')
        else:
            users[username] = password
            flash('Registration successful')
            return redirect(url_for('login'))  # Redirect to login page after successful registration
    else:
        return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle form submission
        text = request.form['text']
        dest_lang = request.form['dest_lang']
        lang = detect(text)

        # Get full language name of detected language
        try:
            detected_langs = detect_langs(text)
            detected_lang = detected_langs[0].lang
            lang = LANGUAGES[detected_lang]
        except LangDetectException:
            pass

        translator = Translator()
        translation = translator.translate(text, dest=dest_lang).text
        return render_template('home.html', text=text, lang=lang, translation=translation, languages=LANGUAGES)
    else:
        # Render the home page
        return render_template('home.html', languages=LANGUAGES)

if __name__ == '__main__':
    app.run(debug=True)
