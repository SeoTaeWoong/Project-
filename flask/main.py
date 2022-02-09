from flask import Flask, render_template, Response, request
from multiprocessing import Process, Queue
import socketClient as SocketCli
import dbConnection as Mysql
import datetime
import json

app = Flask(__name__)
maskUserCnt = 0;
noMaskUserCnt = 0;

@app.route('/')
def index():
   
    return render_template("index.html")


@app.route('/anomalyDetection', methods=['GET', 'POST'])
def anomalyDetection():
   
    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        page = 1
        num = 5
    else:
        page = parameter_dict["page"]
        num = parameter_dict["num"]
        try:
            page=int(page)
            num=int(num)
            
        except:
            page=1
            num=5
    
    print("com1")
    mysqlDB = Mysql.MysqlConnector()
    print("com2")
    getData, paging = mysqlDB.getPageData(page, num)
        
    return render_template("anomalyDetection.html", getData=getData, paging=paging)

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

@app.route('/getDetectData', methods=['POST'])
def getDetectData():
    mysqlDB = Mysql.MysqlConnector()
    tupleData = mysqlDB.getDetectUser();
    dicData = {}
    try:
        for i in range(len(tupleData)):
            dicData[i] = {"seq": tupleData[i][0]}
            dicData[i]["temp"] = tupleData[i][1]
            dicData[i]["mask"] = tupleData[i][2]
            dicData[i]["name"] = tupleData[i][3]
            dicData[i]["age"] = tupleData[i][4]
            dicData[i]["gender"] = tupleData[i][5]
            dicData[i]["shootingData"] = tupleData[i][6]
            dicData[i]["logDate"] = "{:%B %d, %Y - %H:%M:%S}".format(tupleData[i][7])
            
            
    except Exception as e:
        print("err:",e);

    return json.dumps(dicData)


@app.route('/getInfoData', methods=['POST'])
def getInfoData():
    if request.method == "POST":
        jsonData = request.get_json()
        mysqlDB = Mysql.MysqlConnector()
        tupleData = mysqlDB.getInfoData(jsonData);
        print(jsonData)
    return ''

@app.route('/getMaskPlotData', methods=['POST'])
def getMaskPlotData():
    mysqlDB = Mysql.MysqlConnector()
    tupleData = mysqlDB.getMaskPlotData();
    
    dictData = {};
    dictData[tupleData[0][0]] = tupleData[0][1]
    dictData[tupleData[1][0]] = tupleData[1][1]
    
    return json.dumps(dictData)

@app.route('/getToDayCountData', methods=['POST'])
def getToDayCountData():
    mysqlDB = Mysql.MysqlConnector()
    now = "{:%%%Y/%m/%d%%}".format(datetime.datetime.now())
    dictData = mysqlDB.getToDayCountData(now);
    return json.dumps(dictData)

if __name__ == '__main__':
    imgQueue1 = Queue()
    imgQueue2 = Queue()
    robotDataQueue = Queue()
    setDataQueue = Queue()
    
    #sock = SocketCli.SocketClient()
    #socket_process = Process(target=sock.clientON, args=(imgQueue1, imgQueue2, robotDataQueue, setDataQueue))
    #socket_process.start()


    app.run(host="0.0.0.0", port ="8484")
    