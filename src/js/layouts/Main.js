import React from 'react';
import Wavesurfer from 'react-wavesurfer';
import qwest from 'qwest';
import _ from 'underscore';
import AudioControls from '../components/AudioControls';

function throttle(fn, threshhold, scope) {
  threshhold || (threshhold = 250);
  var last,
      deferTimer;
  return function () {
    var context = scope || this;

    var now = +new Date,
        args = arguments;
    if (last && now < last + threshhold) {
      // hold on to it
      clearTimeout(deferTimer);
      deferTimer = setTimeout(function () {
        last = now;
        fn.apply(context, args);
      }, threshhold);
    } else {
      last = now;
      fn.apply(context, args);
    }
  };
}


class Main extends React.Component {
  render() {
    let playButton;

    return (
      <div class="main-layout">
        <header class="main-header">
          <h1>Sound Event Detection Visualisation</h1>
        </header>
        { this.props.children }
      </div>)
    }
}


export default Main;
