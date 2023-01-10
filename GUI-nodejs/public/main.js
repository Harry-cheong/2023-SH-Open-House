function openConfirmationBox() {
    $('#confirmclearmodal').modal('show'); 
}

function clearAllCode() {
    $('#confirmclearmodal').modal('hide'); 
    console.log("all code cleared")
}

function runCode() {
    $("#runmodal").modal("show");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            reloadToCompletion()
        }
    };
    xhttp.open("POST", "/formdata", true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.send(`cmd=${$("#name").val()}`);    
}

function stopCode() {
    $("#runmodal").modal("hide");
    $("#stopmodal").modal("show");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            reloadToCompletion()
        }
    };
    xhttp.open("POST", "/interruptexecution", true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.send();    
}

window.status = ""

function reloadToCompletion() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            newStatus = this.responseText;

            if (window.status !== newStatus) {
                if(newStatus === "Running") {
                    $("#runmodal").modal("show");
                } 
                else if (newStatus === "Stopping") {
                    $("#runmodal").modal("hide");
                    $("#stopmodal").modal("show");
                }
            }

            if (newStatus === "Clear") {
                $("#runmodal").modal("hide");
                $("#stopmodal").modal("hide");
            }

            window.status = newStatus;

            if (window.status === "Running" || window.status === "Stopping") {
                setTimeout(function() {
                    reloadToCompletion()
                }, 1000)
            }
            console.log(window.status)
        }
    };
    xhttp.open("GET", "/runstatus", true);
    xhttp.send();    
}

$(function() {
    reloadToCompletion();
})