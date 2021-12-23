
var maxSPDOutput = document.querySelector(".maxSPDValue");
var minSPDOutput = document.querySelector(".minSPDValue");
var kpOutput = document.querySelector(".kpValue");
var kiOutput = document.querySelector(".kiValue");
var kdOutput = document.querySelector(".kdValue");

var cancleBtn = document.querySelector('.cancleBtn');
var applyBtn = document.querySelector('.applyBtn');
var resetBtn = document.querySelector('.resetBtn');

var optionBtn = document.querySelector('.optionBtn');
var shutdownBtn = document.querySelector('.shutdownBtn');

var modalMinSPD = document.querySelector('.modalMinSPDRange');
var modalMaxSPD = document.querySelector('.modalMaxSPDRange');
var modalKp = document.querySelector('.modalKpRange');
var modalKi = document.querySelector('.modalKiRange');
var modalKd = document.querySelector('.modalKdRange');

var modalMinSPDOutput = document.querySelector('.modalMinSPDValue');
var modalMaxSPDOutput = document.querySelector('.modalMaxSPDValue');
var modalKpOutput = document.querySelector('.modalKpValue');
var modalKiOutput = document.querySelector('.modalKiValue');
var modalKdOutput = document.querySelector('.modalKdValue');

var modalMinSPDValue = modalMinSPD.value;
var modalMaxSPDValue = modalMaxSPD.value;
var modalKpValue = modalKp.value;
var modalKiValue = modalKi.value;
var modalKdValue = modalKd.value;

var cnt = 0;

var xhr;

const ajaxTest = function(data){
    xhr = new XMLHttpRequest();
    xhr.open("POST", "/getRobotData", true);
    jsonData = JSON.stringify(data)
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
}

applyBtn.addEventListener("click", function(){
    var modal = document.querySelector(".modal")
    modalMinSPDValue = modalMinSPD.value;
    modalMaxSPDValue = modalMaxSPD.value;
    modalKpValue = modalKp.value;
    modalKiValue = modalKi.value;
    modalKdValue = modalKd.value;

    maxSPDOutput.innerHTML = modalMaxSPDValue;
    minSPDOutput.innerHTML = modalMinSPDValue;
    kpOutput.innerHTML = modalKpValue;
    kiOutput.innerHTML = modalKiValue;
    kdOutput.innerHTML = modalKdValue;

    data = {"maxSPD": modalMaxSPDValue, 
             "minSPD": modalMinSPDValue,
             "kp": modalKpValue,
             "ki": modalKiValue,
             "kd": modalKdValue};
    console.log(data);
    ajaxTest(data);
    alert("Apply Commit");
    modal.style = "display:none"
    if(cnt == 1){
        cnt = 0;
    }
})

cancleBtn.addEventListener("click", function(){
    var modal = document.querySelector(".modal")
    modalMinSPD.value = modalMinSPDValue;
    modalMaxSPD.value = modalMaxSPDValue;
    modalKp.value = modalKpValue;
    modalKi.value = modalKiValue;
    modalKd.value = modalKdValue;
    modal.style = "display:none";

    if(cnt == 1){
        cnt = 0;
    }
})

optionBtn.addEventListener("click", function(){
    if(cnt == 0){
        var modal = document.querySelector(".modal")
        modalMinSPDValue = modalMinSPD.value;
        modalMaxSPDValue = modalMaxSPD.value;
        modalKpValue = modalKp.value;
        modalKiValue = modalKi.value;
        modalKdValue = modalKd.value;

        modalMinSPDOutput.innerHTML = modalMinSPDValue;
        modalMaxSPDOutput.innerHTML = modalMaxSPDValue;
        modalKpOutput.innerHTML = modalKpValue;
        modalKiOutput.innerHTML = modalKiValue;
        modalKdOutput.innerHTML = modalKdValue;
        
        modal.style = "display:block";
        cnt++;
    }
})

shutdownBtn.addEventListener("click", function(){
    location.href="/"
})


modalMinSPD.addEventListener("mousedown", function(){
    this.addEventListener("mousemove", function(){
        modalMinSPDOutput.innerHTML = modalMinSPD.value;
    })
})

modalMaxSPD.addEventListener("mousedown", function(){
    this.addEventListener("mousemove", function(){
        modalMaxSPDOutput.innerHTML = modalMaxSPD.value;
    })
})

modalKp.addEventListener("mousedown", function(){
    this.addEventListener("mousemove", function(){
        modalKpOutput.innerHTML = modalKp.value;
    })
})

modalKi.addEventListener("mousedown", function(){
    this.addEventListener("mousemove", function(){
        modalKiOutput.innerHTML = modalKi.value;
    })
})

modalKd.addEventListener("mousedown", function(){
    this.addEventListener("mousemove", function(){
        modalKdOutput.innerHTML = modalKd.value;
    })
})
