const coverPicture = document.getElementById('id_cover_picture');
const description = document.getElementById('id_description');
const channelName = document.getElementById('id_name');

const previewPhoto = () => {
    const file = coverPicture.files;
    if (file) {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file[0]);
        // const preview = document.getElementById("file-preview");

        fileReader.onload = function(event){

            // preview.src = fileReader.result;//event.target.result;
            // console.log(file[0]);
            fileName = file[0].name.split('.')[0];
            if (!channelName.value){
                channelName.value = fileName;
            }
            
            // console.log(file[0].type);
        }


    }
    // button.style.visibility = "hidden"
}

coverPicture.addEventListener("change", previewPhoto);
