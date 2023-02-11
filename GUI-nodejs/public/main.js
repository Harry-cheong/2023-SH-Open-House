function openConfirmationBox() {
  $("#confirmclearmodal").modal("show");
}

function clearAllCode(clearMemory = true) {
  $("#confirmclearmodal").modal("hide");
  if (clearMemory) {
    localStorage.setItem("codesequence", "");
  }
  var allBlocks = $("#codecontainer .block");
  for (var i = 0; i < allBlocks.length; i++) {
    if (allBlocks[i].id === "startblock") {
      continue;
    }
    $(allBlocks[i]).remove();
  }
}

function pullCodeSequenceToString() {
    var finalText = "["
    var allBlocks = $("#codecontainer .block")
    var loopIndentRemaining = 0;
    var ifIndentRemaining = 0;
    for(var i = 0; i < allBlocks.length; i++) {
        if (allBlocks[i].id === "startblock") {
            continue;
        }
        var id = allBlocks[i].id.split('_')[1];
        var val = $(`#${allBlocks[i].id} input`).val()
        if(id !== "w" && id !== "for" && id !== "if") {
            if(id === "kb") {
                finalText = finalText + id;
                if(loopIndentRemaining === 0) {
                    $("#errormodal .modal-body").text("Please place 'end loop' block within a loop")
                    $("#errormodal").modal("show")
                    return false;
                }
            } else {
                finalText = finalText + id + val;
            }
            if(ifIndentRemaining === 1 && loopIndentRemaining > 1) {
                finalText = finalText + ",]"; // ending IF, not ending LOOP
            } else if (ifIndentRemaining === 1 && loopIndentRemaining === 1) {
                finalText = finalText + ",],]"; // ending IF, ending LOOP
            } else if (ifIndentRemaining === 0 && loopIndentRemaining === 1) {
                finalText = finalText + ",]"; // ending LOOP, not ending IF
            } else if (ifIndentRemaining === 1 && loopIndentRemaining === 0) {
                finalText = finalText + ",]";  // ending IF, not ending LOOP
            } 
            if (i !== allBlocks.length-1) {
                finalText = finalText + ",";
            }

            if (ifIndentRemaining > 0 && loopIndentRemaining > 0) {
                if(ifIndentRemaining === 1) {loopIndentRemaining -= 1;}
                ifIndentRemaining -= 1;
            } else if (loopIndentRemaining > 0) {
                loopIndentRemaining -= 1;
            } else if (ifIndentRemaining > 0) {
                ifIndentRemaining -= 1;
            }
        } else if (id === "w" || id === "for") {
            loopIndentRemaining = parseInt($(allBlocks[i]).attr("data-numblocks"))
            if (id === "w") {
                finalText = finalText + "w(),[,"
            } else {
                finalText = finalText + "for(" + $(`#${allBlocks[i].id} input`).val() + "),[,"
            }
        } else if (id === "if") {
            ifIndentRemaining = parseInt($(allBlocks[i]).attr("data-numblocks"))
            finalText = finalText + "if(" + $(`#${allBlocks[i].id} .selectvariable`).val() + $(`#${allBlocks[i].id} .selectcondition`).val() + $(`#${allBlocks[i].id} input`).val() + "),[,"
        }
        
    }
    finalText = finalText + "]"
    if(loopIndentRemaining > 0 || ifIndentRemaining > 0) {
        $("#errormodal .modal-body").text("Please do not leave loops/conditionals that require blocks. Press '-' button on loop/conditional if no more blocks are needed.")
        $("#errormodal").modal("show")
        return false;
    }
    return finalText;
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
        if (id === "w" || id === "for") {
            finalText = finalText + id + "_" + val + "_" + $(allBlocks[i]).attr("data-numblocks");
        } else if (id === "if") {
            finalText = finalText + id + "_" + val + "_" + $(allBlocks[i]).attr("data-numblocks") + "_" + $(`#${allBlocks[i].id} .selectvariable`).val() + "_" + $(`#${allBlocks[i].id} .selectcondition`).val();
        } else {
            finalText = finalText + id + "_" + val;
        }
        
        if (i !== allBlocks.length-1) {
            finalText = finalText + "-";
        }
    }
    localStorage.setItem("codesequence", finalText)
}

function renderLocalStorage() {
    clearAllCode(clearMemory = false)
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
        $(`#${window.codeCounter-1}_${key} input`).val(seq[i].split("_")[1])
        if(key === "w" || key === "for" || key === "if") {
            $(`#${window.codeCounter-1}_${key}`).attr("data-numblocks", parseInt(seq[i].split("_")[2]))
        }
        if (key === "if") {
            $(`#${window.codeCounter-1}_${key} .selectvariable`).val(seq[i].split("_")[3])
            $(`#${window.codeCounter-1}_${key} .selectcondition`).val(seq[i].split("_")[4])
        }
    }}
}

function runCode() {
    var seq = pullCodeSequenceToString();
    if (!!seq)  {
        updateLocalStorage()
        updateModal("Sending");
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                reloadToCompletion()
            }
        };
        xhttp.open("POST", "/formdata", true);
        xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xhttp.send(`cmd=${seq}`);  
    }  else {

    }
}

function updateModal(state) {
  if (state === "Sending") {
    $("#runmodal").modal("show");
    $("#runmodal h1").text("Code sending...");
    $("#runmodal button").attr("disabled", false);
    $("#runmodal .loader").addClass("green");
    $("#runmodal .loader").removeClass("red");
    $("#runmodal button").addClass("btn-danger");
    $("#runmodal button").removeClass("btn-secondary");
    $("#stopimg").addClass("d-none");
    $("#playimg").removeClass("d-none");
  } else if (state === "Running") {
    $("#runmodal").modal("show");
    $("#runmodal h1").text("Code running...");
    $("#runmodal button").attr("disabled", false);
    $("#runmodal .loader").addClass("green");
    $("#runmodal .loader").removeClass("red");
    $("#runmodal button").addClass("btn-danger");
    $("#runmodal button").removeClass("btn-secondary");
    $("#stopimg").addClass("d-none");
    $("#playimg").removeClass("d-none");
  } else if (state === "Stopping") {
    $("#runmodal").modal("show");
    $("#runmodal h1").text("Code stopping...");
    $("#runmodal button").attr("disabled", true);
    $("#runmodal .loader").addClass("red");
    $("#runmodal .loader").removeClass("green");
    $("#runmodal button").addClass("btn-secondary");
    $("#runmodal button").removeClass("btn-danger");
    $("#playimg").addClass("d-none");
    $("#stopimg").removeClass("d-none");
  } else if (state === "Clear") {
    $("#runmodal").modal("hide");
  } else if (state === "Failed") {
    setTimeout(function () {
      $("#runmodal").modal("hide");
      $("#failmodal").modal("show");
    }, 500);
  }
}

function stopCode() {
  updateModal("Stopping");
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      reloadToCompletion();
    }
  };
  xhttp.open("POST", "/interruptexecution", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send();
}

window.status = "";

function reloadToCompletion() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      newStatus = this.responseText;
      if (window.status !== newStatus) {
        updateModal(newStatus);
      }
      if (newStatus === "Clear") {
        updateModal("Clear");
      }

      window.status = newStatus;

      if (
        window.status === "Running" ||
        window.status === "Stopping" ||
        window.status === "Sending" ||
        window.status === "Failed"
      ) {
        setTimeout(function () {
          reloadToCompletion();
        }, 3000);
      }
      console.log(window.status);
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
  var allBlocks = $("#codecontainer .block");
  for (var i = 0; i < allBlocks.length; i++) {
    var blockID = allBlocks[i].id;
    var val = parseInt($(`#${blockID} input`).val());
    if (blockID === "startblock") {
        continue;
    }
    if (val > 99999 || val < 0 || isNaN(val)) {
      $("#run").addClass("disabled");
      $("#run").attr("disabled", true);
      $(`#${blockID} input`).addClass("warning");
      return;
    } else {
        $(`#${blockID} input`).removeClass("warning");
    }
  }
  $("#run").removeClass("disabled");
  $("#run").attr("disabled", false);
  return;
}

function verifyInput(e) {
  var value = parseInt(e.currentTarget.value);
  var input = e.currentTarget;
  var blockID = $(input).parent().parent().parent().attr("id");
  if (value > 99999 || value < 0 || isNaN(value)) {
    $(`#${blockID} input`).addClass("warning");
  } else {
    $(`#${blockID} input`).removeClass("warning");
  }
  verifyAllInputs();
  updateLocalStorage();
}

function verifySequence() {
  var allBlocks = $("#codecontainer .block");
  if (allBlocks.length === 1) {
    $("#run").addClass("disabled");
    $("#run").attr("disabled", true);
  } else if (allBlocks.length > 1) {
    $("#run").removeClass("disabled");
    $("#run").attr("disabled", false);
  } else {
    throw new Error("Impossible value of length reached");
  }
}

function findBlock(blockNumber) {
  var allBlocks = $("#codecontainer .block");
  for (var i = 0; i < allBlocks.length; i++) {
    var val = parseInt(allBlocks[i].id.split("_")[0]);
    if (val === blockNumber) {
      return allBlocks[i].id;
    }
  }
  return "not found";
}

function renderLoopIndentation(revertIfError = true) {
    var allBlocks = $("#codecontainer .block")
    var loopIndentRemaining = 0
    var ifIndentRemaining = 0
    for (var i = 0; i < allBlocks.length; i++) {
        blockID = allBlocks[i].id
        var blocktype = blockID.split("_")[1]
        if (blocktype === "w" || blocktype === "for") {
            if (loopIndentRemaining > 0 && revertIfError) {
                renderLocalStorage()
                renderLoopIndentation()
                $("#errormessage").modal("show")
                return;
            } else if (ifIndentRemaining > 0 && revertIfError) {
                renderLocalStorage()
                renderLoopIndentation()
                $("#errormessage").modal("show")
            } else {
                loopIndentRemaining += parseInt($(allBlocks[i]).attr("data-numblocks"))
                $(allBlocks[i]).removeClass("loopindent");
                $(allBlocks[i]).removeClass("ifindent");
                $(allBlocks[i]).removeClass("ifloopindent");
            }
        } else if (blocktype === "if") {
            if (ifIndentRemaining > 0 && revertIfError) {
                renderLocalStorage()
                renderLoopIndentation()
                $("#errormessage").modal("show")
            } else {
                ifIndentRemaining += parseInt($(allBlocks[i]).attr("data-numblocks"))
                if (loopIndentRemaining > 0) { 
                    $(allBlocks[i]).addClass("loopindent");
                    $(allBlocks[i]).removeClass("ifindent");
                    $(allBlocks[i]).removeClass("ifloopindent");
                    // loopIndentRemaining -= 1;
                } else {
                    $(allBlocks[i]).removeClass("loopindent");
                    $(allBlocks[i]).removeClass("ifindent");
                    $(allBlocks[i]).removeClass("ifloopindent");
                }
            }
        } else {
            if (loopIndentRemaining > 0 && ifIndentRemaining > 0) {
                $(allBlocks[i]).removeClass("loopindent");
                $(allBlocks[i]).removeClass("ifindent");
                $(allBlocks[i]).addClass("ifloopindent");
                if(ifIndentRemaining === 1) {
                    loopIndentRemaining -= 1;
                }
                // loopIndentRemaining -= 1;
                ifIndentRemaining -= 1;
            } else if (loopIndentRemaining > 0) {
                $(allBlocks[i]).addClass("loopindent");
                $(allBlocks[i]).removeClass("ifindent");
                $(allBlocks[i]).removeClass("ifloopindent");
                loopIndentRemaining -= 1;
            } else if (ifIndentRemaining > 0) {
                $(allBlocks[i]).removeClass("loopindent");
                $(allBlocks[i]).addClass("ifindent");
                $(allBlocks[i]).removeClass("ifloopindent");
                ifIndentRemaining -= 1;
            } else {
                $(allBlocks[i]).removeClass("loopindent");
                $(allBlocks[i]).removeClass("ifindent");
                $(allBlocks[i]).removeClass("ifloopindent");
            }
        }
    }
}

function addlayer(e) {
  var btn = e.currentTarget;
  var block = $(btn).parent().parent();
  var currentlayer = $(block).attr("data-numblocks");
  $(block).attr("data-numblocks", parseInt(currentlayer) + 1);
  renderLoopIndentation();
  updateLocalStorage();
}

function removelayer(e) {
  var btn = e.currentTarget;
  var block = $(btn).parent().parent();
  var currentlayer = $(block).attr("data-numblocks");
  if (currentlayer > 1) {
    $(block).attr("data-numblocks", parseInt(currentlayer) - 1);
  }
  renderLoopIndentation();
  updateLocalStorage();
}

function moveUp(e) {
  var btn = e.currentTarget;
  var block = $(btn).parent().parent();
  var blockID = $(block).attr("id");
  var blockNumber = parseInt(blockID.split("_")[0]);
  if (blockNumber === 0) {
    return;
  } else {
    blockAboveID = findBlock(blockNumber - 1);
    $(`#${blockAboveID}`).before($(`#${blockID}`));
    $(`#${blockAboveID}`).attr(
      "id",
      `temp_${blockNumber}_${blockAboveID.split("_")[1]}`
    );
    $(`#${blockID}`).attr(
      "id",
      `temp_${blockNumber - 1}_${blockID.split("_")[1]}`
    );
    $(`#temp_${blockNumber}_${blockAboveID.split("_")[1]}`).attr(
      "id",
      `${blockNumber}_${blockAboveID.split("_")[1]}`
    );
    $(`#temp_${blockNumber - 1}_${blockID.split("_")[1]}`).attr(
      "id",
      `${blockNumber - 1}_${blockID.split("_")[1]}`
    );
  }
  renderLoopIndentation();
  updateLocalStorage();
}

function moveDown(e) {
  var btn = e.currentTarget;
  var block = $(btn).parent().parent();
  var blockID = $(block).attr("id");
  var blockNumber = parseInt(blockID.split("_")[0]);
  if (blockNumber === $("#codecontainer .block").length - 2) {
    return;
  } else {
    blockBelowID = findBlock(blockNumber + 1);
    $(`#${blockBelowID}`).after($(`#${blockID}`));
    $(`#${blockBelowID}`).attr(
      "id",
      `temp_${blockNumber}_${blockBelowID.split("_")[1]}`
    );
    $(`#${blockID}`).attr(
      "id",
      `temp_${blockNumber + 1}_${blockID.split("_")[1]}`
    );
    $(`#temp_${blockNumber}_${blockBelowID.split("_")[1]}`).attr(
      "id",
      `${blockNumber}_${blockBelowID.split("_")[1]}`
    );
    $(`#temp_${blockNumber + 1}_${blockID.split("_")[1]}`).attr(
      "id",
      `${blockNumber + 1}_${blockID.split("_")[1]}`
    );
  }
  renderLoopIndentation();
  updateLocalStorage();
}

function trash(e) {
  var btn = e.currentTarget;
  $(btn).parent().parent().remove();

  counter = 0;
  var allBlocks = $("#codecontainer .block");
  for (var i = 0; i < allBlocks.length; i++) {
    var origID = allBlocks[i].id;
    if (origID === "startblock") {
      continue;
    }
    var newID = `${counter}_${allBlocks[i].id.split("_")[1]}`;
    $(`#${origID}`).attr("id", newID);
    counter += 1;
  }
  window.codeCounter = counter;
  verifySequence();
  renderLoopIndentation();
  updateLocalStorage();
}
function addToCode(key) {
    contents = $(`#${key}`).html();
    copy = $(`<button id="${window.codeCounter}_${key}" class="block fillblock ${allBlocks[key].color}"></button>`);
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
    if (key === "w" || key === "for" || key === "if") {
        $(`#${window.codeCounter}_${key}`).attr('data-numblocks', 1);
        $(`#${window.codeCounter}_${key} button.addlayer`).on('click', function(e) {
            addlayer(e);
        });
        $(`#${window.codeCounter}_${key} button.removelayer`).on('click', function(e) {
            removelayer(e);
        });
    }

    if (key === "if") {
        var variable = $(`<select class="selectvariable" aria-label="Select variable">
        <option value="lr" selected>Light reflected (%)</option>
        <option value="ud">Obstacle distance (m)</option>
        </select>`)
        var condition = $(`<select class="selectcondition" aria-label="Select variable">
        <option value="<" selected>&#60;</option>
        <option value="<=">≤</option>
        <option value="==">=</option>
        <option value=">=">≥</option>
        <option value=">">&#62;</option>
        </select>`)
        condition.on("change", function() {
            updateLocalStorage();
        })
        variable.on("change", function() {
            updateLocalStorage();
        })
        $(`#${window.codeCounter}_${key} input`).before(condition)
        $(`#${window.codeCounter}_${key} .selectcondition`).before(variable)
    }
    window.codeCounter += 1;
    verifySequence();
    renderLoopIndentation()
    updateLocalStorage();
}

const allBlocks = {
    "f": {pretext: "Move forward ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot forward by degrees of wheel rotation", color: "orange"},
    "r": {pretext: "Turn right ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Turns the robot right by degrees of robot", color: "orange"},
    "l": {pretext: "Turn left ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot left by degrees of robot", color: "orange"},
    "b": {pretext: "Move backward ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot backward by degrees of wheel rotation", color: "orange"},
    "t": {pretext: "Line trace ", posttext: "°", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Moves the robot forward by tracing the line by degrees of wheel rotation", color: "orange"},
    "if": {pretext: "If ", posttext: "", inputRequired: true, info: "Executes code blocks within it if condition is fulfilled", color: "purple"},
    "w": {pretext: "Repeat continuously", posttext: "", inputRequired: false, info: "Repeats code blocks within it infinitely", color: "blue"},
    "for": {pretext: "Repeat ", posttext: "times", inputRequired: true, inputType: "number", max: 10000, min: 1, info: "Repeats code blocks within it a set number of times", color: "blue"},
    "kb": {pretext: "End loop", posttext: "", inputRequired: false, info: "Ends the loop", color: "orange"},
}

function renderAddBlocks() {
  for (const [key, value] of Object.entries(allBlocks)) {
    contents = $("#template").html();
    copy = $(
      `<button id="${key}" class="block addblock" onclick="addToCode('${key}')"></button>`
    );
    if (isOdd) {
      $("#allblocksleft").append(copy.append(contents));
    } else {
      $("#allblocksright").append(copy.append(contents));
    }
    isOdd = !isOdd;
    $(`#${key} .preblockname`).text(value.pretext);
    $(`#${key} .postblockname`).text(value.posttext);
    if (value.inputRequired) {
      $(`#${key} .blockdetail`).attr("type", value.inputType);
      $(`#${key} .blockdetail`).attr("min", value.min);
      $(`#${key} .blockdetail`).attr("max", value.max);
    } else {
      $(`#${key} .blockdetail`).addClass("d-none");
    }
    if(key === "if") {
        $(`#${key} input`).attr("placeholder", "...");
    }
    $(`#${key} .blockinfo`).attr("data-bs-title", value.info);
    $(`#${key}`).addClass(value.color);
  }
}

$(function () {
  reloadToCompletion();
  renderAddBlocks();
  $("body").tooltip({ selector: "[data-bs-toggle=tooltip]" });
  renderLocalStorage();
  renderLoopIndentation();
  verifyAllInputs();
  verifySequence();
});
