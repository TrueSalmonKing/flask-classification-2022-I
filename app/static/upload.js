/**
 * Defined script used to change the label of the upload button.
 * Once the image is uploaded the text content is changed 
 * to the image filename.
 */

document.addEventListener('DOMContentLoaded', function() {
    var inputFile = document.getElementById('image');

    inputFile.addEventListener('change', function() {
        var label = document.getElementById("image_label");
        if (this.files.length > 0) {
            label.textContent = this.files[0].name;
        } else {
            label.textContent = "upload image";
        }
    });
});