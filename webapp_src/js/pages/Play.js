import React from 'react';

import AudioControls from '../components/AudioControls';
import LabelSlider from '../components/LabelSlider';
import SystemPicker from '../components/SystemPicker';

import { Timeline, NullTimeline } from '../structs/Timeline';
import ItemManager from '../structs/ItemManager';

import { clamp } from '../utils/math';
import Key from '../utils/Key';

import { Overhang, Page } from '../components/bundles/layout';
import Waveform from '../components/Waveform';
import LabelsPicker from '../components/LabelsPicker';
import SystemsOutputContainer from '../components/SystemsOutputContainer';
import Modal from '../components/Modal';
import ClassifierFactory from '../structs/ClassifierFactory';

import Api from '../api';

const api = new Api();

class Play extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      timeline: new NullTimeline(),
      systems: new ItemManager({}),
      choosingSystem: false,
      labelsFile: null
    }

    this.classifierFactory = new ClassifierFactory({ api });

    this.timelineKeyMappings = {
      [Key.SPACE]: 'toggle',
      [Key.LEFT]: 'nudgeBackwards',
      [Key.RIGHT]: 'nudgeForwards'
    };
  }

  upload = e => {
    let input = document.getElementById('labels-upload');
    input.click();
  }

  handleLabelsSelected = async e => {
    const file = e.target.files[0];
    if (file) return;

    const reader = new TextFileReader();
    try {
      const labels = await reader.read();
    } catch (e) {
      return Promise.reject(e);
    }

    this.setState({ labels });
  }

  componentWillMount() {
    document.body.addEventListener('keydown', e => {
      const timeline = this.state.timeline;
      const actionName = this.timelineKeyMappings[e.keyCode];

      if (timeline[actionName]) {
        timeline[actionName].call();
      }
    })
  }

  handlePosChange = (e) => {
    const pos = e.originalArgs[0];
    const timeline = this.state.timeline;
    this.setState({
      timeline: timeline.seek(pos)
    });
  }

  seek(pos) {
    this.setState({ player: player.seek(pos) });
  }

  handleSystemPicked = system => {
    console.log('----', system);
    if (system) {
      this.setState({
        choosingSystem: false,
        systems: this.state.systems.add(system)
      });
    } else {
      this.setState({ choosingSystem: false });
    }
  }

  removeSystem = (system) => {
    this.setState({
      systems: this.state.systems.remove(system)
    });
  };

  get audioCode() {
    return this.props.match.params.code;
  }

  get audioFile() {
    return `/audio/${this.audioCode}/audio.wav`;
  }

  setTimeline = timeline => {
    this.setState({ timeline });
  };

  openSystemPicker() {
    this.setState({ choosingSystem: true });
  }

  closeSystemPicker() {
    this.setState({ choosingSystem: false });
  }

  render() {
    const { timeline, systems } = this.state;
    return (
      <div>
        {/* If choosing a system the picker appears over the top
            of the page */}
        <Modal onClose={this.closeSystemPicker.bind(this)}
              title="Select a system" open={this.state.choosingSystem}>
          <SystemPicker onChange={this.handleSystemPicked}
                        classifierFactory={this.classifierFactory}/>
        </Modal>
        <Overhang>
            <Waveform
              file={this.audioFile} timeline={timeline}
              onChange={this.setTimeline}
              onLoad={this.setTimeline}
            />
            {/* Doesn't make sense to show controls before loading audio */}
            { timeline.duration &&
              <AudioControls timeline={timeline} onChange={this.setTimeline} />
            }
        </Overhang>
        <Page>
          {/*<LabelsPicker labels={this.setLabels} onChange={this.setLabels} />*/}
          <SystemsOutputContainer systems={systems}
              timeline={timeline} code={this.audioCode}
              onRemove={this.removeSystem}
              api={api}
              audioCode={this.audioCode}
              onAdd={this.openSystemPicker.bind(this)} />
        </Page>
      </div>
    );
  }
}


export default Play;
