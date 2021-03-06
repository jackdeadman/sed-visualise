import React from 'react';
import { isEmpty, parseLabels, fetch } from '../utils/utils';

export default class LabelSlider extends React.Component {

  constructor(props) {
    super(props);
    this.scale = 100;
    this.labelOffset = 220;
    this.state = {
      labels: {},
      loading: false
    };
  }

  async componentDidMount() {
    this.setState({ loading: true });

    const classifier = this.props.system.id;
    const code = this.props.audioCode;
    let labels = null;
    try {
      labels = await this.props.api.classify(classifier, code);
      console.log(labels)
      labels = parseLabels(labels);
    } catch (e) {
      return this.props.onError(e);
    }

    this.setState({
      labels,
      loading: false
    });
  }

  labelVisible(start, pos, left, duration, end) {
    const slider = document.getElementById('slider');
    const sliderWidth = slider.offsetWidth;
    const offLeft = (left + duration) < 0;
    const offRight = left > sliderWidth;

    return !offLeft && !offRight;
  }

  // ===== RENDER =====

  renderLoading() {
    return (
      <div class="loader-box">
        <div><img src="/images/loading.svg" alt="loader"/></div>
        <span class="loader-box__text">Classifying</span>
      </div>
    );
  }

  renderLabel(start, pos, end) {
    const duration = (end - start) * this.scale;
    const left = ((start - pos) * this.scale) + this.labelOffset;

    // Don't render labels that are off the screen
    if (!this.labelVisible(start, pos, left, duration, end)) {
      return null;
    }

    const isActive = start < pos && end > pos;

    return (
      <div onClick={() => onSelect(data) }
            class={`event-block ${isActive ? 'active': ''}`}
            style={{width: `${duration}px`, left: `${left}px`}}>
      </div>
    )
  }

  renderLabelRow([label, labelData], pos, onSelect) {
    return (
      <li class="event">
          <label>{ label }</label>
          {labelData.map(([start, end]) => {
            return this.renderLabel(start, pos, end);
          })}
      </li>
    )
  }

  renderLabels(labels, pos, onSelect) {
    let orderedLabelKeys = labels.orderedKeys;

    return orderedLabelKeys.map(label => {
      const labelData = labels[label];
      return this.renderLabelRow([ label, labelData ], pos, onSelect);
    });
  }

  render() {
    let { timeline, onSelect, onRemove, system } = this.props;

    return (
      <div class="card card--spaced">
        <header class="card-header cf">
          <h2 class="pull-left">{ system.title }</h2>
          <button onClick={() => onRemove(system)} class="btn btn-danger btn-medium pull-right">Remove</button>
        </header>
        <div class="label-slider" id="slider">
          <ul class="events">
            { isEmpty(this.state.labels)
                  ? this.renderLoading()
                  : this.renderLabels(this.state.labels, timeline.pos, onSelect)
            }
          </ul>
        </div>
      </div>
    );
  };

}
