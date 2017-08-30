import React from 'react';
import Wavesurfer from 'react-wavesurfer';
import { Timeline, NullTimeline } from '../structs/Timeline';
import Loader from './Loader';

export default class WaveForm extends React.Component {

    constructor(props) {
        super(props);
        this.options = {
            progressColor: '#F17300', waveColor: '#054A91',
            normalize: true, hideScrollbar: true
        };
    }

    handleLoaded = component => {
        const duration = component.wavesurfer.getDuration();
        console.log('Loaded');
        this.props.onLoad(new Timeline({ duration }));
    }

    handleChange = component => {
        const { timeline, onChange } = this.props;
        const pos = component.originalArgs[0];
        onChange(timeline.seek(pos));
    }

    get loading() {
        return this.props.timeline.duration == null;
    }

    render() {
        const { file, timeline, onChange } = this.props;
        return (
            <div>
                <div class={this.loading ? 'hidden' : ''}>
                    <Wavesurfer
                        audioFile={file}
                        pos={timeline.pos}
                        zoom={100}
                        options={this.options}
                        onPosChange={this.handleChange}
                        playing={timeline.playing}
                        onReady={this.handleLoaded}
                    />
                </div>
                {/* Can't use a ternary as the Wavesurfer component
                 needs to be mounted to start loading the audio */}
                { this.loading &&
                    <Loader message="Downloading audio..."/>
                }
            </div>
        );
    }
}
