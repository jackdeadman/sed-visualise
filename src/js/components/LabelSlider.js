import React from 'react';
import qwest from 'qwest';
import _ from 'underscore';


const renderLabels = (labels, pos, onSelect) => {
  let slider = document.getElementById('slider');
  let orderedLabelKeys = labels.orderedLabelKeys;
  let sliderWidth = slider.offsetWidth;

  return orderedLabelKeys.map(label => {
    let labelData = labels[label];
    return (
      <li class="event">
        <label>{label}</label>
        {labelData.map(data => {
          let [start, end] = data;
          let duration = end - start;
          duration *= 100;
          let left = start - pos;
          left = (left * 100) + 220;
          if (left > sliderWidth) return null;
          if ((left + duration) < 0) return null;
          let active = start < pos && end > pos;
          return <div onClick={() => onSelect(data) } class={`event-block ${active ? 'active': ''}`} style={{width: `${duration}px`, left: `${left}px`}}></div>
        })}
      </li>
    );
  });

  return events;
}

const parseLabels = (response) => {
  let labels = {};
  for (let line of response.split('\n')) {
    if (line === '') { continue; }
    let [start, end, label ] = line.split('\t');
    if (start && end && label) {
      if (label in labels) {
        labels[label].push([parseFloat(start), parseFloat(end)]);
      } else {
        labels[label] = [[parseFloat(start), parseFloat(end)]]
      }
    } else {
      throw new Error('Cannot parse');
    }
  }
  let orderedLabelKeys = Object.keys(labels);
  orderedLabelKeys.sort();
  labels.orderedLabelKeys = orderedLabelKeys;
  return labels;
}

const renderLoading = () => {
  return (
    <div class="loader-box">
      <div><img src="/images/loading.svg" alt="loader"/></div>
      <span class="loader-box__text">Classifying</span>
    </div>);
};

class LabelSlider extends React.Component {

  constructor(props) {
    super(props);
    this.state = { labels: {} };
    this.count = 0;
  }

  componentDidMount() {
      try {
        if(this.props.labels && this.props.labels.length) {
          let labels = parseLabels(this.props.labels);
          this.setState({ labels });
        } else if (this.props.system) {
          let url = `/classify/${this.props.code}`
          qwest.get(url, this.props.system)
          .then((_, response) => {
            let labels = parseLabels(response);
            this.setState({ labels });
          })
          .catch(this.props.onError);
        }
      } catch(e) {
        console.log(e)
        this.props.onError(e);
      }
  }

  render() {
    let { pos, onSelect } = this.props;
    return (
      <div class="label-slider" id="slider">
        <ul class="events">
          { _.isEmpty(this.state.labels)
                ? renderLoading()
                : renderLabels(this.state.labels, pos, onSelect)
          }
        </ul>
      </div>)
  };

}

export default LabelSlider;
