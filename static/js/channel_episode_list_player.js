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
const currentEpisodeId = document.querySelector('#currentepisodeid');
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

let playerEpisodeId, playerEpisodeIdIndex
function locatecurrentEpisode(currentEpisodeId, episodeIds){
    console.log('current Id', currentEpisodeId.value)
    playerEpisodeId = Array.from(episodeIds).find((item, index, array)=>{
        return item.value == currentEpisodeId.value    
    });

    playerEpisodeIdIndex = Array.from(episodeIds).findIndex((item, index, array)=>{
        return item.value == currentEpisodeId.value    
    });

    if (playerEpisodeId) {
        console.log(playerEpisodeIdIndex)
        console.log(playerEpisodeId.value);
    }

}


locatecurrentEpisode(currentEpisodeId, episodeIds)



let currentPlayItem, currentPlayIndex;//, playIndex, playitem;
function addplayBtns3(playBtns){
    Array.from(playBtns).forEach((item, index) => {
    let playIndex = index;
    let playItem = item;
    console.log('I got here');
    
    
    playItem.addEventListener('click', () => {
            console.log('got to top of playBtn!')
            console.log(audioPlayer.getAttribute('src'));
            console.log('got to after getting audio src');
            let audioSrc = audioPlayer.getAttribute('src');
            let episodeUrl = episodeUrls[playIndex].value;            
            console.log(`episodeUrl ${episodeUrl}`);
            console.log(`audioSrc ${audioSrc}`);
            if (audioSrc){
                playerPauseBtn.click(); // pause current music
            }
            
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
        if (audioPlayer.currentTime == audioPlayer.duration){
            audioPlayer.currentTime = 0;
        }
        audioPlayer.play()
        console.log('got to setEpisode with same Episode');
       
  
    } else {
        console.log('got here 4');
        audioPlayer.setAttribute('src', episodeUrl);
        
        playItemTime = parseFloat(episodeTimes[playIndex].value);
        if (playItemTime){
            audioPlayer.currentTime = playItemTime
            if (audioPlayer.currentTime == audioPlayer.duration){
                audioPlayer.currentTime = 0;
            }
            audioPlayer.play();
        }else{
            audioCurrentTime.innerHTML = '00 : 00';
            if (audioPlayer.currentTime == audioPlayer.duration){
                audioPlayer.currentTime = 0;
            }
            audioPlayer.play()
        }
        
    }
};


addplayBtns3(playBtns);
addpauseBtns(pauseBtns);



htmx.on('#episodelist', 'htmx:afterSwap', function(evt) {

    addplayBtns3(playBtns);
    addpauseBtns(pauseBtns);
    locatecurrentEpisode(currentEpisodeId, episodeIds)
    if (audioPlayer.paused){
        let bindex = playBtns[playerEpisodeIdIndex].innerHTML.indexOf('<b>');
        playBtns[playerEpisodeIdIndex].innerHTML = playBtns[playerEpisodeIdIndex].innerHTML.slice(0, bindex);
        if (!pauseBtns[playerEpisodeIdIndex].innerHTML.includes('<b>paused</b>')){
            pauseBtns[playerEpisodeIdIndex].innerHTML += '<b>paused</b>';
        };
        
    } else{
        
        let bindex = pauseBtns[playerEpisodeIdIndex].innerHTML.indexOf('<b>');
        pauseBtns[playerEpisodeIdIndex].innerHTML = pauseBtns[playerEpisodeIdIndex].innerHTML.slice(0, bindex);
        if (!playBtns[playerEpisodeIdIndex].innerHTML.includes('<b>playing</b>')){
            playBtns[playerEpisodeIdIndex].innerHTML += '<b>playing</b>'
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
    // console.log(e.target);
    console.log(e.target.duration);
    console.log(`audio duration ${audioPlayer.duration}`);
    audioDuration.innerHTML = formatTime(audioPlayer.duration);
    console.log(`the innerHTML ${audioDuration.innerHTML}`)
    
});

audioPlayer.addEventListener('timeupdate', (e)=>{
    let currenttime = e.target.currentTime; // get audio current time
    let duration = e.target.duration; // get audio duration time
    let progreswidth = (currenttime/duration) * 100;
    audioCurrentTime.innerHTML = formatTime(currenttime);
    seekBar.value = e.target.currentTime;
    seekBar.style.background = `linear-gradient(to right, #63ff69 0%, #63ff69 ${progreswidth}%, rgba(0, 0, 0, 0.5) ${progreswidth}%, rgba(0, 0, 0, 0.5) 100%)`;

});


audioPlayer.setAttribute('src', currentEpisode.value);
if (currentTimeListened.value) {
    audioPlayer.currentTime = parseFloat(currentTimeListened.value);
}



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

playerPlayBtn.addEventListener('click', ()=>{
    
    console.log('got to top of playerPlayBtn');
    
    if (currentPlayIndex | currentPlayIndex == 0 ){
        playBtns[currentPlayIndex].click();
    } else{
        audioPlayer.play();
        if (playerEpisodeIdIndex | playerEpisodeIdIndex == 0){ 
            let bindex = pauseBtns[playerEpisodeIdIndex].innerHTML.indexOf('<b>');
            pauseBtns[playerEpisodeIdIndex].innerHTML = pauseBtns[playerEpisodeIdIndex].innerHTML.slice(0, bindex);
            if (!playBtns[playerEpisodeIdIndex].innerHTML.includes('<b>playing</b>')){
                playBtns[playerEpisodeIdIndex].innerHTML += '<b>playing</b>'
            };
            
        }

        // send start time to server
        htmx.ajax('POST', 
                    `/episode/${playerEpisodeId.value}/paused`,
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
        if (playerEpisodeIdIndex | playerEpisodeIdIndex == 0){ 
            let bindex = playBtns[playerEpisodeIdIndex].innerHTML.indexOf('<b>');
            playBtns[playerEpisodeIdIndex].innerHTML = playBtns[playerEpisodeIdIndex].innerHTML.slice(0, bindex);
            if (!pauseBtns[playerEpisodeIdIndex].innerHTML.includes('<b>paused</b>')){
                pauseBtns[playerEpisodeIdIndex].innerHTML += '<b>paused</b>';
            };
        }

        // send current time to server

        htmx.ajax('POST', 
                    `/episode/${playerEpisodeId.value}/paused`,
                    {target : "#play_status", swap: 'innerHTML', 
                    headers : {'current': `${audioPlayer.currentTime}`, },
                    source  : playerPauseBtn}
        )
    }
   
});

