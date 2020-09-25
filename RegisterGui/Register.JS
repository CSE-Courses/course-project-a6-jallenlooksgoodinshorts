function checkEmail(email){
    if(!email.includes("@")){
        return false;
    }else{
        return true;
    }
}

function checkForm(){
    form = document.getElementById("registerDetails");
    if(form[0].value === "" && form[1].value === "" && form[2].value === "" && form[3].value === "" && form[4].value === ""){
        alert("please asd");
    }
}