function drawArray (img, canv, width, height) {
    const context = canv.getContext("2d")
    // set your canvas width/height
    canv.width = width;
    canv.height = height;


    // create the imageData object, you'll need the width and height of your image
    var dataImage = context.createImageData(width, height);
    // browsers supporting TypedArrays
    if (dataImage.data.set) {
        dataImage.data.set(img);
    } else {
        // IE9
        img.forEach(function(val, i) {
            dataImage.data[i] = val;
        });
    }

    context.putImageData(dataImage, 0, 0);
    return context

}

function contrastImage(imgData, contrast){  //input range [-100..100]
    var d = imgData.data;
    contrast = (contrast/100) + 1;  //convert to decimal & shift range: [0..2]
    var intercept = 128 * (1 - contrast);
    for(var i=0;i<d.length;i+=4){   //r,g,b,a
        d[i] = d[i]*contrast + intercept;
        d[i+1] = d[i+1]*contrast + intercept;
        d[i+2] = d[i+2]*contrast + intercept;
    }
    return imgData;
}

function brightnessImage(imgData, brightness){  //input range [-100..100]
    var d = imgData.data;
    brightness = (brightness/100) ;  //convert to decimal & shift range: [0..2]
    for(var i=0;i<d.length;i+=4){   //r,g,b,a
        d[i] = d[i]*brightness;
        d[i+1] = d[i+1]*brightness;
        d[i+2] = d[i+2]*brightness;
    }
    return imgData;
}

function contrast_stretching(z, a, b, z1, zk){  //input range [-100..100]
    var d = imgData.data;
    brightness = (brightness/100) ;  //convert to decimal & shift range: [0..2]
    for(var i=0;i<d.length;i+=4){   //r,g,b,a
        d[i] = d[i]*brightness;
        d[i+1] = d[i+1]*brightness;
        d[i+2] = d[i+2]*brightness;
    }
    return imgData;
}


function copyImageData(ctx, src)
{
    var dst = ctx.createImageData(src.width, src.height);
    dst.data.set(src.data);
    return dst;
}
