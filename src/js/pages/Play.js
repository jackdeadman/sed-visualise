import React from 'react';
import Wavesurfer from 'react-wavesurfer';
import qwest from 'qwest';
import _ from 'underscore';
import AudioControls from '../components/AudioControls';
import SystemPicker from '../components/SystemPicker';
import LabelSlider from '../components/LabelSlider';

class Play extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      playing: false,
      pos: 0,
      duration: 0,
      choosingSystem: false,
      systems: [],
      labels: null
    }
  }

  upload = e => {
    let input = document.getElementById('labels-upload');
    input.click();
  }

  handleLabelsSelected = e => {
    let file = e.target.files[0];
    if (file) {
        let reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = e => {
          console.log(e.target.result)
          this.setState({ labels: e.target.result });
        }
        reader.onerror = e => {
            alert('Uploaded currently');
        }
    }
  }

  componentWillMount() {
    document.body.addEventListener('keydown', e => {
      console.log(e);
      if (e.keyCode == 32) {
        this.setState({ playing: !this.state.playing });
      } else if (e.keyCode == 65) {
        this.setState({ choosingSystem: true });
      } else if (e.keyCode == 39) {
        this.seek(this.state.pos + 5);
      } else if (e.keyCode == 37) {
        this.seek(this.state.pos - 5);
      }
    })
  }

  handlePosChange = (e) => {
    console.log(e)
    this.setState({
      pos: e.originalArgs[0]
    });
  }

  seek = (pos) => {
    this.setState({
      // Cap between 0 and duration
      pos: Math.min(this.state.duration, Math.max(0, pos))
    })
  }

  handleSystemPicked = system => {
    console.log(system)

    if (system) {
      this.setState({
        choosingSystem: false,
        systems: [].concat(this.state.systems, system)
      });
    } else {
      this.setState({ choosingSystem: false });
    }
  }

  removeSystem = (system) => {
    if (system.labels_file) {
      this.setState({ labels: null });
    } else {
      let index = this.state.systems.indexOf(system);
      let copy = this.state.systems.slice();
      copy.splice(index, 1);
      this.setState({ systems: copy });
    }
  };
  // {/*url={`/classify/${code}/${system.server_name}`}*/}
  renderSystem = (system, pos, code) => {
    let handleError = e => {
      this.removeSystem(system);
      alert('Failed to add.');
    };
    return (
      <div class="card card--spaced">
        <header class="card-header cf">
          <h2 class="pull-left">{ system.friendly_name }</h2>
          <button onClick={() => this.removeSystem(system)} class="btn btn-danger btn-medium pull-right">Remove</button>
        </header>
        <LabelSlider
              pos={pos}
              url='/labels/b032.txt'
              code={code}
              labels={system.labels}
              system={system}
              onError={handleError}
              onSelect={([start]) => this.seek(Math.max(0, start - 0.3))}
              />
      </div>
    );
  };

  render() {
    let addSystem = null;
    let labelsButton = null;
    if (this.state.labels) {
      labelsButton = this.renderSystem({
        friendly_name: 'Labels File',
        labels: this.state.labels,
        labels_file: true
      }, this.state.pos, this.props.params.code)
    } else {
      labelsButton = (
        <div class="hero hero--small">
          <div class="hero__inner">
            <div class="card button-box">
              <div class="button-box__inner">
                <span>Upload a labels file.</span>
                <button onClick={this.upload} class="btn btn-secondary btn-large">Upload</button>
                <input type="file" id="labels-upload" class="hidden" onChange={this.handleLabelsSelected}/>
              </div>
            </div>
          </div>
        </div>
      );
    }

    if (this.state.systems.length) {
      addSystem = <button class="btn btn-primary pull-right" onClick={() => this.setState({choosingSystem: true})}>Add Another System</button>
    } else {
      addSystem = (
        <div class="hero hero--small">
          <div class="hero__inner">
            <div class="card button-box">
              <div class="button-box__inner">
                <span>No systems added yet.</span>
                <button onClick={() => this.setState({choosingSystem: true})} class="btn btn-primary btn-large">Select a system!</button>
              </div>
            </div>
          </div>
        </div>
      );
    }
    let playButton;

    let loadingWaveSurfer = null;
    if (!this.state.duration) {
      loadingWaveSurfer = (
        <div class="loader-box">
          <div class="center-loader"><img src="/images/loading.svg" alt="loader"/></div>
        </div>
      )
    }

    return (
      <div>
        <SystemPicker
            open={this.state.choosingSystem}
            onChange={this.handleSystemPicked}/>
        <div class="overhang cf">
          <div class="page-inner">
            {/*<div class="pull-left">My_file.wav</div>*/}
            { loadingWaveSurfer }
            <Wavesurfer
              audioFile={`/audio/${this.props.params.code}/audio.wav`}
              pos={this.state.pos}
              zoom={100}
              options={{progressColor: '#F17300', waveColor: '#054A91',normalize: true, hideScrollbar: true}}
              onPosChange={this.handlePosChange}
              playing={this.state.playing}
              onReady={(p) => this.setState({duration: p.wavesurfer.getDuration()})}
            />
            <AudioControls
                  playing={this.state.playing}
                  onSeek={this.seek}
                  onPlayChange={playing => this.setState({playing})}
                  pos={this.state.pos} duration={this.state.duration} />
            { playButton }

            {/*<div class="buttons pull-right">
              <button class="btn btn-primary">Change audio file</button>
              <button class="btn btn-primary">Play</button>
              <button class="btn btn-primary">Pause</button>
            </div>*/}
          </div>
        </div>
        <div class="page-inner">
          { labelsButton }
          { this.state.systems.map(system => this.renderSystem(system, this.state.pos, this.props.params.code)) }
          { addSystem }
        </div>
      </div>)
    }
}


export default Play;
