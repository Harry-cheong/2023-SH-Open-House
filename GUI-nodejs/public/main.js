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

$(function() {
    let status = $("#statusHolder").text().trim()
    console.log(status)
    if (status === "Running") {
        setTimeout(() => {
            location.reload()
        }, "1000")
          
    }
})