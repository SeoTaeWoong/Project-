from flask import Flask, render_template, Response, request
from multiprocessing import Process, Queue
import socketClient as SocketCli

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
    return Response(getLiveCam01(), mimetype='multipart/x-mixed-replace; boundary=frame')

def getLiveCam01():
    while True:
        print(imgQueue1.qsize())
        if imgQueue1.qsize() != 0:
            print("cam1 입장")
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + imgQueue1.get() + b'\r\n')
        else :
            pass
            

@app.route('/liveCam02')
def liveCam02():
    return Response(getLiveCam02(), mimetype='multipart/x-mixed-replace; boundary=frame')

def getLiveCam02():
    while True:
        print(imgQueue1.qsize())
        if imgQueue2.qsize() != 0:
            print("cam2 입장")
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + imgQueue2.get() + b'\r\n')
        else :
            pass
                  

            

@app.route('/getRobotData', methods=['POST'])
def getRobotData():
    if request.method == "POST":
        jsonData = request.get_json()
        setDataQueue.put(jsonData)
        print(jsonData)
    return ''



if __name__ == '__main__':
    imgQueue1 = Queue()
    imgQueue2 = Queue()
    robotDataQueue = Queue()
    setDataQueue = Queue()

    sock = SocketCli.SocketClient()
    socket_process = Process(target=sock.clientON, args=(imgQueue1, imgQueue2, robotDataQueue, setDataQueue))
    socket_process.start()
    app.run(host="0.0.0.0", port ="80", debug=True)
    