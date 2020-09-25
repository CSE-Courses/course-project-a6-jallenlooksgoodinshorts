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

function sendJSON(input) {
    xml = new XMLHttpRequest();
    url = "https://httpbin.org/post "; //PLACEHOLDER UNTIL I KNOW WHERE TO SEND IT
    xml.open("POST", url, true);
    xml.setRequestHeader("Content-Type", "application/json");
    xml.onreadystatechange = function () {
        if (xml.readyState === 4 && xml.status === 200){
            console.log(JSON.parse(xml.responseText)["data"]); //Remove On Release
            data = JSON.parse(xml.responseText)["data"];
            login(input, data);
        }
    };
    xml.send(input);
}

function login(input, json) {
    //Set What the Server Responds With and rejects
    if (input === json){
        window.location.replace("ConfirmLogin\\LoginConfirmed.html");
    }else{
        alert("Login Failed");
    }
}

function sendCred() {
    cred = getCred();
    //make sure this is a valid email
    if (!checkCred(cred["username"])){
        alert("Please enter a valid email");
    }else {
        data = JSON.stringify(cred);
        sendJSON(data);
    }
}