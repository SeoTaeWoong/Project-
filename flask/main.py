from flask import Flask, render_template, Response, request
from multiprocessing import Process, Queue
import threading as Threading
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
    mysqlDB = Mysql.MysqlConnector()
    getData, paging = mysqlDB.getPageData(page, num)
        
    return render_template("anomalyDetection.html", getData=getData, paging=paging)

@app.route('/liveStreaming')
def liveStreaming():
    return render_template("liveStreaming.html")

@app.route('/liveCam01')
def liveCam01():
    return #Response(getLiveCam01(), mimetype='multipart/x-mixed-replace; boundary=frame')

def getLiveCam01():
    while True:
        
        if imgQueue1.qsize() != 0:
            
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + imgQueue1.get() + b'\r\n')
        else :
            pass
            

@app.route('/liveCam02')
def liveCam02():
    return #Response(getLiveCam02(), mimetype='multipart/x-mixed-replace; boundary=frame')

def getLiveCam02():
    while True:
        
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
        
    return ''

@app.route('/getDetectData', methods=['POST'])
def getDetectData():
    mysqlDB = Mysql.MysqlConnector()
    tupleData = mysqlDB.getDetectUser();
    dictData = {}
    
    try:
        for i in range(len(tupleData)):
            dictData[i] = {"seq": tupleData[i][0]}
            dictData[i]["temp"] = tupleData[i][1]
            if tupleData[i][2] == 0:
                dictData[i]["mask"] = "On"
            else:
                dictData[i]["mask"] = "No"
            
            dictData[i]["name"] = tupleData[i][3]
            
            dictData[i]["shootingData"] = tupleData[i][6]
            dictData[i]["checked"] = tupleData[i][7]
            dictData[i]["warning"] = tupleData[i][8]
            dictData[i]["logDate"] = "{:%B %d, %Y - %H:%M:%S}".format(tupleData[i][11])
            
    
    except Exception as e:
        print("err:",e);
    
    return json.dumps(dictData)


@app.route('/getInfoData', methods=['POST'])
def getInfoData():
    if request.method == "POST":
        jsonData = request.get_json()
        mysqlDB = Mysql.MysqlConnector()
        tupleData = mysqlDB.getInfoData(jsonData["seq"]);
        listData = list(tupleData[0])
        
            
        dictData = {
            "seq":listData[0],
            "name":listData[1],
            "age":listData[2],
            "gender":listData[3],
            "temp":listData[4],
            "mask":listData[5],
            "origin_img":listData[6].replace("D:/project2021/imgFileServer","/static/mntimg"),
            "origin_ir_img":listData[7].replace("D:/project2021/imgFileServer","/static/mntimg"),
            "detail_img":listData[8].replace("D:/project2021/imgFileServer","/static/mntimg"),
            "detail_ir_img":listData[9].replace("D:/project2021/imgFileServer","/static/mntimg"),
            }
        
        #{{url_for('static', filename='mntimg/shutdown.png')}}
        
    return json.dumps(dictData)

@app.route("/getMembers", methods=['POST'])
def getMembers():
    mysqlDB = Mysql.MysqlConnector()
    tupleData = mysqlDB.getMembersData()
    
    dictData = {};
    for index in range(len(tupleData)):
        dictData[tupleData[index][1]] = {"name":tupleData[index][1]}
        dictData[tupleData[index][1]]["age"] = tupleData[index][2]
        
        if tupleData[index][3] == 0:
            dictData[tupleData[index][1]]["gender"] = "Male"
        else:
            dictData[tupleData[index][1]]["gender"] = "FeMale"
        dictData[tupleData[index][1]]["email"] = tupleData[index][5]
        dictData[tupleData[index][1]]["img"] = tupleData[index][6]
        
    return json.dumps(dictData) 

@app.route("/getMemberList", methods=['POST'])
def getMemberList():
    mysqlDB = Mysql.MysqlConnector()
    tupleData = mysqlDB.getMemberListData()
    dictData = {}
    
    for index in range(len(tupleData)):
        dictData[index] = tupleData[index]
    return json.dumps(dictData)

@app.route("/getMemberInfo", methods=['POST'])
def getMemberInfo():
    jsonData = request.get_json()
    nowDate = datetime.datetime.now()
    dayData = {
            0:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(6)),
            1:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(5)),
            2:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(4)),
            3:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(3)),
            4:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(2)),
            5:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(1)),
            6:"{:%%%Y/%m/%d%%}".format(nowDate)
        }
    
    email= jsonData["email"]
    
    mysqlDB = Mysql.MysqlConnector()
    userDict, plotDict = mysqlDB.getMemberInfoAllData(email,dayData)
    
    userDict.update(plotDict)
    if(userDict["name"] == "Unknown"):
        userDict["age"] = "Unknown"
        userDict["gender"] = "Unknown"
    elif userDict["gender"] == 0 :
        userDict["gender"] = "Male"
    elif userDict["gender"] == 1 :
        userDict["gender"] = "FeMale"
    
    return json.dumps(userDict)

@app.route('/warningData', methods=['POST'])
def warningData():
    if request.method == "POST":
        
        
        jsonData = request.get_json()
        mysqlDB = Mysql.MysqlConnector()
        mysqlDB.warningDataUpdate(jsonData)

    return json.dumps({"0":"OK"})

@app.route('/getMaskPlotData', methods=['POST'])
def getMaskPlotData():
    mysqlDB = Mysql.MysqlConnector()
    tupleData = mysqlDB.getMaskPlotData();
    
    dictData = {};
    if len(tupleData) == 1 :
        dictData[tupleData[0][0]] = tupleData[0][1]
        if tupleData[0][0] == 0:        
            dictData["1"]=0
        else:
            dictData["0"]=0

    elif len(tupleData) == 2 :
        dictData[tupleData[0][0]] = tupleData[0][1]
        dictData[tupleData[1][0]] = tupleData[1][1]
    else:
        dictData["0"] = 0
        dictData["1"] = 0
    
    return json.dumps(dictData)
    
@app.route('/getToDayCountData', methods=['POST'])
def getToDayCountData():
    mysqlDB = Mysql.MysqlConnector()
    now = "{:%%%Y/%m/%d%%}".format(datetime.datetime.now())
    dictData = mysqlDB.getToDayCountData(now);
    return json.dumps(dictData)


@app.route('/memberAllData', methods=['POST'])
def memberAllData():
    jsonData = request.get_json()
    nowDate = datetime.datetime.now()
    dayData = {
            0:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(6)),
            1:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(5)),
            2:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(4)),
            3:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(3)),
            4:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(2)),
            5:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(1)),
            6:"{:%%%Y/%m/%d%%}".format(nowDate)
        }
    
    email= jsonData["email"]
    
    mysqlDB = Mysql.MysqlConnector()
    userDict, plotDict = mysqlDB.getMemberInfoAllData(email,dayData)
    return json.dumps(plotDict)

@app.route('/memberVerifyData', methods=['POST'])
def memberVerifyData():
    jsonData = request.get_json()
    nowDate = datetime.datetime.now()
    dayData = {
            0:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(6)),
            1:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(5)),
            2:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(4)),
            3:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(3)),
            4:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(2)),
            5:"{:%%%Y/%m/%d%%}".format(nowDate-datetime.timedelta(1)),
            6:"{:%%%Y/%m/%d%%}".format(nowDate)
        }
    email= jsonData["email"]
    mysqlDB = Mysql.MysqlConnector()
    plotDict = mysqlDB.getMemberVerifyData(email, dayData)
    return json.dumps(plotDict)


@app.route('/getLogData_all', methods=['POST'])
def getLogData_all():
    jsonData = request.get_json()
    day = "{:%%%Y/%m/DAY%%}".format(datetime.datetime.now())
    jsonData["day"] = day.replace("DAY", jsonData["day"])
    
    mysqlDB = Mysql.MysqlConnector()
    logData = mysqlDB.getLogData_all(jsonData)
    
    return json.dumps(logData)

@app.route('/getLogData_verify', methods=['POST'])
def getLogData_verify():
    jsonData = request.get_json()
    day = "{:%%%Y/%m/DAY%%}".format(datetime.datetime.now())
    jsonData["day"] = day.replace("DAY", jsonData["day"])
    
    mysqlDB = Mysql.MysqlConnector()
    logData = mysqlDB.getLogData_verify(jsonData)
    
    return json.dumps(logData)

@app.route('/getSelectLogData', methods=['POST'])
def getSelectLogData():
    jsonData = request.get_json()
    seq = jsonData["seq"]
    
    mysqlDB = Mysql.MysqlConnector()
    logData = mysqlDB.getSelectLogData(seq)
    return json.dumps(logData)

@app.route('/getLiveData', methods=['POST'])
def getLiveData():
    jsonData = request.get_json()
    seq = jsonData["seq"]
    mysqlDB = Mysql.MysqlConnector()
    now = "{:%%%Y/%m/%d%%}".format(datetime.datetime.now())
    tupleData = mysqlDB.getLiveData(seq);
    dictData = mysqlDB.getToDayCountData(now);
    for index in range(len(tupleData)):
        dictData[index] = {"seq": tupleData[index][0]}
        dictData[index]["temp"] = tupleData[index][1]
        if tupleData[index][2] == 0:
            dictData[index]["mask"] = "On"
        else:
            dictData[index]["mask"] = "No"
        dictData[index]["name"] = tupleData[index][3]
        dictData[index]["date"] = tupleData[index][4]
        dictData[index]["checked"] = tupleData[index][5]
        dictData[index]["warning"] = tupleData[index][6]
    
        
    
    return json.dumps(dictData)

if __name__ == '__main__':
    imgQueue1 = Queue()
    imgQueue2 = Queue()
    robotDataQueue = Queue()
    setDataQueue = Queue()
    warningQueue = Queue()
    
    sock = SocketCli.SocketClient()
    socket_process = Process(target=sock.clientON, args=(imgQueue1, imgQueue2, robotDataQueue, setDataQueue, warningQueue))
    socket_process.start()


    app.run(host="0.0.0.0", port=8484)
    