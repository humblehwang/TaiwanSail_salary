var SubmitBtn = document.getElementById("submit");
var ID = document.getElementById("ID");

SubmitBtn.addEvetListener("click",function(e)){
    e.preventDefault();
    console.log(ID.value);
}