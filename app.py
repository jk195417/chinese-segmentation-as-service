from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def root():
    return 'Chinese segmentation as service.'

if __name__ == "__main__":
    app.run('127.0.0.1', 3001)
