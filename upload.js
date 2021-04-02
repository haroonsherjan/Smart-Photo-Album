document.getElementById("displaytext").style.display = "none";
const sdk = apigClientFactory.newClient({apiKey:"K43G5Y7l8F1B7zFi5M16E21Zkpxz0lVeZjWRtOw5"});

function searchPhoto() {
    let image_message = document.getElementById("note-textarea").value;
    if (image_message === "")
        image_message = document.getElementById("transcript").value;

    console.log(image_message);

    var body = {};
    var params = {
        q: image_message,
        'x-api-key': 'K43G5Y7l8F1B7zFi5M16E21Zkpxz0lVeZjWRtOw5'
    };
    var additionalParams = {
        headers: {
            'Content-Type': "application/json",
        },
    };

    sdk.searchGet(params, body, additionalParams)
        .then(function (result) {
            //This is where you would put a success callback
            let response_data = result.data
            var ids = result.data.ids;
            let length_of_response = response_data.ids.length;
            if (length_of_response === 0) {
                document.getElementById("displaytext").innerHTML = "No Images Found !!!"
                document.getElementById("displaytext").style.display = "block";
            }

            document.getElementById("img-container").innerHTML = "";
            var para = document.createElement("p");
            para.setAttribute("id", "displaytext")
            document.getElementById("img-container").appendChild(para);

            ids.forEach(function (obj) {
                var img = new Image();
                img.src = "https://cloud-hw2-photos.s3.amazonaws.com/"+obj;
                img.setAttribute("class", "banner-img");
                img.setAttribute("alt", "effy");
                img.setAttribute("width", "150");
                img.setAttribute("height", "100");
                document.getElementById("displaytext").innerHTML = "Images returned are : "
                document.getElementById("img-container").appendChild(img);
                document.getElementById("displaytext").style.display = "block";

            });
        }).catch(function (result) {
        //This is where you would put an error callback
    });

}

function getBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        // reader.onload = () => resolve(reader.result)
        reader.onload = () => {
            let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
            if ((encoded.length % 4) > 0) {
                encoded += '='.repeat(4 - (encoded.length % 4));
            }
            resolve(encoded);
        };
        reader.onerror = error => reject(error);
    });
}

function uploadPhoto() {
    // var file_data = $("#file_path").prop("files")[0];
    var file = document.getElementById('file_path').files[0];
    const reader = new FileReader();

    var file_data;
    // var file = document.querySelector('#file_path > input[type="file"]').files[0];
    var encoded_image = getBase64(file).then(
        () => {
            var body = file;
            var params = {
                bucket: "cloud-hw2-photos",
                key: file.name,
                'x-api-key': 'K43G5Y7l8F1B7zFi5M16E21Zkpxz0lVeZjWRtOw5',
                "x-amz-meta-customlabels": document.getElementById("labels").value
            };

            var additionalParams = {
                headers: {
                    "x-amz-meta-customlabels": document.getElementById("labels").value
                },
            };

            sdk.uploadBucketKeyPut(params, body, additionalParams).then(function (res) {
                if (res.status == 200) {
                    // alert("Upload Successfull")
                    console.log("Success");
                    document.getElementById("uploadText").innerHTML = "IMAGE UPLOADED SUCCESSFULLY !!!"
                    document.getElementById("uploadText").style.display = "block";
                    document.getElementById("uploadText").style.color = "green";
                    document.getElementById("uploadText").style.fontWeight = "bold";
                }
            })
        });
}