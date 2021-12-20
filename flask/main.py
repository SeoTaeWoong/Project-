from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/anomalyDetection')
def anomalyDetection():
    return render_template("anomalyDetection.html")

@app.route('/liveStreaming')
def liveStreaming():
    return render_template("liveStreaming.html")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port ="5050", debug=True)