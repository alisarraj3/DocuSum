from flask import Flask, render_template, redirect, flash, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import nlp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
ALLOWED_EXTENSIONS = {'pdf'}
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST']) # Home page
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            fs = nlp.FileSum(file)
            summary = fs.createSummary()
            return render_template('result.html', summary=summary)
        
    return render_template('home.html')









@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)




if __name__ == "__main__":
    app.run(port=8000, debug=True)