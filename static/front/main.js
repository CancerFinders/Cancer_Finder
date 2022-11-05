const canvas = document.getElementById("canvas")
const CanvasPanel = document.getElementById("CanvasPanel")
const ContrastSlider = document.getElementById('ContrastSlider')
const BrightnessSlider = document.getElementById('BrightnessSlider')
const ScaleSlider = document.getElementById('ScaleSlider')  

const reduceButton = document.getElementById('reduce');
const brushModeButton = document.getElementById('brushMode');
const pointModeButton = document.getElementById('pointMode');
const rulerModeButton = document.getElementById('rulerMode');

const DDModeButton = document.getElementById('2D')
const TDModeButton = document.getElementById('3D')
const NextSliceButton = document.getElementById('NextSlice')
const PrevSliceButton = document.getElementById('PrevSlice')
const sendButton = document.getElementById('send')
const generateButton = document.getElementById('generateBtn')

const boneWindowButton = document.getElementById('boneWindowMode')
const softfabricWindowButton = document.getElementById('softfabricWindowMode')
const pulmonaryWindowButton = document.getElementById('pulmonaryWindowMode')

const chestTypeButton = document.getElementById('chestType')
const spleenTypeButton = document.getElementById('spleenType')

let contrast = 0
let brightness = 100
let scale = 100
let mouseMode = 'brushMode'
let imgType = 'spleen'
let movePointNum = 0
let moveMode = false
let prevX = null
let prevY = null

let draw = false
let pointArray = []
let beginCoordinateBrushMode = []
let endCoordinateBrushMode = []

let beginCoordinateRulerMode = []
let endCoordinateRulerMode = []
let swapFlagMoveMode = false

let imageMode = '2D'
let sliceArray = []
let sliceNumber = 0


function httpGet(theUrl) {

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

let core_url = 'http://127.0.0.1:5000/img/'

let url =  core_url + imgType +'/512/512'
let name = 'placeHolder'
let responce  = JSON.parse(httpGet(url));
let img = responce['img']
name = responce['name']


console.log(img)

canvas.height =  (responce['h']*scale/100)
canvas.width = (responce['w']*scale/100)
canvas.style.width  = (responce['h']*scale/100) + 'px';
canvas.style.height = (responce['w']*scale/100) + 'px';




let ctx = drawArray(img, canvas, responce['h'], responce['w']);
let originalImgData = copyImageData(ctx, ctx.getImageData(0,0, canvas.width, canvas.height))
let currentImgData = copyImageData(ctx, ctx.getImageData(0,0, canvas.width, canvas.height))



//Кнопки редактора изображения
function changeImg(){
    ctx.putImageData(currentImgData, 0, 0)
    let newImgData = contrastImage(ctx.getImageData(0,0, canvas.width, canvas.height), contrast)
    newImgData = brightnessImage(newImgData, brightness)
    canvas.style.width  = (responce['h']*scale/100) + 'px';
    canvas.style.height = (responce['w']*scale/100) + 'px';
    ctx.putImageData(newImgData, 0, 0)
}
function clearImg() {
    ctx.putImageData(originalImgData, 0, 0)
    contrast = 0
    brightness = 100
    scale = 100
}
function findNear(x,y, XYarray){

    let minDist = 2147483648;
    let minDistPos = 2147483648;
    for (let coordinateNum = 0; coordinateNum < XYarray.length; coordinateNum++){
       let dist = Math.sqrt(Math.pow((x - XYarray[coordinateNum][0]),2 ) + Math.pow((y - XYarray[coordinateNum][1]), 2))
        console.log('distance ', dist)
        if (minDist > dist) {
            minDist = dist;
            minDistPos = coordinateNum;
        }
    }
    return [minDist,  minDistPos]
}
reduceButton.addEventListener('click',  clearImg);
function setContrast() {
    contrast = ContrastSlider.value;
    console.log(contrast)
    changeImg()
}

function setBrightness() {
    brightness = BrightnessSlider.value;
    console.log(brightness)
    changeImg()
}
function setScale() {
    scale = ScaleSlider.value;
    console.log(scale)
    changeImg()
}


boneWindowButton.addEventListener('click', () => {
    contrast = 50
    brightness = 50
    changeImg()
})
softfabricWindowButton.addEventListener('click', () => {
    contrast = 50
    brightness = 150
    changeImg()
})
pulmonaryWindowButton.addEventListener('click', () => {
    contrast = -20
    brightness = 200
    changeImg()
})

brushModeButton.addEventListener('click', () => {
    mouseMode = 'brushMode'
})
pointModeButton.addEventListener('click', () => {
    mouseMode = 'pointMode'
})
rulerModeButton.addEventListener('click', () => {
    mouseMode = 'rulerMode'
})

function setNewImg(img, h, w){
    canvas.height = h
    canvas.width = w
    canvas.style.width  = (h*scale/100) + 'px';
    canvas.style.height = (w*scale/100) + 'px';
    ctx = drawArray(img, canvas, h, w);
    originalImgData = copyImageData(ctx, ctx.getImageData(0,0, canvas.width, canvas.height))
}

function newDDimg(){
    NextSliceButton.style.display = 'None'
    PrevSliceButton.style.display = 'None'
    imageMode = '2D';
    let url = core_url + imgType +'/512/512'
    let responce  = JSON.parse(httpGet(url));
    name = responce['name']
    let img = responce['img']
    setNewImg(img, responce['h'], responce['w'])
}

DDModeButton.addEventListener('click', newDDimg)
TDModeButton.addEventListener('click', ()=> {
    NextSliceButton.style.display = 'Block'
    PrevSliceButton.style.display = 'Block'
    imageMode = '3D';
    let url = core_url + 'img3d/' + imgType +'/512/512'
    let responce  = JSON.parse(httpGet(url));
    sliceArray = responce
    console.log(sliceArray)
    console.log(responce[sliceNumber])
    setNewImg(responce[sliceNumber]['img'], responce[sliceNumber]['h'], responce[sliceNumber]['w'])

})
NextSliceButton.addEventListener('click', () => {
    if (sliceNumber + 1 < sliceArray.length){
    sliceNumber += 1;
    console.log('Slice Number ' + sliceNumber)
    console.log(sliceArray[sliceNumber])
    setNewImg(sliceArray[sliceNumber]['img'], sliceArray[sliceNumber]['h'], sliceArray[sliceNumber]['w'])}
})
PrevSliceButton.addEventListener('click', () => {
    if (sliceNumber - 1 > 0) {
        sliceNumber -= 1;
        console.log('Slice Number ' + sliceNumber)
        console.log(sliceArray[sliceNumber])
        setNewImg(sliceArray[sliceNumber]['img'], sliceArray[sliceNumber]['h'], sliceArray[sliceNumber]['w'])
    }
    })

spleenTypeButton.addEventListener('click', ()=> {
    imgType = "spleen"
    newDDimg()
})
spleenTypeButton.addEventListener('click', ()=> {
    imgType = "chest"
    newDDimg()
})

canvas.addEventListener("mousedown", (e) => {
    // clearImg()
    changeImg()
    draw = true;
    ctx.fillStyle = "red";
    ctx.strokeStyle = "red";
    ctx.strokeWidth = 2;
    ctx.lineWidth = 5;
    let radius = 5
    const rect = canvas.getBoundingClientRect()
    let x = e.clientX - rect.x
    let y = e.clientY - rect.y

    ctx.beginPath();
    if (mouseMode === 'rulerMode') {
        if (!swapFlagMoveMode){
            ctx.arc(x, y, radius, 0, Math.PI*2, false)
            beginCoordinateRulerMode = [x, y]
        }
        else {
            ctx.arc(x, y, radius, 0, Math.PI*2, false)
            endCoordinateRulerMode = [x, y]
        }
        swapFlagMoveMode = !swapFlagMoveMode
    }
    if (mouseMode === 'brushMode')
    {
        beginCoordinateBrushMode = [x, y]
        console.log('Begin brush at ' + x + '/' + y )
    }
    if (mouseMode === 'pointMode'){

        moveMode = true
        console.log('Enabled Move Mode')


        let nearDist = findNear(x, y, pointArray)[0]
        let nearPointNum = findNear(x, y, pointArray)[1]
        console.log(pointArray);

        if (nearDist < radius) {
            pointArray[nearPointNum] = [x, y]
            movePointNum = nearPointNum
        }
        else {
            pointArray[pointArray.length] = [x, y]
            movePointNum = pointArray.length
        }
        console.log('MovePointNum ', movePointNum)

        ctx.moveTo(x, y);
        for (let i = 0; i < pointArray.length; i++)
        {

            ctx.arc(x, y, radius, 0, Math.PI*2, false);
            x = pointArray[i][0] ;
            y = pointArray[i][1] ;
            ctx.lineTo(x  ,y )
        }
        // ctx.lineTo(pointArray[0][0], pointArray[0][1])


    }
    ctx.closePath();
    ctx.stroke()
})
// Set draw to false when mouse is released
canvas.addEventListener("mouseup", (e) => {


    if (mouseMode === 'brushMode')
    {
        ctx.strokeStyle = "red";
        let x_begin = beginCoordinateBrushMode[0]
        let y_begin = beginCoordinateBrushMode[1]
        let x_end = endCoordinateBrushMode[0]
        let y_end = endCoordinateBrushMode[1]

        console.log('Begin brush at ' + x_begin + '/' + y_begin )
        console.log('End brush at ' + x_end + '/' + y_end )
        ctx.beginPath()
        ctx.moveTo(x_begin, y_begin)
        ctx.lineTo(x_end, y_end)
        ctx.closePath()
        ctx.stroke()
        console.log('End Brush')

    }
    moveMode = false
    console.log('Disabled Move Mode')
    draw = false
    currentImgData = copyImageData(ctx, ctx.getImageData(0,0, canvas.width, canvas.height))
})

canvas.addEventListener("mousemove", (e) => {
    let radius = 5
    // if draw is false then we won't draw
    if (mouseMode === 'rulerMode' ){

        // clearImg()
        changeImg()
        const rect = canvas.getBoundingClientRect()
        let x = e.clientX - rect.x
        let y = e.clientY - rect.y
        if (!swapFlagMoveMode)
            endCoordinateRulerMode = [x, y]
        ctx.beginPath()
        ctx.moveTo(beginCoordinateRulerMode[0], beginCoordinateRulerMode[1])
        ctx.arc(beginCoordinateRulerMode[0], beginCoordinateRulerMode[1], radius, 0, Math.PI*2, false);
        ctx.lineTo(endCoordinateRulerMode[0]  ,endCoordinateRulerMode[1] )
        ctx.arc(endCoordinateRulerMode[0], endCoordinateRulerMode[1], radius, 0, Math.PI*2, false);
        ctx.closePath()
        ctx.stroke()
    }
    if (mouseMode === 'pointMode' && moveMode){
        // clearImg()
        changeImg()
        const rect = canvas.getBoundingClientRect()
        let x = e.clientX - rect.x
        let y = e.clientY - rect.y
        pointArray[movePointNum] = [x, y]

        ctx.beginPath()
        ctx.moveTo(pointArray[movePointNum][0], pointArray[movePointNum][1])
        for (let i = 0; i < pointArray.length; i++) {
            ctx.arc(x, y, radius, 0, Math.PI*2, false);
            x = pointArray[i][0]
            y = pointArray[i][1]
            ctx.lineTo(x  ,y )
        }
        //  ctx.lineTo(pointArray[0][0], pointArray[0][1])

            ctx.closePath()
            ctx.stroke()
    }
    if (mouseMode === 'brushMode'){
        if(prevX == null || prevY == null || !draw){
            const rect = canvas.getBoundingClientRect()
            prevX = e.clientX - rect.x
            prevY = e.clientY - rect.y
            return
        }
        const rect = canvas.getBoundingClientRect()
        let currentX = e.clientX - rect.x
        let currentY = e.clientY - rect.y

        ctx.beginPath()
        ctx.strokeStyle = "red";
        ctx.moveTo(prevX, prevY)
        ctx.lineTo(currentX, currentY)
        ctx.stroke()

        prevX = currentX
        prevY = currentY
        endCoordinateBrushMode = [prevX, prevY]
    }
})

sendButton.addEventListener('click', ()=> {

    let imgData = ctx.getImageData(0 ,0 , canvas.width, canvas.height)
    let bitMask =  new ArrayBuffer( imgData.data.length/4)
    for (let i = 0; i< imgData.data.length; i+=4){
            if (imgData.data[i] !== imgData.data[i + 1] || imgData.data[i + 1] !== imgData.data[i + 2] )
            {
                bitMask[i/4] = 1;
            }
            else
            {
                bitMask[i/4] = 0;
            }
    }
    console.log(bitMask)

    let data = {
        'filename': name,
        'type': imgType,
        'img': Array.from(imgData.data),
        'h': canvas.height,
        'w': canvas.width,
        'bitMask': bitMask,
    }
    // console.log(data)
    fetch(core_url + "setimg", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body:
            JSON.stringify(data)
    }).then(res => {
        console.log("Re quest complete! response:", res);
    });

    newDDimg()
})


generateButton.addEventListener('click', ()=> {

    let imgData = ctx.getImageData(0 ,0 , canvas.width, canvas.height)


    let data = {
        'filename': name,
        'type': imgType,
        'img': Array.from(imgData.data),
        'h': canvas.height,
        'w': canvas.width,
    }
    // console.log(data)
    fetch(core_url + "generate", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body:
            JSON.stringify(data)
    }).then(res => {
        console.log("Re quest complete! response:", res);
    });

    newDDimg()
})