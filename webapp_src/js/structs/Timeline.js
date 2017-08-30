import PureClass from './PureClass';
import { clamp } from '../utils/utils';

export class Timeline extends PureClass {
    
    constructor({playing=false, pos=0, duration=0, nudgeSize=5}) {
        super();
        this.playing = playing;
        this.pos = pos;
        this.duration = duration;
        this.nudgeSize = nudgeSize;
    }

    get percentage() {
        const { duration, pos } = this;

        if (duration === 0) {
            return 0;
        }

        const ratio = pos / duration;
        const percentage = ratio * 100;
        return clamp({ value: percentage, min: 0, max: 100 });
    }

    clampInsideTimeline(time) {
        return clamp({ value: time, min: 0, max: this.duration});
    }

    pause() {
        return this.update({ playing: false });
    }

    play() {
        return this.update({ playing: true });
    }

    togglePlaying() {
        return this.update({ playing: !this.playing })
    }

    seek(pos) {
        return this.update({
            pos: this.clampInsideTimeline(pos)
        });
    }

    seekRelative(delta) {
        return this.seek(this.pos + delta);
    }

    nudgeForward() {
        return this.seekRelative(this.nudgeSize);
    }

    nudgeBackwards() {
        return this.seekRelative(-this.nudgeSize);
    }
}

export class NullTimeline extends Timeline {
    constructor() {
        super({
            playing: false,
            pos: null,
            duration: null
        });
    }

    get percentage() {
        return null;
    }

    seek(pos) {
        console.warn('Cannot seek a timeline with no audio.');
        return this;
    }
}