const jsonSender = document.getElementById("drag_and_drop_json");
const imgSender = document.getElementById("drag_and_drop_img");
const sendFileButton = document.getElementById('sendFileBtn')


sendFileButton.addEventListener('click', () => {

    const inputFile = document.getElementById('senderFiles')

    let data = new FormData()
    data.append('file', inputFile.files[0])
    data.append('user', 'hubot')
    fetch('http://127.0.0.1:5000/sendimg', {
        method: 'POST',
        body: data
    })
})


function sendImg(json){
    fetch("http://127.0.0.1:5000/sendimg", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(json)
    }).then(res => {
        console.log("Re quest complete! response:", res);
    });
}

function sendJson(json){
    fetch("http://127.0.0.1:5000/sendjson", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(json)
    }).then(res => {
        console.log("Re quest complete! response:", res);
    });
}



jsonSender.addEventListener("dragover", function(event) {
    event.preventDefault(); // отменяем действие по умолчанию
}, false);
jsonSender.addEventListener("drop", function(event) {
    // отменяем действие по умолчанию
    event.preventDefault();
    console.log('DROP')

    let files = event.dataTransfer.files
    let len = files.length
    let reader = new FileReader();
    console.log(event.target.result);
    reader.readAsText(files[0]);
    reader.onload = function (event) {
        console.log('Read File');
        console.log(event.target.result);
        sendJson(event.target.result)
        //holder.style.background = 'url(' + event.target.result + ') no-repeat center';

    };


    // for (let i = 0; i < len; i++) {
    //     reader.readAsText(files[i]);
    //
    //     for (let key in files[i]) {
    //         console.log(key + ': ' + files[i][key])}
    //     // sendJson(files[i]).then(r => {console.log('SEND FILE')})
    //
    // }
}, false);

