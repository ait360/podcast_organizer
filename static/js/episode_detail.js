const episodeAudio = document.getElementsByClassName("audio-source");
const playBtns = document.getElementsByClassName("episode_play"); 
const pauseBtns = document.getElementsByClassName("episode_pause");
const episodeUrls = document.getElementsByClassName("episodeurl");
const episodeIds = document.getElementsByClassName("episodeid");
const episodeTimes = document.getElementsByClassName("user_episode_currentTime");
const audioPlayer = document.querySelector('audio');
const seekBar = document.querySelector('.player-seek-bar');
const bufferedBar = document.querySelector('.player-buffered-bar');

const audioCurrentTime = document.querySelector('.current-time');
const audioDuration = document.querySelector('.duration');
const playerPlayBtn = document.querySelector('.play');
const playerPauseBtn = document.querySelector('.pause');
const fastForwardBtn = document.querySelector('.fast-forward');
const rewindBtn = document.querySelector('.rewind');
const playBackRateBtn = document.querySelector('.playbackrate');
const currentEpisode = document.querySelector('#currentepisode');
const currentTimeListened = document.querySelector('#timelistened');
const currentEpisdoeId = document.querySelector('#currentepisodeid');
const playbackrateView = document.querySelector('#playbackrateid');



playbackrateView.innerHTML = `${audioPlayer.playbackRate}`
fastForwardBtn.addEventListener('click', ()=>{
    // add 30 seconds to the current time
    console.log('got to fast forward')
    audioPlayer.currentTime += 30;
});

rewindBtn.addEventListener('click', ()=>{
    console.log('got to rewind')
    // subtract 10 seconds from the current time 
    audioPlayer.currentTime -= 10;
});

playBackRateBtn.addEventListener('change', ()=>{
    audioPlayer.playbackRate = parseFloat(playBackRateBtn.value);
    playbackrateView.innerHTML = `${audioPlayer.playbackRate}`
});

let currentid, currentidIndex
function locatecurrentEpisode(currentEpisdoeId, episodeIds){
    console.log('current Id', currentEpisdoeId.value)
    currentid = Array.from(episodeIds).find((item, index, array)=>{
        return item.value == currentEpisdoeId.value    
    });

    currentidIndex = Array.from(episodeIds).findIndex((item, index, array)=>{
        return item.value == currentEpisdoeId.value    
    });

    if (currentid) {
        console.log(currentidIndex)
        console.log(currentid.value);
    }

}

// locatecurrentEpisode(currentEpisdoeId, episodeIds)





let currentPlayItem, currentPlayIndex;
function addplayBtns3(playBtns){
    console.log('got to PlayBtns')
    Array.from(playBtns).forEach((item, index) => {
    const playIndex = index;
    const playItem = item;
    
    playItem.addEventListener('click', () => {
            console.log('got here!')
            console.log(audioPlayer.getAttribute('src'));
            console.log('got here 2');
            let audioSrc = audioPlayer.getAttribute('src');
            let episodeUrl = episodeUrls[playIndex].value;            
            console.log(`episodeUrl ${episodeUrl}`);
            console.log(`audioSrc ${audioSrc}`);
            playerPauseBtn.click(); // pause current music
            setEpisode(audioSrc, episodeUrl, playIndex);
            // dispatch submit event
            const submitStartTime = new Event("submitstarttime");
            playItem.setAttribute('hx-headers', `{"start": ${audioPlayer.currentTime}, "playing": "yes"}`)
            playItem.dispatchEvent(submitStartTime);
            
            currentPlayItem = playItem;
            currentPlayIndex = playIndex;
            // playerPlayBtn.click();
            console.log('got here 5');
            
            
            
        
        })

});
};

let prevEpisodeIndex
function setEpisode(audioSrc, episodeUrl, playIndex){


    if (audioSrc == episodeUrl){
        audioPlayer.play()
        console.log('got here 3');
       
  
    } else {
        console.log('got here 4');
        audioPlayer.setAttribute('src', episodeUrl);
        
        playItemTime = parseFloat(episodeTimes[playIndex].value);
        if (playItemTime){
            audioPlayer.currentTime = playItemTime
            audioPlayer.play();
        }else{
            audioCurrentTime.innerHTML = '00 : 00';
            audioPlayer.play()
        }
        
    }
};


addplayBtns3(playBtns);
addpauseBtns(pauseBtns);



htmx.on('#episodelist', 'htmx:afterSwap', function(evt) {

    addplayBtns3(playBtns);
    addpauseBtns(pauseBtns);
    locatecurrentEpisode(currentEpisdoeId, episodeIds)
    if (audioPlayer.paused){
        let bindex = playBtns[currentidIndex].innerHTML.indexOf('<b>');
        playBtns[currentidIndex].innerHTML = playBtns[currentidIndex].innerHTML.slice(0, bindex);
        if (!pauseBtns[currentidIndex].innerHTML.includes('<b>paused</b>')){
            pauseBtns[currentidIndex].innerHTML += '<b>paused</b>';
        };
        
    } else{
        
        let bindex = pauseBtns[currentidIndex].innerHTML.indexOf('<b>');
        pauseBtns[currentidIndex].innerHTML = pauseBtns[currentidIndex].innerHTML.slice(0, bindex);
        if (!playBtns[currentidIndex].innerHTML.includes('<b>playing</b>')){
            playBtns[currentidIndex].innerHTML += '<b>playing</b>'
        };
        
    }
})


let currentPauseItem, currentPauseIndex;
function addpauseBtns(pauseBtns){


    Array.from(pauseBtns).forEach((item, index) => {
        item.addEventListener('click', () =>{
            audioPlayer.pause()
            console.log(audioPlayer.currentTime);
            console.log(item.getAttribute('hx-post'))
            const submitCurrentTime = new Event("submitcurrenttime");
            
            item.setAttribute('hx-headers', `{"current": ${audioPlayer.currentTime}}`)
            item.dispatchEvent(submitCurrentTime);
            currentPauseItem = item;
            episodeTimes[index].setAttribute('value', `${audioPlayer.currentTime}`)
            // playerPauseBtn.click();

           
        });

    });
};


seekBar.addEventListener('input', (e) => {
    console.log(seekBar.value);
    audioPlayer.currentTime = parseFloat(seekBar.value);
    console.log('seekBar Change', audioPlayer.currentTime);
    let playedLength = (audioPlayer.currentTime * 100)/audioPlayer.duration;
    audioCurrentTime.innerHTML = formatTime(audioPlayer.currentTime);
    seekBar.style.background = `linear-gradient(to right, #63ff69 0%, #63ff69 ${playedLength}%, rgba(0, 0, 0, 0.5) ${playedLength}%, rgba(0, 0, 0, 0.5) 100%)`;
  
    
})


audioPlayer.addEventListener("loadedmetadata", (e)=>{
    seekBar.max = audioPlayer.duration;
    bufferedBar.max = audioPlayer.duration;
    audioDuration.innerHTML = formatTime(audioPlayer.duration);
    
});

audioPlayer.addEventListener('timeupdate', (e)=>{
    let currenttime = e.target.currentTime; // get audio current time
    let duration = e.target.duration; // get audio duration time
    let progreswidth = (currenttime/duration) * 100;
    audioCurrentTime.innerHTML = formatTime(currenttime);
    seekBar.value = e.target.currentTime;
    seekBar.style.background = `linear-gradient(to right, #63ff69 0%, #63ff69 ${progreswidth}%, rgba(0, 0, 0, 0.5) ${progreswidth}%, rgba(0, 0, 0, 0.5) 100%)`;

});


audioPlayer.setAttribute('src', episodeUrls[0].value);
audioPlayer.currentTime = parseFloat(episodeTimes[0].value);


// set seekbar and bufferedbar attributes with episode audio is loaded



// bufferBar
audioPlayer.addEventListener('durationchange', () =>{

    audioPlayer.addEventListener('progress', () =>{
        let musicDuration = audioPlayer.duration;
        if (musicDuration > 0) {
            for (let i = 0; i < audioPlayer.buffered.length; i++){
                if (audioPlayer.buffered.start(audioPlayer.buffered.length - 1 -i) < audioPlayer.currentTime) {
                    bufferedBar.value = audioPlayer.buffered.end(audioPlayer.buffered.length -1 -i);
                    console.log(bufferedBar.value);
                    break
                }
            }
        } 
    });

});


// format episode audio duration to readable format
const formatTime = (time) => {
    if (time >= 3600) {
        let hour = Math.floor(time / 3600);
        if (hour < 10){
            hour =`0${hour}`;
        }
        let min_sec = Math.floor(time % 3600);
        let min = Math.floor(min_sec / 60);

        if(min < 10) {
            min =`0${min}`;
        }

        let sec = Math.floor(min_sec % 60);

        if(sec < 10){
            sec = `0${sec}`;

        }

        return `${hour} : ${min} : ${sec}`;


    } else {let min  = Math.floor(time/60);
    
        if(min < 10) {
        min =`0` + min;
    }
    let sec = Math.floor(time % 60);

    if(sec < 10){
        sec = `0` + sec;

    }

    return `${min} : ${sec}`;
}

};


// player play and pause buttons

playerPlayBtn.addEventListener('click', (e)=>{
    
    console.log('got here 6');
    
    if (currentPlayIndex | currentPlayIndex == 0 ){
        playBtns[currentPlayIndex].click();
    } else{
        audioPlayer.play();
        if (currentidIndex | currentidIndex == 0){ 
            let bindex = pauseBtns[currentidIndex].innerHTML.indexOf('<b>');
            pauseBtns[currentidIndex].innerHTML = pauseBtns[currentidIndex].innerHTML.slice(0, bindex);
            if (!playBtns[currentidIndex].innerHTML.includes('<b>playing</b>')){
                playBtns[currentidIndex].innerHTML += '<b>playing</b>'
            };
            
        }

        // send start time to server
        htmx.ajax('POST', 
                    `/episode/${episodeIds[0].value}/paused`,
                    {target : "#play_status", swap: 'innerHTML', 
                    headers : {'start': `${audioPlayer.currentTime}`, 'playing' : 'yes'},
                    source  : playerPlayBtn}
        )
        
    }
    
});

playerPauseBtn.addEventListener('click', ()=>{
    
    
    if (currentPlayIndex | currentPlayIndex == 0 ){
        console.log('got here 7');
        pauseBtns[currentPlayIndex].click();
    }else{
        console.log('got here 8');
        audioPlayer.pause();
        if (currentidIndex | currentidIndex == 0){ 
            let bindex = playBtns[currentidIndex].innerHTML.indexOf('<b>');
            playBtns[currentidIndex].innerHTML = playBtns[currentidIndex].innerHTML.slice(0, bindex);
            if (!pauseBtns[currentidIndex].innerHTML.includes('<b>paused</b>')){
                pauseBtns[currentidIndex].innerHTML += '<b>paused</b>';
            };
        }

        // send current time to server
        console.log(`episodeid ${episodeIds[0].value}`)
        htmx.ajax('POST', 
                    `/episode/${episodeIds[0].value}/paused`,
                    {target : "#play_status", swap: 'innerHTML', 
                    headers : {'current': `${audioPlayer.currentTime}`, },
                    source  : playerPauseBtn}
        )
    }
   
});

