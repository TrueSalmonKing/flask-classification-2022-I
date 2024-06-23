/** 
 * This script renders the histogram of the image chosen 
 * by the user. The histogram is rendered directly after the image
 *  is loaded on the page  
*/

window.onload = function() {
    const image = document.images[0];
    image.onload = generateHistogram();

    function generateHistogram() {
        const histogramCanvas = document.getElementById('histogram');
        const histogramCtx = histogramCanvas.getContext('2d');

        histogramCanvas.height = image.height;
        histogramCtx.drawImage(image, 0, 0, histogramCanvas.width, histogramCanvas.height);


        // Acquiring all image pixels for the three channels
        const imageData = histogramCtx.getImageData(0, 0, histogramCanvas.width, histogramCanvas.height);
        const data = imageData.data;
        const reds = new Array(256).fill(0);
        const greens = new Array(256).fill(0);
        const blues = new Array(256).fill(0);

        for (let i = 0; i < data.length; i += 4) {
            reds[data[i]]++;
            greens[data[i + 1]]++;
            blues[data[i + 2]]++;
        }

        // Setting the positions of the axes and the histogram
        histogramCtx.clearRect(0, 0, histogramCanvas.width, histogramCanvas.height);
        const axisMarginLeft = 50;
        const axisMarginBottom = 50;
        const maxCount = Math.max(...reds, ...greens, ...blues);

        // Plotting the axes
        drawAxes(histogramCtx, histogramCanvas, maxCount, axisMarginLeft, axisMarginBottom);

        //Plotting the histogram bars
        const width = (histogramCanvas.width - axisMarginLeft*2) / 256;
        for (let i = 0; i < 256; i++) {
            const redHeight = (reds[i] / maxCount) * (histogramCanvas.height - axisMarginBottom*2);
            const greenHeight = (greens[i] / maxCount) * (histogramCanvas.height - axisMarginBottom*2);
            const blueHeight = (blues[i] / maxCount) * (histogramCanvas.height - axisMarginBottom*2);

            histogramCtx.fillStyle = 'rgba(255, 0, 0, 0.6)';
            histogramCtx.fillRect(i * width + axisMarginLeft+1, histogramCanvas.height - redHeight - axisMarginBottom, width, redHeight);

            histogramCtx.fillStyle = 'rgba(0, 255, 0, 0.6)';
            histogramCtx.fillRect(i * width + axisMarginLeft+1, histogramCanvas.height - greenHeight - axisMarginBottom, width, greenHeight);

            histogramCtx.fillStyle = 'rgba(0, 0, 255, 0.6)';
            histogramCtx.fillRect(i * width + axisMarginLeft+1, histogramCanvas.height - blueHeight - axisMarginBottom, width, blueHeight);
        }
    }


    // Helper function used to draw the axes of count and intensity
    function drawAxes(ctx, canvas, maxCount, axisMarginLeft, axisMarginBottom) {
        ctx.beginPath();
        ctx.moveTo(axisMarginLeft, axisMarginBottom);
        ctx.lineTo(axisMarginLeft, canvas.height - axisMarginBottom);
        ctx.lineTo(canvas.width - axisMarginLeft, canvas.height - axisMarginBottom);
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Plotting the labels and the ticks for the Y axis
        ctx.font = '14px Arial';
        ctx.fillStyle = '#000';
        ctx.fillText('Count', 5, 20);
        for (let i = 0; i <= 10; i++) {
            const y = canvas.height - axisMarginBottom - (i * ((canvas.height - axisMarginBottom * 2)) / 10);
            ctx.moveTo(axisMarginLeft - 5, y);
            ctx.lineTo(axisMarginLeft, y);
            ctx.stroke();
            ctx.fillText(Math.round(maxCount * i / 10), 5, y + 3);
        }

        // Plotting the labels and the ticks for the X axis
        ctx.fillText('Intensity', canvas.width - 70, canvas.height - 10);
        for (let i = 0; i <= 256; i += 32) {
            const x = (i * (canvas.width - axisMarginLeft * 2) / 256) + axisMarginLeft;
            ctx.moveTo(x, canvas.height - axisMarginBottom);
            ctx.lineTo(x, canvas.height - axisMarginBottom + 5);
            ctx.stroke();
            ctx.fillText(i, x - 10, canvas.height - axisMarginBottom + 15);
        }
    }
};
