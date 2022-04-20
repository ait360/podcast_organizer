const episodeForm = document.getElementById("episode_create_form");
const uploadBtn = document.getElementById("upload")

const audioTag = document.createElement('audio');
const episodeInput = document.getElementById('id_episode');
const episodeTitle = document.getElementById('id_title');
const episodeduration = document.getElementById('id_duration');
const episodeImage = document.getElementById('id_image');
const episodeSeason = document.getElementById('id_season');
const episodeInputDiv = document.getElementById('div_id_episode');

episodeForm.style.display = 'none';

uploadBtn.addEventListener('click', () => {
    episodeInput.click();
})

const episodeProperty = () => {
    uploadBtn.style.display = "none";
    const file = episodeInput.files;
    if (file) {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file[0]);

        fileReader.onload = function(event){
            audioTag.src = fileReader.result;
            console.log(audioTag.src);
            console.log(audioTag.currentTime);
            console.log(audioTag.duration);

            fileName = file[0].name.split('.')[0];
            if (!episodeTitle.value){
                episodeTitle.value = fileName;
            }

            // load audio duration
            audioTag.addEventListener("loadedmetadata", () =>{
                console.log(audioTag.duration);

                if (audioTag.duration === Infinity){
                    console.log(`got to infinity`)
                    audioTag.currentTime = 24*60*60;
                    console.log(`current time at infinity ${audioTag.currentTime}`);
                    episodeduration.value = audioTag.currentTime;
                    // audioTag.addEventListener('timeupdate', getduration)
                }

                episodeduration.value = audioTag.duration;
                console.log(`final duration ${episodeduration.value}`)
                // create new custom event for htmx trigger
                const HTMXChange = new Event("formSubmit");
                episodeInput.dispatchEvent(HTMXChange);
            })

            htmx.find("#progressDiv").style.display = 'block';
            htmx.find("#progressDiv").style.transition = 'ease-in';

        }
    }
    episodeForm.style.display = "block";
}

// function getduration(){
//         console.log(`current time before set to zero ${audioTag.currentTime}`)
//         audioTag.currentTime = 0;
//         console.log(`currentTime after set to zero ${audioTag.currentTime}`)
//         console.log(audioTag.duration);
//         audioTag.removeEventListener('timeupdate', getduration)
        
// }

episodeInput.addEventListener("change", episodeProperty);

// For Episode Create form upload progress
htmx.on('#episode_create_form', 'htmx:xhr:progress', function(evt) {
htmx.find('#progress').setAttribute('value', evt.detail.loaded/evt.detail.total * 100);
htmx.find('#progress').setAttribute('aria-valuenow', evt.detail.loaded/evt.detail.total * 100);
htmx.find('#progress').style.width = `${evt.detail.loaded/evt.detail.total * 100}%`

let upload_progress = evt.detail.loaded/evt.detail.total * 100;
htmx.find('#progress').innerHTML = `${upload_progress.toFixed(0)}%`;
});




// Hide input file button after file upload starts
htmx.on('#episode_create_form', 'htmx:xhr:loadstart', function(evt) {
episodeInputDiv.style.display = "none";
episodeInput.value = '';
});

// For Episode Update form upload progress
htmx.on('#episode_update_form', 'htmx:xhr:progress', function(evt) {
htmx.find('#progress').setAttribute('value', evt.detail.loaded/evt.detail.total * 100);
htmx.find('#progress').setAttribute('aria-valuenow', evt.detail.loaded/evt.detail.total * 100);
htmx.find('#progress').style.width = `${evt.detail.loaded/evt.detail.total * 100}%`

let upload_progress = evt.detail.loaded/evt.detail.total * 100;
htmx.find('#progress').innerHTML = `${upload_progress.toFixed(0)}%`;
});

htmx.on('#episode_update_form', 'htmx:xhr:loadstart', function(evt) {
episodeInputDiv.style.display = "none";
htmx.find("#progressDiv").style.display = 'block';
htmx.find("#progressDiv").style.transition = 'ease-in';
episodeInput.value = '';
});