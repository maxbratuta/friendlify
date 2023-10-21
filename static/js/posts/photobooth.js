document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("takeAShot");
    const video = document.getElementById("video");
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const captureButton = document.getElementById("capture");
    const capturedPhoto = document.getElementById("capturedPhoto");
    const capturedPhotoInput = document.getElementById("capturedPhotoInput");
    const loader = document.getElementById("videoLoader");

    let stream = null;

    modal.addEventListener("shown.bs.modal", async function () {
        try {
            stream = await navigator.mediaDevices.getUserMedia({video: true});
            video.srcObject = stream;

            video.onloadedmetadata = function () {
                console.log("Metadata for video loaded");
                video.play();
            };

            video.onerror = function () {
                console.error("Error in video playback:", video.error);
            };

            video.onplaying = function () {
                loader.style.display = "none";
                captureButton.disabled = false;

                const size = Math.min(video.videoWidth, video.videoHeight);
                video.width = size;
                video.height = size;
            };
        } catch (error) {
            console.error("Error accessing the camera:", error);
            alert("Error accessing the camera: " + error);
        }
    });

    modal.addEventListener("hidden.bs.modal", function () {
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }

        video.srcObject = null;
        video.onplaying = null;

        loader.style.display = "flex";
        captureButton.disabled = true;
    });

    captureButton.addEventListener("click", function () {
        const size = Math.min(video.videoWidth, video.videoHeight);
        canvas.width = size;
        canvas.height = size;

        const offsetX = (video.videoWidth - size) / 2;
        const offsetY = (video.videoHeight - size) / 2;

        // Draw the video frame to the canvas as it is
        context.drawImage(video, offsetX, offsetY, size, size, 0, 0, size, size);

        // Create an auxiliary canvas to perform the inversion
        const tempCanvas = document.createElement("canvas");
        const tempContext = tempCanvas.getContext("2d");
        tempCanvas.width = size;
        tempCanvas.height = size;

        // Draw the inverted image to the auxiliary canvas
        tempContext.scale(-1, 1);
        tempContext.drawImage(canvas, -size, 0);

        // Copy the inverted image back to the original canvas
        context.drawImage(tempCanvas, 0, 0);

        capturedPhoto.src = canvas.toDataURL("image/jpeg");

        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
        }


        const file = dataURLtoFile(capturedPhoto.src, "captured.jpg");
        let dt = new DataTransfer();

        dt.items.add(file);

        capturedPhotoInput.files = dt.files;

        const firstModal = bootstrap.Modal.getInstance(modal);
        firstModal.hide();

        const nextModal = new bootstrap.Modal(document.getElementById("addPost"));
        nextModal.show();
    });

    function dataURLtoFile(dataurl, filename) {
        let arr = dataurl.split(",");
        let bstr = atob(arr[1]);
        let n = bstr.length;
        let u8arr = new Uint8Array(n);

        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }

        return new File([u8arr], filename, {type: "image/jpeg"});
    }
});