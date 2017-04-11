from flask import Flask
app = Flask(__name__)

@app.route("/test", methods=['GET'])
def test():
    return "test....."

@app.route("/login")
def login(username, password):
    pass

@app.route("/upload", methods=['POST'])
def upload_image(image):
    pass

@app.route("/download", methods=['POST'])
def download_file(file_name):
    pass