import React from 'react';

const secsToMins = (secs) => {
  secs = Math.round(secs);
  let mins = parseInt(Math.floor(secs / 60));
  let seconds = Math.round((secs % 60));
  if (seconds < 10) {
    seconds = `0${seconds}`;
  }
  return `${mins}:${seconds}`;

}

const handleSeek = (e, duration, seek) => {
  let box = e.target.getBoundingClientRect()
  let width = 350;
  let pos = e.nativeEvent.clientX - box.left;
  seek(pos / width * duration)
}

const AudioControls = ({ onPlayChange, playing, pos, duration, onSeek}) => {
  let icon;

  if (playing) {
    icon = <i class="fa fa-pause" aria-hidden="true"></i>
  } else {
    icon = <i class="fa fa-play" aria-hidden="true"></i>
  }

  let percentage = 0;
  if (duration && pos) {
    percentage = pos / duration;
    percentage *= 100;
  }

  percentage = Math.min(100, percentage);
  percentage = Math.max(0, percentage);

  return (
    <div class="audio-controls cf">
      <div class="audio-controls__play" onClick={() => onPlayChange(!playing)}>
        { icon }
      </div>
      <div class="audio-controls__bar" onClick={(e) => handleSeek(e, duration, onSeek)}>
        <div class="audio-controls__inner" style={{width: percentage+'%'}}></div>
      </div>
      <div class="audio-controls__time">{secsToMins(pos)} / {secsToMins(duration)}</div>
    </div>
  )
}

export default AudioControls
