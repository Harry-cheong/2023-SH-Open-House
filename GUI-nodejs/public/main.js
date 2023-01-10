function openConfirmationBox() {
    $('#confirmclearmodal').modal('show'); 
}

function clearAllCode() {
    $('#confirmclearmodal').modal('hide'); 
    console.log("all code cleared")
}

function pullCodeSequenceToString() {
    finalText = ""
    var allBlocks = $("#codecontainer .block")
    for(var i = 0; i < allBlocks.length; i++) {
        var id = allBlocks[i].id.split('_')[1];
        console.log(allBlocks[i].id)
        var val = $(`#${allBlocks[i].id} input`).val()
        finalText = finalText + id + val;
        if (i !== allBlocks.length-1) {
            finalText = finalText + "-";
        }
    }
    console.log(finalText)
    $("#name").val(finalText)
}

function runCode() {
    pullCodeSequenceToString();
    // $("#runmodal").modal("show");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            reloadToCompletion()
        }
    };
    xhttp.open("POST", "/formdata", true);
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    // xhttp.send(`cmd=${$("#name").val()}`);    
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

// GUI rendering code blocks
let isOdd = true;
let codeCounter = 0;

function addToCode(key) {
    contents = $(`#${key}`).html();
    copy = $(`<button id="${codeCounter}_${key}" class="block"></button>`);
    $('#codecontainer').append(copy.append(contents));
    $(`#${codeCounter}_${key} input`).prop('disabled', false);
    $(`#${codeCounter}_${key} input`).on('input', function(e) {
        value = e.target.value
    });
    codeCounter += 1;
}

const allBlocks = {
    "fwd": {pretext: "Move forward ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1},
    "right": {pretext: "Turn right ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1},
    "left": {pretext: "Turn left ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1},
    "bwd": {pretext: "Move backward ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1},
}


$(function() {
    reloadToCompletion();
    for (const [key, value] of Object.entries(allBlocks)) {
        contents = $('#template').html();
        copy = $(`<button id="${key}" class="block" onclick="addToCode('${key}')"></button>`);
        if (isOdd) {
            $('#allblocksleft').append(copy.append(contents));
        } else {
            $('#allblocksright').append(copy.append(contents));
        }
        isOdd = !isOdd;
        $(`#${key} .preblockname`).text(value.pretext);
        $(`#${key} .postblockname`).text(value.posttext);
        if (value.inputRequired) {
            $(`#${key} .blockdetail`).attr('type', value.inputType);
            $(`#${key} .blockdetail`).attr('min', value.min);
            $(`#${key} .blockdetail`).attr('max', value.max);
        } else {
            $(`#${key} .blockdetail`).addClass('d-none');
        }
        
        console.log(`${key}: ${value}`);
    }
})
