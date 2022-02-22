
window.onload = function(){
    
    
    var shutdownBtn = document.querySelector('.shutdownBtn');
    var chartTable = document.querySelector(".chartTable");
    var checkNumResult = document.querySelector(".checkNumResult");
    var noMaskNumResult = document.querySelector(".noMaskNumResult");
    var checkNumEffect = document.querySelector(".checkNumEffect");
    var noMaskNumEffect = document.querySelector(".noMaskNumEffect");
    var chartImgZoom = document.querySelector(".chartImg");
    var magnifier = document.querySelector(".magnifier");
    let chartInfoTab = document.querySelector(".chartInfoTab");
    let chartMemberTab = document.querySelector(".chartMemberTab");
    
    
    const getDetectData = function(){
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/getDetectData", false);
        xhr.onreadystatechange = function(){
            if(xhr.readyState ==4){
                if(xhr.status == 200){
                    
                    data = JSON.parse(this.responseText)
                    htmlText = ""
                    for(key in data){
                        value = data[key]
                        let checked = ""
                        let _warning = ""
                        let maskLine = '</li><li style="font-weight:bold">'+value["mask"]
                        let tempLine = '</div></li><li style="font-weight:bold">'+value["temp"]
                        
                        if(value["checked"] === 0){
                            checked = "newIcon"
                        }
                        if(value["warning"] === 1){
                            _warning = "warningIcon"
                            
                            if(value["mask"] === "No")
                                maskLine = '</li><li style="color:red; font-weight:bold">'+value["mask"]
                            
                            if(value["temp"] > 28)
                                tempLine = '</li><li style="color:red; font-weight:bold;">'+value["temp"]
                        }
                        
                        
                        
                        htmlText +='<ul class="items item'+value["seq"]+'"> <li><div class='+checked+
                            '></div><div class='+_warning+
                            '></div><div class="seqFont">'+value["seq"]+
                            '</div></li><li>'+value["name"]+
                            tempLine+maskLine+
                            '</li><li>'+value["shootingData"]+
                            '</li><li><div class="infoBtn" data-seq='+value["seq"]+
                            '>▶</div></li></ul>'
                    }
                    chartTable.innerHTML = htmlText
                    var infoBtns = document.querySelectorAll(".infoBtn");
                    infoBtns.forEach(function(item,index,arr){
                        
                        
                        item.addEventListener("click", function(){
                            let clickEvent = document.querySelector(".clickEvent")
                            if(clickEvent != null){
                                clickEvent.classList.remove("clickEvent")
                            }
                            item.parentNode.parentNode.classList.add("clickEvent")
                            item.parentNode.previousSibling.previousSibling.previousSibling.previousSibling.previousSibling.firstChild.classList.remove("newIcon")
                            xhr = new XMLHttpRequest();
                            xhr.open("POST", "/getInfoData", false);
                            jsonData = {"seq":item.dataset.seq}
                            jsonData = JSON.stringify(jsonData)
                            xhr.onreadystatechange = function(){
                                if(xhr.readyState ==4){
                                    if(xhr.status == 200){
                                        
                                        data = JSON.parse(this.responseText)
                                        var event = new MouseEvent('click', {
                                            bubbles: true,
                                            cancelable: true,
                                            view: window
                                        });
                                        
                                        chartInfoTab.dispatchEvent(event)
                                        let chartLog = document.querySelector(".chartLog");
                                        chartLog.disabled=false;
                                        
                                        let chartSeq = document.querySelector(".chartSeq");
                                        let userName = document.querySelector(".userName");
                                        let predictedAge = document.querySelector(".predictedAge");
                                        let predictedGender = document.querySelector(".predictedGender");
                                        let temperature = document.querySelector(".temperature");
                                        let useOfMask = document.querySelector(".useOfMask");
                                        let verifyBtn = document.querySelector(".verifyBtn");
                                        let chartImg = document.querySelector('.chartImg');
                                       
                                        let genderHTML = ""
                                        if(data["gender"] == 0){
                                            genderHTML = '<label><input type="radio" name="gender" value="0" checked>남</label>'+
                                                         '<label><input type="radio" name="gender" value="1">여</label>'
                                        }else if(data["gender"]==1){
                                            genderHTML = '<label><input type="radio" name="gender" value="0">남</label>'+
                                                         '<label><input type="radio" name="gender" value="1" checked>여</label>'
                                        }else{
                                            genderHTML = '<label><input type="radio" name="gender" value="0">남</label>'+
                                                         '<label><input type="radio" name="gender" value="1">여</label>'
                                        }
                                        
                                        let chartImgNum1 = document.querySelector(".chartImgNum1")
                                        let chartImgNum2 = document.querySelector(".chartImgNum2")
                                        let chartImgNum3 = document.querySelector(".chartImgNum3")
                                        let chartImgNum4 = document.querySelector(".chartImgNum4")
                                        
                                        let origin_img = data["origin_img"]
                                        let detail_ir_img = data["detail_ir_img"]
                                        let detail_img = data["detail_img"]
                                        let origin_ir_img = data["origin_ir_img"]
                                       
                                        chartImgNum1.addEventListener("click", function(){
                                            chartImg.src = origin_img
                                        });
                                       
                                        chartImgNum2.addEventListener("click", function(){
                                            chartImg.src = detail_ir_img
                                            
                                        });
                                       
                                        chartImgNum3.addEventListener("click", function(){
                                            chartImg.src = detail_img
                                            
                                        });
                                       
                                        chartImgNum4.addEventListener("click", function(){
                                            chartImg.src = origin_ir_img
                                        });
                                        
                                        
                                        let maskHTML =""
                                        if(data["mask"] == 0){
                                            maskHTML = '<label><input type="radio" name="mask" value="0" checked>On</label>'+
                                                         '<label><input type="radio" name="mask" value="1">No</label>'
                                        }else if(data["mask"]==1){
                                            maskHTML = '<label><input type="radio" name="mask" value="0">On</label>'+
                                                         '<label><input type="radio" name="mask" value="1" checked>No</label>'
                                        }
                                        
                                        chartSeq.innerHTML = 'No. '+data["seq"]
                                        userName.innerHTML = '이름: '+ data["name"]
                                        predictedAge.innerHTML = '추정 나이: '+ data["age"]
                                        temperature.innerHTML = '감지 온도: '+data["temp"]
                                        predictedGender.innerHTML = '성별 : '+genderHTML;
                                        useOfMask.innerHTML = '마스크:  '+maskHTML
                                        verifyBtn.innerHTML = "확인"
                                        chartImg.src= data["origin_img"];
                                        
                                        verifyBtn.addEventListener("click", function(){
                                            let className = ".item"+data["seq"]
                                            
                            
                                            let inputGender = predictedGender.querySelectorAll("input[name='gender']:checked")
                                            let inputMask = useOfMask.querySelectorAll("input[name='mask']:checked")
                                            
                                            
                                            
                                            let errMSG = document.querySelector(".errMSG");
                                            
                                            if(inputGender.length == 0){
                                                errMSG.innerHTML="*성별을 확인하세요"
                                            }else{
                                            
                                                
                                                name = data["name"]
                                                gender= inputGender[0].value == 0 ? "남성" : "여성";
                                                mask = inputMask[0].value == 0 ? "On" : "Off";
                                                temp = data["temp"]
                                                age = data["age"];
                                                
                                                errMSG.innerHTML=""
                                                
                                                
                                                let modal = document.querySelector(".modal");
                                                let modalCancelBtn = document.querySelector(".modalCancelBtn");
                                                let modalImg = document.querySelector(".modalImg")
                                                let modalName = modal.querySelector(".modalName")
                                                let modalAge = modal.querySelector(".modalAge")
                                                let modalGen = modal.querySelector(".modalGen")
                                                let modalTemp = modal.querySelector(".modalTemp")
                                                let modalMask = modal.querySelector(".modalMask")
                                                let modalNum = modal.querySelector(".modalNum")
                                                
                                                
                                                modalImg.src = data["origin_img"]
                                                modalNum.value = data["seq"]
                                                modalName.innerHTML = "이름 :"+name
                                                modalAge.innerHTML = "나이 :"+age
                                                modalGen.innerHTML = "성별 :"+gender
                                                modalTemp.innerHTML = "온도 :"+temp
                                                modalMask.innerHTML = "마스크 :"+mask
                                                
                                                
                                                modal.classList.add("modalOn")
                                                modalCancelBtn.addEventListener("click", function(){
                                                
                                                    modal.classList.remove("modalOn")
                                                })
                                                
                                                
                                                xhr = new XMLHttpRequest();
                                                xhr.open("POST", "/getMembers", false);
                                                xhr.onreadystatechange = function(){
                                                    if(xhr.readyState ==4){
                                                        if(xhr.status == 200){
                                                            
                                                            
                                                            _data = JSON.parse(this.responseText)
                                                            
                                                            let memberSelect = document.querySelector(".memberSelect")
                                                            let selectOptionText = "";
                                                            
                                                            for(key in _data){
                                                                selectOptionText += "<option value='"+_data[key]["name"]+"'>"+_data[key]["name"]+"</option>"
                                                            }
                                                            memberSelect.innerHTML = selectOptionText;
                                                            let modalMemberName = document.querySelector(".modalMemberName")
                                                            let modalMemberAge = document.querySelector(".modalMemberAge")
                                                            let modalMemberGen = document.querySelector(".modalMemberGen")
                                                            let modalMemberEmail = document.querySelector(".modalMemberEmail")
                                                            let modalMemberImg = document.querySelector(".modalMemberImg")
                                                            
                                                            
                                                            modalMemberImg.src = _data["Unknown"]["img"]
                                                            modalMemberName.innerHTML = _data["Unknown"]["name"]
                                                            modalMemberAge.innerHTML = _data["Unknown"]["age"]
                                                            modalMemberGen.innerHTML = _data["Unknown"]["gender"]
                                                            modalMemberEmail.innerHTML = _data["Unknown"]["email"]
                                                            
                                                            memberSelect.addEventListener("change", function(){
                                                                let _key = memberSelect.value
                                                                modalMemberImg.src = _data[_key]["img"]
                                                                modalMemberName.innerHTML = _data[_key]["name"]
                                                                modalMemberAge.innerHTML = _data[_key]["age"]
                                                                modalMemberGen.innerHTML = _data[_key]["gender"]
                                                                modalMemberEmail.innerHTML = _data[_key]["email"]        
                                                            })
                                                            
                                                            let modalCheckBtn = document.querySelector(".modalCheckBtn");
                                                            modalCheckBtn.addEventListener("click", function(){
                                                                
                                                                sendData = {
                                                                    "seq" : modalNum.value ,
                                                                    "name" : modalMemberName.textContent,
                                                                    "age" : modalMemberAge.textContent,
                                                                    "gender" : modalMemberGen.textContent,
                                                                    "Email" : modalMemberEmail.textContent,
                                                                    "log" : chartLog.value
                                                                }
                                                                
                                                                sendData = JSON.stringify(sendData)
                                                                _xhr = new XMLHttpRequest();
                                                                _xhr.open("POST", "/warningData", false);
                                                                _xhr.onreadystatechange = function(){
                                                                    if(_xhr.readyState ==4){
                                                                        if(_xhr.status == 200){
                                                                            
                                                                            modal.classList.remove("modalOn")
                                                                            getDetectData()
                                                                            
                                                                            chartImg.src = "static/img/NoImage.jpg"
                                                                            chartSeq.innerHTML = ""
                                                                            userName.innerHTML = ""
                                                                            predictedAge.innerHTML = ""
                                                                            temperature.innerHTML = ""
                                                                            predictedGender.innerHTML = ""
                                                                            useOfMask.innerHTML = ""
                                                                            verifyBtn.innerHTML = ""
                                                                            chartLog.disabled=true
                                                                            chartLog.innerHTML=""
                                                                                
                                                                        }else{
                                                                            alert("요청 실패: "+_xhr.status);
                                                                        }
                                                                    }
                                                                }
                                                                
                                                                _xhr.setRequestHeader("Content-Type", "application/json");
                                                                _xhr.send(sendData)
                                                                
                                                            })
                                                            
                                                        }else{
                                                            alert("요청 실패: "+xhr.status);
                                                        }
                                                    }
                                                }
                                                
                                                xhr.setRequestHeader("Content-Type", "application/json");
                                                xhr.send()
                                            }
                                            
                                        });
                                       
                                        
                                       
                                    }else{
                                       alert("요청 실패: "+xhr.status);
                                    }
                                }
                            }
                           
                            xhr.setRequestHeader("Content-Type", "application/json");
                            xhr.send(jsonData)
                        })
                    })
                    
                }else{
                    alert("요청 실패: "+xhr.status);
                }
            }
        }
        
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send()
        //xhr.setRequestHeader("Content-Type", "application/json");
        //xhr.send(jsonData)
    }
    
    
    const getMaskPlotData = function(){
        
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/getMaskPlotData", true);
        xhr.onreadystatechange = function(){
            if(xhr.readyState ==4){
                if(xhr.status == 200){
                    
                    data = JSON.parse(this.responseText)
                    
                    Highcharts.setOptions({
                      colors: ['#01BAF2', '#71BF45', '#FAA74B']
                    });  
                    Highcharts.chart('maskUsagePlot', {
                        chart: {
                          plotBackgroundColor: null,
                          plotBorderWidth: null,
                          plotShadow: false,
                          type: 'pie'
                        },
                        title: {
                          text: 'MaskUsagePlot'
                        },
                        tooltip: {
                          pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                        },
                        plotOptions: {
                          pie: {
                            allowPointSelect: true,
                            cursor: 'pointer',
                            dataLabels: {
                              enabled: false
                            },
                            showInLegend: true
                          }
                        },
                        series: [{
                          name: 'percentage',
                          colorByPoint: true,
                          data: [{
                            name: 'Mask('+data["0"]+')',
                            y: data["0"],
                          }, {
                            name: 'No Mask('+data["1"]+')',
                            y: data["1"],
                            sliced: true,
                            selected: true
                          }]
                        }]
                      });

                    
                }else{
                    alert("요청 실패: "+xhr.status);
                }
            }
        }
        
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send()
    }
    
     const getToDayCountData = function(){
        
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/getToDayCountData", false);
        xhr.onreadystatechange = function(){
            if(xhr.readyState ==4){
                if(xhr.status == 200){
                    
                    data = JSON.parse(this.responseText)
                    checkNumResult.innerHTML = data["tester"]
                    checkNumEffect.innerHTML = data["tester"]
                    noMaskNumResult.innerHTML = data["mask"]        
                    noMaskNumEffect.innerHTML = data["mask"]
                }else{
                    alert("요청 실패: "+xhr.status);
                }
            }
        }
        
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send()
    }
    
    
    
    var chartList = function(){
        getDetectData()
    }
    chartList()
    
    var toDayCount = function(){
        getToDayCountData()
    }
    toDayCount()
    
    var maskUsagePlot = function(){
        getMaskPlotData()
    }
    maskUsagePlot()
    
    
    
    var cnt = 0;
    
    var xhr;
    
    
    
    
    chartInfoTab.addEventListener("click", function(){
        let chartInfo = document.querySelector(".chartInfo");
        chartInfoTab.classList.remove('noneSelect')
        chartMemberTab.classList.add('noneSelect');
        chartInfo.innerHTML = '<ul>'+
                                '<li class="chartDivision">'+
                                    '<ul class="chartTextArea">'+
                                        '<li class="chartImageArea">'+
                                            '<figure>'+
                                                '<img class="chartImg" onerror="this.src=\'/static/img/NoImage.jpg\'" src="..">'+
                                            '</figure>'+                           
                                            '<ul>'+
                                                '<li class="chartImgNum1">'+
                                                    'No.1'+
                                                '</li>'+
                                                '<li class="chartImgNum2">'+
                                                    'No.2'+
                                                '</li>'+
                                                '<li class="chartImgNum3">'+
                                                    'No.3'+
                                                '</li>'+
                                                '<li class="chartImgNum4">'+
                                                    'No.4'+
                                                '</li></ul></li>'+
                                        '<li class="chartIntelligence">'+
                                            '<div class="chartSeq"></div>'+
                                            '<div class="userName"></div>'+
                                            '<div class="predictedAge"></div>'+
                                            '<div class="temperature"></div>'+
                                            '<div class="predictedGender"></div>'+
                                            '<div class="useOfMask"></div>'+
                                            '<div class="errMSG"></div>'+
                                            '<div class="verifyBtn"></div>'+
                                        '</li></ul>'+
                                        '<div class="chartLogWrap">'+
                                            '<h4>Chart Log</h4>'+
                                            '<textArea class="chartLog" disabled="true";></textArea>'+
                                        '</div>'

        
        
    })
    
    let getLogData = function(jsonData, url){
        
        jsonData = JSON.stringify(jsonData)
        _xhr = new XMLHttpRequest();
        _xhr.open("POST", url, false);
        _xhr.onreadystatechange = function(){
            if(_xhr.readyState ==4){
                if(_xhr.status == 200){
                    let logModalWrap = document.querySelector('.logModalWrap')
                    
                    logModalWrap.addEventListener("click", function(e){
                        if (e.target == e.currentTarget){
                            logModalWrap.classList.remove("modalOn")  
                        }
                    })
                        
                    
                    
                    logModalWrap.classList.add("modalOn")  
                    
                    data = JSON.parse(this.responseText)
                    
                    let logListArea = logModalWrap.querySelector(".logListArea")
                    let logItem = ""
                    for(index in data["seq"]){
                        
                        logItem += '<li class="logItem">LogFile_'+data["seq"][index]+'</li>'
                    }
                    logListArea.innerHTML = logItem
                    let logFile = logModalWrap.querySelector(".logFile")
                    let logDate = logModalWrap.querySelector(".logDate")
                    let logName = logModalWrap.querySelector(".logName")
                    let logGender = logModalWrap.querySelector(".logGender")
                    let logTemp = logModalWrap.querySelector(".logTemp")
                    let logMask = logModalWrap.querySelector(".logMask")
                    let logContent = logModalWrap.querySelector(".logContent")
                    _seqs
                    logFile.innerHTML = "- LogFile_"+data["seq"][0]+" -"
                    logDate.innerHTML = data["date"]
                    logName.innerHTML = data["name"]
                    logGender.innerHTML = data["gender"]
                    logTemp.innerHTML = data["temp"]
                    logMask.innerHTML = data["mask"]
                    logContent.innerHTML = data["log"]
                    
                    let logModalMainImg = logModalWrap.querySelector('.logModalMainImg')
                    let logModalSubImg1 = logModalWrap.querySelector('.logModalSubImg1')
                    let logModalSubImg2 = logModalWrap.querySelector('.logModalSubImg2')
                    let logModalSubImg3 = logModalWrap.querySelector('.logModalSubImg3')
                    let logModalSubImg4 = logModalWrap.querySelector('.logModalSubImg4')
                    
                    logModalMainImg.src = "/static/"+data["img1"]
                    logModalSubImg1.src = "/static/"+data["img1"]
                    logModalSubImg2.src = "/static/"+data["img2"]
                    logModalSubImg3.src = "/static/"+data["img3"]
                    logModalSubImg4.src = "/static/"+data["img4"]
                    
                    logModalSubImg1.classList.add("imgSelect")
                    
                    let logModalSubImg = logModalWrap.querySelectorAll(".logModalSubImg")
                    logModalSubImg.forEach(function(item, index, addr){
                        item.addEventListener("click", function(){
                            let imgSelect = logModalWrap.querySelector(".imgSelect");
                            if(imgSelect != null)
                                imgSelect.classList.remove("imgSelect")
                            logModalMainImg.src = item.src
                            item.classList.add("imgSelect")
                        })
                    })
                    
                    let logItems = logModalWrap.querySelectorAll(".logItem");
                    logItems[0].classList.add("logItemSelect")
                    
                    logItems.forEach(function(item, index, arr){
                        item.addEventListener("click", function(){
                            let logItemSelect = logModalWrap.querySelector(".logItemSelect");
                            logItemSelect.classList.remove("logItemSelect")
                            item.classList.add("logItemSelect")
                            
                            _jsonData = {"seq":item.textContent.replace("LogFile_","")}
                            _jsonData = JSON.stringify(_jsonData);
                            
                            
                            __xhr = new XMLHttpRequest();
                            __xhr.open("POST", "/getSelectLogData", false);
                            __xhr.onreadystatechange = function(){
                                if(__xhr.readyState ==4){
                                    if(__xhr.status == 200){
                                        _data = JSON.parse(this.responseText)
                                        
                                        logFile.innerHTML = "- "+item.textContent+" -"
                                        logDate.innerHTML = _data["date"]
                                        logName.innerHTML = _data["name"]
                                        logGender.innerHTML = _data["gender"]
                                        logTemp.innerHTML = _data["temp"]
                                        logMask.innerHTML = _data["mask"]
                                        logContent.innerHTML = _data["log"]
                                        logModalMainImg.src = "/static/"+_data["img1"]
                                        logModalSubImg1.src = "/static/"+_data["img1"]
                                        logModalSubImg2.src = "/static/"+_data["img2"]
                                        logModalSubImg3.src = "/static/"+_data["img3"]
                                        logModalSubImg4.src = "/static/"+_data["img4"]
                                        let imgSelect = logModalWrap.querySelector(".imgSelect");
                                        if(imgSelect != null)
                                            imgSelect.classList.remove("imgSelect")
                                        logModalSubImg1.classList.add("imgSelect")
                                    }else{
                                        alert("요청 실패: "+__xhr.status);
                                    }
                                }
                            }
                            __xhr.setRequestHeader("Content-Type", "application/json");
                            __xhr.send(_jsonData)
                        })
                    })
                }else{
                    alert("요청 실패: "+_xhr.status);
                }
            }
        }
        
        _xhr.setRequestHeader("Content-Type", "application/json");
        _xhr.send(jsonData)
    }    
    
    
    chartMemberTab.addEventListener("click", function(){
        let chartInfo = document.querySelector(".chartInfo");
        chartInfoTab.classList.add('noneSelect');
        chartMemberTab.classList.remove('noneSelect');
        chartInfo.innerHTML='<ul class="memberList">'+
                                
                            '</ul>'+
                            '<ul class="memberInfoArea">'+
                                '<li class="memberInfo">'+
                                    '<figure><img class="memberImg"></figure>'+
                                    '<ul class="memberStatusInfo">'+
                                        '<li class="memberName">Name: Unknown</li>'+
                                        '<li class="memberBirth">Birth: Unknown</li>'+    
                                        '<li class="memberAge">Age: Unknown</li>'+
                                        '<li class="memberGen">Gender: Unknown</li>'+    
                                    '</ul>'+    
                                '</li>'+
                                '<li class="memberlinePlot">'+
                                    '<label for="plotCheck">All<input name="plotCheck" type="radio" value="all" checked disabled></label>'+
                                    '<label for="plotCheck">verify<input name="plotCheck" type="radio" value="verify" disabled></label>'+
                                    '<div id="linePlot" class="linePlot"></div>'+
                                '</li>'+
                            '</ul>'
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/getMemberList", false);
        xhr.onreadystatechange = function(){
            if(xhr.readyState ==4){
                if(xhr.status == 200){
                    
                    data = JSON.parse(this.responseText)
                    let memberList = document.querySelector(".memberList");
                    let memberListText=""
                    for(key in data){
                        memberListText += "<li class='item'>"+data[key]+"</li>"
                    }
                    
                    memberList.innerHTML = memberListText;
                    let members = document.querySelectorAll(".item")
                    members.forEach(function(item, index, arr){
                        item.addEventListener("click", function(){
                            let jsonData = {"email":item.textContent}
                            jsonData = JSON.stringify(jsonData)
                            _xhr = new XMLHttpRequest();
                            _xhr.open("POST", "/getMemberInfo", false);
                            _xhr.onreadystatechange = function(){
                                if(_xhr.readyState ==4){
                                    if(_xhr.status == 200){
                                        data = JSON.parse(this.responseText)
                                        let memberName = document.querySelector(".memberName");
                                        let memberBirth = document.querySelector(".memberBirth");
                                        let memberAge = document.querySelector(".memberAge");
                                        let memberGen = document.querySelector(".memberGen");
                                        let memberImg = document.querySelector(".memberImg");
                                        memberName.innerHTML ="Name: "+data["name"]
                                        memberBirth.innerHTML ="Birth: "+data["birth"]
                                        memberAge.innerHTML ="Age: "+data["age"]
                                        memberGen.innerHTML ="Gennder: "+data["gender"]
                                        memberImg.src=data["img"]
                                        
                                        if(data['name'] == "Unknown"){
                                            let plotCheck = document.querySelectorAll("input[name='plotCheck']");
                                            for(key in plotCheck){
                                                if(plotCheck[key].value == "all"){
                                                    plotCheck[0].checked = true;
                                                    plotCheck[key].disabled = false
                                                }else{
                                                    plotCheck[key].disabled = true
                                                }
                                            }
                                        }else{
                                            let plotCheck = document.querySelectorAll("input[name='plotCheck']");
                                            plotCheck[0].checked = true;
                                            plotCheck[0].disabled = false;
                                            plotCheck[1].disabled = false;
                                        }
                                        let dateArr=[]
                                        let tempArr=[]
                                        let maskArr=[]
                                        for(let i = 0; i<7; i++){
                                            dateArr.push(data[i]["date"].split("/")[2])
                                            tempArr.push(data[i]["tempCnt"])
                                            maskArr.push(data[i]["maskCnt"])
                                        }
                                        
                                        
                                        
                                        Highcharts.chart('linePlot', {
                                            title:{
                                            	text: null
                                            },  
                                            scrollbar: {
                                	            enabled: false
                                            },
                                            navigator: {
                                            	enabled: false
                                            },
                                            exporting: {
                                            	enabled: false
                                            },
                                            chart: {
                                                type: 'line',
                                                spacingLeft: -30,
                                                spacingTop: 40
                                            },
                                            legend: {
                                                layout: 'vertical',
                                                floating: true,
                                                align: 'left', //정렬
                                                x: 460,
                                                verticalAlign: 'top',//정렬
                                                y: -45,
                                                itemStyle: {color: "red"} //글자스타일
                                            },
                                            xAxis: {
                                                title:{
                                                    text: 'Day'
                                                },
                                                categories: dateArr,
                                                labels:{ 
                                                	style: {color:'red'}
                                                }
                                            },
                                            yAxis: {
                                                tickInterval:5,
                                                min:0
                                            },
                                            plotOptions: {
                                                series:{
                                                     colorByPoint : false,
                                                     dataLabels:{
                                                         enabled : true, //각각의 데이터 값을 나타낼 것인지
                                                         color:'black', // 데이터 값을 나타낼 때 색
                                                         style: {
                                                             fontSize:'8px',
                                                             fontWeight:'bold',
                                                             textOutline:0  
                                                         }
                                                     }
                                                },
                                                connectNulls : true //null인 지점에 연결할 것인지
                                                
                                            },
                                            series: [{
                                                name: 'DangerZoneCnt',
                                                data: tempArr,
                                                events: {
                                                    click: function (event) {
                                                        if(event.point.options["y"] != 0){
                                                            let plotCheck_checked = document.querySelector("input[name='plotCheck']:checked")
                                                            let url = "/getLogData_all"
                                                            _jsonData = JSON.parse(jsonData)
                                                            _jsonData.day = event.point["category"]
                                                            _jsonData.temp = 28 
                                                            getLogData(_jsonData, url)
                                                        }else{
                                                            alert("데이터가 없습니다.")
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                name: 'NoMaskCnt',
                                                data: maskArr,
                                                events: {
                                                    click: function (event) {
                                                        
                                                        if(event.point.options["y"] != 0){
                                                            let plotCheck_checked = document.querySelector("input[name='plotCheck']:checked")
                                                            let url = "/getLogData_all"
                                                            _jsonData = JSON.parse(jsonData)
                                                            _jsonData.day = event.point["category"]
                                                            _jsonData.mask = 1
                                                            getLogData(_jsonData, url)
                                                        }else{
                                                            alert("데이터가 없습니다.")
                                                        }
                                                    }
                                                }
                                            }]
                                            
                                        });
                                    }else{
                                        alert("요청 실패: "+_xhr.status);
                                    }
                                }
                            }
                            _xhr.setRequestHeader("Content-Type", "application/json");
                            _xhr.send(jsonData)
                            
                            let plotCheck = document.querySelectorAll("input[name='plotCheck']");
                            plotCheck.forEach(function(item, index, arr){
                                item.addEventListener("change", function(){
                                    
                                    let url=""
                                    if(this.value == "all"){
                                        url="/memberAllData"
                                    }else if(this.value == "verify"){
                                        url="/memberVerifyData"
                                    }
                                    let _xhr  = new XMLHttpRequest
                                    _xhr.open("POST",url,false)
                                    _xhr.onreadystatechange = function(){
                                        if(_xhr.readyState ==4){
                                            if(_xhr.status == 200){
                                                data = JSON.parse(this.responseText)
                                                
                                                let dateArr=[]
                                                let tempArr=[]
                                                let maskArr=[]
                                                for(let i = 0; i<7; i++){
                                                    dateArr.push(data[i]["date"].split("/")[2])
                                                    tempArr.push(data[i]["tempCnt"])
                                                    maskArr.push(data[i]["maskCnt"])
                                                }
                                                
                                                Highcharts.chart('linePlot', {
                                                    title:{
                                                    	text: null
                                                    },  
                                                    scrollbar: {
                                        	            enabled: false
                                                    },
                                                    navigator: {
                                                    	enabled: false
                                                    },
                                                    exporting: {
                                                    	enabled: false
                                                    },
                                                    chart: {
                                                        type: 'line',
                                                        spacingLeft: -30,
                                                        spacingTop: 40
                                                    },
                                                    legend: {
                                                        layout: 'vertical',
                                                        floating: true,
                                                        align: 'left', //정렬
                                                        x: 460,
                                                        verticalAlign: 'top',//정렬
                                                        y: -45,
                                                        itemStyle: {color: "red"} //글자스타일
                                                    },
                                                    xAxis: {
                                                        title:{
                                                            text: 'Day'
                                                        },
                                                        categories: dateArr,
                                                        labels:{ 
                                                        	style: {color:'red'}
                                                        }
                                                    },
                                                    yAxis: {
                                                        tickInterval:5,
                                                        min:0
                                                    },
                                                    plotOptions: {
                                                        series:{
                                                             colorByPoint : false,
                                                             dataLabels:{
                                                                 enabled : true, //각각의 데이터 값을 나타낼 것인지
                                                                 color:'black', // 데이터 값을 나타낼 때 색
                                                                 style: {
                                                                     fontSize:'8px',
                                                                     fontWeight:'bold',
                                                                     textOutline:0  
                                                                 }
                                                             }
                                                        },
                                                        connectNulls : true //null인 지점에 연결할 것인지
                                                        
                                                    },
                                                    series: [{
                                                        name: 'DangerZoneCnt',
                                                        data: tempArr,
                                                        events: {
                                                            click: function (event) {
                                                                if(event.point.options["y"] != 0){
                                                                    let plotCheck_checked = document.querySelector("input[name='plotCheck']:checked")
                                                                    let url = "/getLogData_"+plotCheck_checked.value
                                                                    _jsonData = JSON.parse(jsonData)
                                                                    _jsonData.day = event.point["category"]
                                                                    _jsonData.temp = 28
                                                                    getLogData(_jsonData, url)
                                                                }else{
                                                                    alert("데이터가 없습니다.")
                                                                }
                                                            }
                                                        }
                                                    },
                                                    {
                                                        name: 'NoMaskCnt',
                                                        data: maskArr,
                                                        events: {
                                                            click: function (event) {
                                                                if(event.point.options["y"] != 0){
                                                                    let plotCheck_checked = document.querySelector("input[name='plotCheck']:checked")
                                                                    let url = "/getLogData_"+plotCheck_checked.value
                                                                    _jsonData = JSON.parse(jsonData)
                                                                    _jsonData.day = event.point["category"]
                                                                    _jsonData.mask = 1
                                                                    getLogData(_jsonData, url)
                                                                }else{
                                                                    alert("데이터가 없습니다.")
                                                                }
                                                            }
                                                        }
                                                    }]
                                                    
                                                });
                                            
                                            }else{
                                                alert("요청 실패: ",_xhr.status)
                                            }
                                        }
                                    }
                                    _xhr.setRequestHeader("Content-Type", "application/json");
                                    _xhr.send(jsonData)
                                })
                            })
                            
                            
                        })
                    });
                }else{
                    alert("요청 실패: "+xhr.status);
                }
            }
        }
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send()
        
        
    });
    shutdownBtn.addEventListener("click", function(){
        location.href="/"
    })
    
    
    
    let _chartTable = document.querySelector(".chartTable")
    playAlert = setInterval(function() {
        
        let _seq = _chartTable.firstChild.querySelector(".seqFont")
        sendData = {"seq":_seq.textContent}
        jsonData = JSON.stringify(sendData)
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/getLiveData", false);
        xhr.onreadystatechange = function(){
            if(xhr.readyState ==4){
                if(xhr.status == 200){
                    
                    data = JSON.parse(this.responseText)
                    console.log(data)
                    checkNumResult.innerHTML = data["tester"]
                    checkNumEffect.innerHTML = data["tester"]
                    noMaskNumResult.innerHTML = data["mask"]        
                    noMaskNumEffect.innerHTML = data["mask"]
                    delete data["mask"]
                    delete data["tester"]
                    
                    if(data["0"] != undefined){
                        for(key in data){
                            
                            value = data[key]
                            let checked = ""
                            let _warning = ""
                            let maskLine = '</li><li style="font-weight:bold">'+value["mask"]
                            let tempLine = '</div></li><li style="font-weight:bold">'+value["temp"]
                            
                            if(value["checked"] === 0){
                                checked = "newIcon"
                            }
                            if(value["warning"] === 1){
                                _warning = "warningIcon"
                                
                                if(value["mask"] === "No")
                                    maskLine = '</li><li style="color:red; font-weight:bold">'+value["mask"]
                                
                                if(value["temp"] > 28)
                                    tempLine = '</li><li style="color:red; font-weight:bold;">'+value["temp"]
                            }
                            
                            
                            
                            htmlText='<ul class="items item'+value["seq"]+'"> <li><div class='+checked+
                                '></div><div class='+_warning+
                                '></div><div class="seqFont">'+value["seq"]+
                                '</div></li><li>'+value["name"]+
                                tempLine+maskLine+
                                '</li><li>'+value["date"]+
                                '</li><li><div class="infoBtn" data-seq='+value["seq"]+
                                '>▶</div></li></ul>'
                            _chartTable.insertAdjacentHTML("afterbegin", htmlText);
                            
                            item = _chartTable.firstChild
                            item.addEventListener("click", function(){
                                let clickEvent = document.querySelector(".clickEvent")
                                if(clickEvent != null){
                                    clickEvent.classList.remove("clickEvent")
                                }
                                item.parentNode.parentNode.classList.add("clickEvent")
                                item.parentNode.previousSibling.previousSibling.previousSibling.previousSibling.previousSibling.firstChild.classList.remove("newIcon")
                                xhr = new XMLHttpRequest();
                                xhr.open("POST", "/getInfoData", false);
                                jsonData = {"seq":item.dataset.seq}
                                console.log()
                                jsonData = JSON.stringify(jsonData)
                                xhr.onreadystatechange = function(){
                                    if(xhr.readyState ==4){
                                        if(xhr.status == 200){
                                            
                                            data = JSON.parse(this.responseText)
                                            var event = new MouseEvent('click', {
                                                bubbles: true,
                                                cancelable: true,
                                                view: window
                                            });
                                            
                                            chartInfoTab.dispatchEvent(event)
                                            let chartLog = document.querySelector(".chartLog");
                                            chartLog.disabled=false;
                                            
                                            let chartSeq = document.querySelector(".chartSeq");
                                            let userName = document.querySelector(".userName");
                                            let predictedAge = document.querySelector(".predictedAge");
                                            let predictedGender = document.querySelector(".predictedGender");
                                            let temperature = document.querySelector(".temperature");
                                            let useOfMask = document.querySelector(".useOfMask");
                                            let verifyBtn = document.querySelector(".verifyBtn");
                                            let chartImg = document.querySelector('.chartImg');
                                           
                                            let genderHTML = ""
                                            if(data["gender"] == 0){
                                                genderHTML = '<label><input type="radio" name="gender" value="0" checked>남</label>'+
                                                             '<label><input type="radio" name="gender" value="1">여</label>'
                                            }else if(data["gender"]==1){
                                                genderHTML = '<label><input type="radio" name="gender" value="0">남</label>'+
                                                             '<label><input type="radio" name="gender" value="1" checked>여</label>'
                                            }else{
                                                genderHTML = '<label><input type="radio" name="gender" value="0">남</label>'+
                                                             '<label><input type="radio" name="gender" value="1">여</label>'
                                            }
                                            
                                            let chartImgNum1 = document.querySelector(".chartImgNum1")
                                            let chartImgNum2 = document.querySelector(".chartImgNum2")
                                            let chartImgNum3 = document.querySelector(".chartImgNum3")
                                            let chartImgNum4 = document.querySelector(".chartImgNum4")
                                            
                                            let origin_img = data["origin_img"]
                                            let detail_ir_img = data["detail_ir_img"]
                                            let detail_img = data["detail_img"]
                                            let origin_ir_img = data["origin_ir_img"]
                                           
                                            chartImgNum1.addEventListener("click", function(){
                                                
                                                chartImg.src = origin_img
                                            });
                                           
                                            chartImgNum2.addEventListener("click", function(){
                                                chartImg.src = detail_ir_img
                                                
                                            });
                                           
                                            chartImgNum3.addEventListener("click", function(){
                                                chartImg.src = detail_img
                                                
                                            });
                                           
                                            chartImgNum4.addEventListener("click", function(){
                                                chartImg.src = origin_ir_img
                                            });
                                            
                                            
                                            let maskHTML =""
                                            if(data["mask"] == 0){
                                                maskHTML = '<label><input type="radio" name="mask" value="0" checked>On</label>'+
                                                             '<label><input type="radio" name="mask" value="1">No</label>'
                                            }else if(data["mask"]==1){
                                                maskHTML = '<label><input type="radio" name="mask" value="0">On</label>'+
                                                             '<label><input type="radio" name="mask" value="1" checked>No</label>'
                                            }
                                            
                                            chartSeq.innerHTML = 'No. '+data["seq"]
                                            userName.innerHTML = '이름: '+ data["name"]
                                            predictedAge.innerHTML = '추정 나이: '+ data["age"]
                                            temperature.innerHTML = '감지 온도: '+data["temp"]
                                            predictedGender.innerHTML = '성별 : '+genderHTML;
                                            useOfMask.innerHTML = '마스크:  '+maskHTML
                                            verifyBtn.innerHTML = "확인"
                                            chartImg.src= data["origin_img"];
                                            
                                            verifyBtn.addEventListener("click", function(){
                                                let className = ".item"+data["seq"]
                                                
                                
                                                let inputGender = predictedGender.querySelectorAll("input[name='gender']:checked")
                                                let inputMask = useOfMask.querySelectorAll("input[name='mask']:checked")
                                                
                                                
                                                
                                                let errMSG = document.querySelector(".errMSG");
                                                
                                                if(inputGender.length == 0){
                                                    errMSG.innerHTML="*성별을 확인하세요"
                                                }else{
                                                
                                                    
                                                    name = data["name"]
                                                    gender= inputGender[0].value == 0 ? "남성" : "여성";
                                                    mask = inputMask[0].value == 0 ? "On" : "Off";
                                                    temp = data["temp"]
                                                    age = data["age"];
                                                    
                                                    errMSG.innerHTML=""
                                                    
                                                    
                                                    let modal = document.querySelector(".modal");
                                                    let modalCancelBtn = document.querySelector(".modalCancelBtn");
                                                    let modalImg = document.querySelector(".modalImg")
                                                    let modalName = modal.querySelector(".modalName")
                                                    let modalAge = modal.querySelector(".modalAge")
                                                    let modalGen = modal.querySelector(".modalGen")
                                                    let modalTemp = modal.querySelector(".modalTemp")
                                                    let modalMask = modal.querySelector(".modalMask")
                                                    let modalNum = modal.querySelector(".modalNum")
                                                    
                                                    
                                                    modalImg.src = data["origin_img"]
                                                    modalNum.value = data["seq"]
                                                    modalName.innerHTML = "이름 :"+name
                                                    modalAge.innerHTML = "나이 :"+age
                                                    modalGen.innerHTML = "성별 :"+gender
                                                    modalTemp.innerHTML = "온도 :"+temp
                                                    modalMask.innerHTML = "마스크 :"+mask
                                                    
                                                    
                                                    modal.classList.add("modalOn")
                                                    modalCancelBtn.addEventListener("click", function(){
                                                    
                                                        modal.classList.remove("modalOn")
                                                    })
                                                    
                                                    
                                                    xhr = new XMLHttpRequest();
                                                    xhr.open("POST", "/getMembers", false);
                                                    xhr.onreadystatechange = function(){
                                                        if(xhr.readyState ==4){
                                                            if(xhr.status == 200){
                                                                
                                                                
                                                                _data = JSON.parse(this.responseText)
                                                                
                                                                let memberSelect = document.querySelector(".memberSelect")
                                                                let selectOptionText = "";
                                                                
                                                                for(key in _data){
                                                                    selectOptionText += "<option value='"+_data[key]["name"]+"'>"+_data[key]["name"]+"</option>"
                                                                }
                                                                memberSelect.innerHTML = selectOptionText;
                                                                let modalMemberName = document.querySelector(".modalMemberName")
                                                                let modalMemberAge = document.querySelector(".modalMemberAge")
                                                                let modalMemberGen = document.querySelector(".modalMemberGen")
                                                                let modalMemberEmail = document.querySelector(".modalMemberEmail")
                                                                let modalMemberImg = document.querySelector(".modalMemberImg")
                                                                
                                                                
                                                                modalMemberImg.src = _data["Unknown"]["img"]
                                                                modalMemberName.innerHTML = _data["Unknown"]["name"]
                                                                modalMemberAge.innerHTML = _data["Unknown"]["age"]
                                                                modalMemberGen.innerHTML = _data["Unknown"]["gender"]
                                                                modalMemberEmail.innerHTML = _data["Unknown"]["email"]
                                                                
                                                                memberSelect.addEventListener("change", function(){
                                                                    let _key = memberSelect.value
                                                                    modalMemberImg.src = _data[_key]["img"]
                                                                    modalMemberName.innerHTML = _data[_key]["name"]
                                                                    modalMemberAge.innerHTML = _data[_key]["age"]
                                                                    modalMemberGen.innerHTML = _data[_key]["gender"]
                                                                    modalMemberEmail.innerHTML = _data[_key]["email"]        
                                                                })
                                                                
                                                                let modalCheckBtn = document.querySelector(".modalCheckBtn");
                                                                modalCheckBtn.addEventListener("click", function(){
                                                                    
                                                                    sendData = {
                                                                        "seq" : modalNum.value ,
                                                                        "name" : modalMemberName.textContent,
                                                                        "age" : modalMemberAge.textContent,
                                                                        "gender" : modalMemberGen.textContent,
                                                                        "Email" : modalMemberEmail.textContent,
                                                                        "log" : chartLog.value
                                                                    }
                                                                    
                                                                    sendData = JSON.stringify(sendData)
                                                                    _xhr = new XMLHttpRequest();
                                                                    _xhr.open("POST", "/warningData", false);
                                                                    _xhr.onreadystatechange = function(){
                                                                        if(_xhr.readyState ==4){
                                                                            if(_xhr.status == 200){
                                                                                
                                                                                modal.classList.remove("modalOn")
                                                                                getDetectData()
                                                                                
                                                                                chartImg.src = "static/img/NoImage.jpg"
                                                                                chartSeq.innerHTML = ""
                                                                                userName.innerHTML = ""
                                                                                predictedAge.innerHTML = ""
                                                                                temperature.innerHTML = ""
                                                                                predictedGender.innerHTML = ""
                                                                                useOfMask.innerHTML = ""
                                                                                verifyBtn.innerHTML = ""
                                                                                chartLog.disabled=true
                                                                                chartLog.innerHTML=""
                                                                                    
                                                                            }else{
                                                                                alert("요청 실패: "+_xhr.status);
                                                                            }
                                                                        }
                                                                    }
                                                                    
                                                                    _xhr.setRequestHeader("Content-Type", "application/json");
                                                                    _xhr.send(sendData)
                                                                    
                                                                })
                                                                
                                                            }else{
                                                                alert("요청 실패: "+xhr.status);
                                                            }
                                                        }
                                                    }
                                                    
                                                    xhr.setRequestHeader("Content-Type", "application/json");
                                                    xhr.send()
                                                }
                                                
                                            });
                                           
                                            
                                           
                                        }else{
                                           alert("요청 실패: "+xhr.status);
                                        }
                                    }
                                }
                               
                                xhr.setRequestHeader("Content-Type", "application/json");
                                xhr.send(jsonData)
                            })
                        }
                    }
                }else{
                    alert("요청 실패: "+xhr.status);
                }
            }
        }
        
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(jsonData)
    }, 5000);
    

    playAlert;
    
    
}
