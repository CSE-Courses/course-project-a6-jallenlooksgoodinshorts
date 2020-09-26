function validateForm(){
    form = document.getElementById("registerDetails");
    if(form[3].value === form[4].value){
        return true;
    }else{
        /*put here for testing will swap to nonintrusive status*/
        alert("Passwords are not identical");
        return false;
    }
}

function mainPage(){
    /*will send to main page*/
    alert("Sending to main Page");
}