from flask import Flask, render_template, Response, request
from threading import Thread
import server

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

@app.route('/liveCam01')
def liveCam01():
    return Response(server.tcpSocketAccept('',8485), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/getRobotData', methods=['POST'])
def getRobotData():
    if request.method == "POST":
        jsonData = request.get_json()
        print(jsonData)
    return ''


if __name__ == '__main__':
    app.run(host="127.0.0.1", port ="5050", debug=True)
    