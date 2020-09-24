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

function sendJSON(json) {
    xml = new XMLHttpRequest();
    url = "https://httpbin.org/post "; //PLACEHOLDER UNTIL I KNOW WHERE TO SEND IT
    xml.open("POST", url, true);
    xml.setRequestHeader("Content-Type", "application/json");
    xml.onreadystatechange = function () {
        if (xml.readyState === 4 && xml.status === 200){
            console.log(JSON.parse(xml.responseText)); //JUST A TEST, NEEDS TO BE DELETED IN IMPLEMENTATION
            //HERE IS WHERE WE REACT TO THE SERVERS MESSAGE
        }
    };
    xml.send(json);
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