function openConfirmationBox() {
    $('#confirmclearmodal').modal('show'); 
}

function clearAllCode() {
    $('#confirmclearmodal').modal('hide'); 
    console.log("all code cleared")
}

function runCode() {
    $('#codeform').submit()
    console.log("submitted")
}

function stopCode() {
    console.log("TODO: implement code interruption")
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
                } else if (newStatus === "Clear") {
                    $("#runmodal").modal("hide");
                }
            }

            window.status = newStatus;

            if (window.status === "Running") {
                setTimeout(function() {
                    reloadToCompletion()
                }, 5000)
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