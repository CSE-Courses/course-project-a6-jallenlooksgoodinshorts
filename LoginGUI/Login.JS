function formatCred(cred){
    return {"username": cred[0].value, "password": cred[1].value};
}

function getCred() {
    credentials = document.getElementById("loginfrm");
    return formatCred(credentials);
}

function checkCred(username){
    if (!username.includes("@")){
        return false;
    }else {
        return true;
    }
}

function sendCred() {
    cred = getCred();
    //make sure this is a valid email
    if (!checkCred(cred["username"])){
        alert("Please enter a valid email");
    }
}