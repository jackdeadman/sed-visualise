import React from 'react';
import { secsToMins } from '../utils/utils';
import { PlayIcon, PauseIcon } from './bundles/icons';

export default class AudioControls extends React.Component {

  seek(time) {
    let { timeline, onChange } = this.props;
    onChange(timeline.seek(time));
  }

  handleClick = e => {
    const { duration } = this.props.timeline;
    let box = e.target.getBoundingClientRect()
    let width = 350;
    let pos = e.nativeEvent.clientX - box.left;
    let time = (pos / width) * duration;

    this.seek(time);
  };

  handlePlayChange = e => {
    let { timeline, onChange } = this.props;
    onChange(timeline.togglePlaying());
  };

  render() {
    const { timeline } = this.props;
    const percentage = timeline.percentage;

    return (
      <div class="audio-controls cf">
        <div class="audio-controls__play"
                onClick={this.handlePlayChange}>
          {/* Show opposite icon to current state */}
          { timeline.playing ? <PauseIcon/> : <PlayIcon/> }
        </div>
        <div class="audio-controls__bar" onClick={this.handleClick}>
          <div class="audio-controls__inner"
                style={{width: (timeline.percentage || 0)+'%'}}></div>
        </div>
        { timeline.duration &&
          <div class="audio-controls__time">
            {secsToMins(timeline.pos)} / {secsToMins(timeline.duration)}
          </div>
        }
      </div>
    );
  }
}
