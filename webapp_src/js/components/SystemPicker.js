import React from 'react';

import Modal from './Modal';

import {
  mod, Key, generateButtonClass, fetchJSON
} from '../utils/utils';

export default class SystemPicker extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      activeSystem: null,
      loadingSystems: false,
      errorText: null,
      systems: []
    }
  }

  get currentIndex() {
      return this.state.systems.indexOf(this.state.activeSystem);
  }

  async componentDidMount() {
    this.setState({ loadingSystems: true });
    let errorText = null;
    let classifiers = [];
    try {
        classifiers = await this.props.classifierFactory.all();
    } catch (e) {
        errorText = e.errorText;
    }

    this.setState({
      loadingSystems: false,
      errorText,
      systems: classifiers
    }, this.bindKeys);

  }

  componentWillUnmount() {
    document.body.removeEventListener('keydown', this.keyHandler);
  }

  componentWillReceiveProps(props) {
    const closing = !this.props.open && props.open;
    if (closing) {
      this.setState({ activeSystem: null });
    }
  }

  selectSystem(system) {
    console.log(system);
    this.setState({ activeSystem: system })
  }

  close() {
    this.props.onChange(null);
  }

  keyHandler = e => {

    if (e.keyCode === Key.ENTER) {
      return this.props.onChange(this.state.activeSystem);
    }

    const currentIndex = this.currentIndex;
    let indexChange = 0;

    if (e.keyCode === Key.UP) {
      indexChange = -1;
    } else if (e.keyCode === Key.DOWN) {
      indexChange = 1;
    } else {
      // no op
      return;
    }

    const newIndex = mod(index + indexChange, systems.length);

    this.setState({
      activeSystem: systems.get(newIndex)
    });
  }

  bindKeys() {
    document.body.addEventListener('keydown', this.keyHandler);
  }

  // ===== RENDER =====

  renderAddSystemButton() {
    return (
      <button onClick={
                () => this.props.onChange(this.state.activeSystem) }
                class="btn btn-primary pull-right">
        Add {this.state.activeSystem.title}
      </button>
    );
  }

  renderFooter() {
    return (
      <div class="card-footer cf">
        { this.state.activeSystem
          ? this.renderAddSystemButton()
          : null }
      </div>
    );
  }

  renderSystemListItem = (system) => {
    const isActive = system == this.state.activeSystem;
    console.log(system);
    console.log('this', this);

    return (
      <li onClick={ () => this.selectSystem(system) }
              class={`system ${isActive ? 'active' : ''}`}>
        { system.title }
      </li>
    )
  }

  renderSystems(systems) {
    return (
      <div class="select-systems">
        <ul class="system-list">
          { systems.map(this.renderSystemListItem).asArray }
        </ul>
        { this.renderFooter() }
      </div>
    );
  }

  render() {
    return (
      <div>
        { this.state.errorText &&
            `<div>${this.state.errorText}<div>`}

        { this.state.loadingSystems
              ? <div>Loading classifiers...</div>
              : this.renderSystems(this.state.systems) }
      </div>
    );
  }
}
