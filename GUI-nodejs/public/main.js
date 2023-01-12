function openConfirmationBox() {
    $('#confirmclearmodal').modal('show'); 
}

function clearAllCode() {
    $('#confirmclearmodal').modal('hide'); 
    localStorage.setItem("codesequence", "")
    var allBlocks = $("#codecontainer .block")
    for(var i = 0; i < allBlocks.length; i++) {
        if (allBlocks[i].id === "startblock") {
            continue;
        }
        $(allBlocks[i]).remove();
    }
}

function pullCodeSequenceToString() {
    var finalText = ""
    var allBlocks = $("#codecontainer .block")
    for(var i = 0; i < allBlocks.length; i++) {
        if (allBlocks[i].id === "startblock") {
            continue;
        }
        var id = allBlocks[i].id.split('_')[1];
        var val = $(`#${allBlocks[i].id} input`).val()
        finalText = finalText + id + val;
        if (i !== allBlocks.length-1) {
            finalText = finalText + ",";
        }
    }
    $("#name").val(`[${finalText}]`)
}
function updateLocalStorage() {
    var finalText = ""
    var allBlocks = $("#codecontainer .block")
    for(var i = 0; i < allBlocks.length; i++) {
        if (allBlocks[i].id === "startblock") {
            continue;
        }
        var id = allBlocks[i].id.split('_')[1];
        var val = $(`#${allBlocks[i].id} input`).val()
        finalText = finalText + id + "_" + val;
        if (i !== allBlocks.length-1) {
            finalText = finalText + "-";
        }
    }
    localStorage.setItem("codesequence", finalText)
}

function renderLocalStorage() {
    window.counter = 0;
    seq = localStorage.getItem("codesequence").split("-")
    if(seq.length > 0) {
    for(var i = 0; i < seq.length; i++) {
        let key = seq[i].split("_")[0]
        try {
            addToCode(key); 
        }  catch {
            // jquery throws a funny error if not caught -> this has no implications on functionality
        }
        $(`#${window.codeCounter-1}_${key} input`).val(parseInt(seq[i].split("_")[1]))
    }}
    
}

function runCode() {
    pullCodeSequenceToString();
    updateLocalStorage()
    console.log("update modal to sending")
    updateModal("Sending");
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

function updateModal(state) {
    if(state === "Sending") {
        $("#runmodal").modal("show");
        $("#runmodal h1").text("Code sending...");
        $("#runmodal button").attr("disabled", false);
        $("#runmodal .loader").addClass("green");
        $("#runmodal .loader").removeClass("red");
        $("#runmodal button").addClass("btn-danger");
        $("#runmodal button").removeClass("btn-secondary");
        $("#stopimg").addClass("d-none")
        $("#playimg").removeClass("d-none")
    } else if(state === "Running") {
        $("#runmodal").modal("show");
        $("#runmodal h1").text("Code running...");
        $("#runmodal button").attr("disabled", false);
        $("#runmodal .loader").addClass("green");
        $("#runmodal .loader").removeClass("red");
        $("#runmodal button").addClass("btn-danger");
        $("#runmodal button").removeClass("btn-secondary");
        $("#stopimg").addClass("d-none")
        $("#playimg").removeClass("d-none")
    } else if (state === "Stopping") {
        $("#runmodal").modal("show");
        $("#runmodal h1").text("Code stopping...");
        $("#runmodal button").attr("disabled", true);
        $("#runmodal .loader").addClass("red");
        $("#runmodal .loader").removeClass("green");
        $("#runmodal button").addClass("btn-secondary");
        $("#runmodal button").removeClass("btn-danger");
        $("#playimg").addClass("d-none")
        $("#stopimg").removeClass("d-none")
    } else if (state === "Clear") {
        $("#runmodal").modal("hide");
    } else if (state === "Failed") {
        setTimeout(function() {
            $("#runmodal").modal("hide");
            $("#failmodal").modal("show");
        }, 500)
        
    }
}

function stopCode() {
    updateModal("Stopping");
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
                updateModal(newStatus)
            }
            if (newStatus === "Clear") {
                updateModal("Clear")
            }

            window.status = newStatus;

            if (window.status === "Running" || window.status === "Stopping" || window.status === "Sending" || window.status === "Failed") {
                setTimeout(function() {
                    reloadToCompletion()
                }, 3000)
            }
            console.log(window.status)
        }
    };
    xhttp.open("GET", "/runstatus", true);
    xhttp.send();    
}

// GUI rendering code blocks
let isOdd = true;
window.codeCounter = 0;
window.errors = 0;

function verifyAllInputs() {
    var allBlocks = $("#codecontainer .block")
    for(var i = 0; i < allBlocks.length; i++) {
        var blockID = allBlocks[i].id    
        var val = $(`#${blockID} input`).val()
        if (val > 99999 || val < 1) {
            $("#run").addClass("disabled")
            $("#run").attr("disabled", true)
            return;
        }
    }
    $("#run").removeClass("disabled")
    $("#run").attr("disabled", false)
    return;
}

function verifyInput(e) {
    var value = e.currentTarget.value;
    var input = e.currentTarget;
    var blockID = $(input).parent().parent().parent().attr("id")
    if (value > 99999) {
        $(`#${blockID} .warning`).removeClass("d-none");
        $(`#${blockID} .warning`).text("! Value has to be smaller than 100000");
    } else if (value < 1) {
        $(`#${blockID} .warning`).removeClass("d-none");
        $(`#${blockID} .warning`).text("! Value has to be larger than 0");
    } else {
        $(`#${blockID} .warning`).addClass("d-none");
    }
    verifyAllInputs()
    updateLocalStorage()
}

function verifySequence() {
    var allBlocks = $("#codecontainer .block")
    if (allBlocks.length === 1) {
        $("#run").addClass("disabled")
        $("#run").attr("disabled", true)
    } else if (allBlocks.length > 1) {
        $("#run").removeClass("disabled")
        $("#run").attr("disabled", false)
    } else {
        throw new Error("Impossible value of length reached")
    }
}

function findBlock(blockNumber) {
    var allBlocks = $("#codecontainer .block")
    for(var i = 0; i < allBlocks.length; i++) {
        var val = parseInt(allBlocks[i].id.split("_")[0])
        if (val === blockNumber) {
            return allBlocks[i].id;
        }
    }
    return "not found";
}

function moveUp(e) {
    var btn = e.currentTarget;
    var block = $(btn).parent().parent();
    var blockID = $(block).attr("id")
    var blockNumber = parseInt(blockID.split("_")[0])
    if (blockNumber === 0) {
        return;
    } else {
        blockAboveID = findBlock(blockNumber-1)
        $(`#${blockAboveID}`).before($(`#${blockID}`))
        $(`#${blockAboveID}`).attr("id", `temp_${blockNumber}_${blockAboveID.split("_")[1]}`)
        $(`#${blockID}`).attr("id", `temp_${blockNumber-1}_${blockID.split("_")[1]}`)
        $(`#temp_${blockNumber}_${blockAboveID.split("_")[1]}`).attr("id", `${blockNumber}_${blockAboveID.split("_")[1]}`)
        $(`#temp_${blockNumber-1}_${blockID.split("_")[1]}`).attr("id", `${blockNumber-1}_${blockID.split("_")[1]}`)
    }
    updateLocalStorage()
}

function moveDown(e) {
    var btn = e.currentTarget;
    var block = $(btn).parent().parent();
    var blockID = $(block).attr("id")
    var blockNumber = parseInt(blockID.split("_")[0])
    if (blockNumber === $("#codecontainer .block").length-2) {
        return;
    } else {
        blockBelowID = findBlock(blockNumber+1)
        $(`#${blockBelowID}`).after($(`#${blockID}`))
        $(`#${blockBelowID}`).attr("id", `temp_${blockNumber}_${blockBelowID.split("_")[1]}`)
        $(`#${blockID}`).attr("id", `temp_${blockNumber+1}_${blockID.split("_")[1]}`)
        $(`#temp_${blockNumber}_${blockBelowID.split("_")[1]}`).attr("id", `${blockNumber}_${blockBelowID.split("_")[1]}`)
        $(`#temp_${blockNumber+1}_${blockID.split("_")[1]}`).attr("id", `${blockNumber+1}_${blockID.split("_")[1]}`)
    }
    updateLocalStorage()
}

function trash(e) {
    var btn = e.currentTarget;
    $(btn).parent().parent().remove()

    counter = 0
    var allBlocks = $("#codecontainer .block")
    for(var i = 0; i < allBlocks.length; i++) {
        var origID = allBlocks[i].id
        if (origID === "startblock") {
            continue;
        }
        var newID = `${counter}_${allBlocks[i].id.split('_')[1]}`;
        $(`#${origID}`).attr("id", newID);
        counter += 1;
    }
    window.codeCounter = counter;
    verifySequence()
    updateLocalStorage()
}
function addToCode(key) {
    contents = $(`#${key}`).html();
    copy = $(`<button id="${window.codeCounter}_${key}" class="block fillblock"></button>`);
    $('#codecontainer').append(copy.append(contents));
    $(`#${window.codeCounter}_${key} input`).prop('disabled', false);
    $(`#${window.codeCounter}_${key} input`).val(100);
    $(`#${window.codeCounter}_${key} input`).on('input', function(e) {
        verifyInput(e);
    });
    $(`#${window.codeCounter}_${key} button.up`).on('click', function(e) {
        moveUp(e);
    });
    $(`#${window.codeCounter}_${key} button.down`).on('click', function(e) {
        moveDown(e);
    });
    $(`#${window.codeCounter}_${key} button.trash`).on('click', function(e) {
        trash(e);
    });
    window.codeCounter += 1;
    verifySequence();
    updateLocalStorage();
}

const allBlocks = {
    "f": {pretext: "Move forward ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot forward by degrees of wheel rotation"},
    "r": {pretext: "Turn right ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Turns the robot right by degrees of robot"},
    "l": {pretext: "Turn left ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot left by degrees of robot"},
    "b": {pretext: "Move backward ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot backward by degrees of wheel rotation"},
    "lt": {pretext: "Line trace ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot forward by tracing the line by degrees of wheel rotation"},
}


$(function() {
    reloadToCompletion();
    for (const [key, value] of Object.entries(allBlocks)) {
        contents = $('#template').html();
        copy = $(`<button id="${key}" class="block addblock" onclick="addToCode('${key}')"></button>`);
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
        $(`#${key} .blockinfo`).attr("data-bs-title", value.info);
    }
    
    $("body").tooltip({ selector: '[data-bs-toggle=tooltip]' });
    verifySequence()
    try {
        renderLocalStorage();
    } catch (error) {
        localStorage.setItem("codesequence", "");
        renderLocalStorage();
    }
})
