
window.onload = function(){
    
    
    var shutdownBtn = document.querySelector('.shutdownBtn');
    var chartTable = document.querySelector(".chartTable");
    var checkNumResult = document.querySelector(".checkNumResult");
    var noMaskNumResult = document.querySelector(".noMaskNumResult");
    var checkNumEffect = document.querySelector(".checkNumEffect");
    var noMaskNumEffect = document.querySelector(".noMaskNumEffect");
    
    const getDetectData = function(){
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/getDetectData", false);
        xhr.onreadystatechange = function(){
            if(xhr.readyState ==4){
                if(xhr.status == 200){
                    console.log("전송 성공")
                    data = JSON.parse(this.responseText)
                    htmlText = ""
                    for(key in data){
                        value = data[key]
                        htmlText +='<ul class="items"> <li>'+value["seq"]+
                            '</li><li>'+value["temp"]+
                            '</li><li>'+value["mask"]+
                            '</li><li>'+value["shootingData"]+
                            '</li><li><div class="infoBtn" data-seq='+value["seq"]+
                            '>▶</div></li></ul>'
                    }
                    chartTable.innerHTML = htmlText
                    var infoBtns = document.querySelectorAll(".infoBtn");
                    infoBtns.forEach(function(item,index,arr){
                        console.log(item.dataset.seq)
                        
                        item.addEventListener("click", function(){
                           xhr = new XMLHttpRequest();
                           xhr.open("POST", "/getInfoData", false);
                           jsonData = {"seq":item.dataset.seq}
                           jsonData = JSON.stringify(jsonData)
                           xhr.onreadystatechange = function(){
                               if(xhr.readyState ==4){
                                   if(xhr.status == 200){
                                       console.log("전송 성공")
                                       
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
        console.log("??3")
        xhr = new XMLHttpRequest();
        xhr.open("POST", "/getMaskPlotData", true);
        xhr.onreadystatechange = function(){
            if(xhr.readyState ==4){
                if(xhr.status == 200){
                    console.log("전송 성공")
                    console.log(this.responseText)
                    data = JSON.parse(this.responseText)
                    
                    Highcharts.setOptions({
                      colors: ['#01BAF2', '#71BF45', '#FAA74B']
                    });  
                    Highcharts.chart('maskUsagePlot', {
                        chart: {
                          plotBackgroundColor: '#FCAFC0',
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
                            name: 'Mask('+data["true"]+')',
                            y: data["true"],
                          }, {
                            name: 'No Mask('+data["false"]+')',
                            y: data["false"],
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
                       console.log("전송 성공")
                       console.log(this.responseText)
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
    
    
    
    
    
    shutdownBtn.addEventListener("click", function(){
        location.href="/"
    })
    
    
    
    
}
