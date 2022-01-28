from flask import Flask, render_template, Response, request
from multiprocessing import Process, Queue
import socketClient as SocketCli
import dbConnection as Mysql
app = Flask(__name__)


@app.route('/')
def index():
   
    return render_template("index.html")


@app.route('/anomalyDetection', methods=['GET', 'POST'])
def anomalyDetection():
   
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        page = 0
        num = 5
    else:
        page = parameter_dict["page"]
        num = parameter_dict["num"]
        try:
            page=int(page)
            num=int(num)
            
        except:
            page=0
            num=5
    
    print("com1")
    mysqlDB = Mysql.MysqlConnector()
    print("com2")
    getData, paging = mysqlDB.getPageData(page, num)
        
    return render_template("anomalyDetection.html", getData, paging)

@app.route('/liveStreaming')
def liveStreaming():
    print("출력해라")
    return render_template("liveStreaming.html")

@app.route('/liveCam01')
def liveCam01():
    return #Response(getLiveCam01(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
    return #Response(getLiveCam02(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
    #sock = SocketCli.SocketClient()
    #socket_process = Process(target=sock.clientON, args=(imgQueue1, imgQueue2, robotDataQueue, setDataQueue))
    #socket_process.start()
    app.run(host="0.0.0.0", port ="8484", debug=True)
    