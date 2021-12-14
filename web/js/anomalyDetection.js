
var c_target = document.querySelectorAll(".tableData");

c_target.forEach(function(target,index, addr,){
    target.addEventListener("click",function(){
        alert("작동");
        target.classList.toggle("moreDataEvent");
    })
})
