import React from 'react';
import ClickOutside from 'react-click-outside';

export default class SystemPicker extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      activeSystem: null,
      systems: [
        {
          id: 0,
          friendly_name: 'Baseline (Home)',
          features: ['mfcc'],
          scene: 'home',
          norm_path: 'standard/baseline',
          model_path: 'standard/components/16/baseline'
        },

        {
          id: 1,
          friendly_name: 'MFCCs + RMS Energy (Home)',
          features: ['mfcc', 'energy'],
          scene: 'home',
          norm_path: 'standard/energy',
          model_path: 'standard/components/16/energy'
        },

        {
          id: 2,
          friendly_name: 'MFCCs + Rolloff (Home)',
          features: ['mfcc', 'rolloff'],
          scene: 'home',
          norm_path: 'standard/rolloff',
          model_path: 'standard/components/16/rolloff'
        },

        {
          id: 3,
          friendly_name: 'MFCCs + Flux (Home)',
          features: ['mfcc', 'flux'],
          scene: 'home',
          norm_path: 'standard/flux',
          model_path: 'standard/components/16/flux'
        },

        {
          id: 4,
          friendly_name: 'MFCCs + Flux (Residential Area)',
          features: ['mfcc', 'flux'],
          scene: 'residential_area',
          norm_path: 'standard/flux',
          model_path: 'standard/components/16/flux'
        },

        {
          id: 5,
          friendly_name: 'MFCCs + Flux + Rolloff + Energy + Spread (Street)',
          features: ['mfcc', 'flux', 'rolloff', 'energy', 'spread'],
          scene: 'street',
          norm_path: 'augmented/combined',
          model_path: 'augmented/combined',
          threshold: 110
        },

        {
          id: 6,
          friendly_name: 'MFCCs (Street)',
          features: ['mfcc'],
          scene: 'street',
          norm_path: 'standard/baseline-street',
          model_path: 'standard/baseline-street',
          threshold: 35
        }
      ]
    }
  }

  handleSelect = (system) => {
    this.setState({ activeSystem: system })
  }

  mod(x, y) {
    // lol Javascript
    return ((x % y) + y) % y;
  }

  componentWillMount(props) {
    document.body.addEventListener('keydown', e => {
      if (!this.props.open) { return; }
      console.log(e);
      if (e.keyCode == 27) {
        this.props.onChange(null)
      }

      let systems = this.state.systems;
      let index = systems.indexOf(this.state.activeSystem);

      if (e.keyCode === 38) {
        this.setState({ activeSystem: systems[this.mod(index-1, systems.length)] });
      } else if (e.keyCode === 40) {
        this.setState({ activeSystem: systems[this.mod(index+1, systems.length)] });
      } else if (e.keyCode === 13) {
        this.props.onChange(this.state.activeSystem);
      }
    })
  }

  componentWillReceiveProps(nextProps) {
    if (!this.props.open && nextProps.open) {
      this.setState({ activeSystem: null });
    }
  }

  render() {
    if (!this.props.open) { return null; }

    let footer = (
      <div class="card-footer cf">
        { this.state.activeSystem ? <button onClick={() => this.props.onChange(this.state.activeSystem)} class="btn btn-primary pull-right">Add {this.state.activeSystem.friendly_name}</button> : null }
      </div>
    );

    return (
      <div class="modal">
          <div class="modal__inner">
            <ClickOutside onClickOutside={() => this.props.onChange(null)}>
            <header class="card-header cf">
              <h2 class="pull-left">Select a system</h2>
              <button class="btn btn-danger btn-medium pull-right" onClick={() => this.props.onChange(null)}><i class="fa fa-times" aria-hidden="true"></i></button>
            </header>
            <div class="select-systems">
              <ul class="system-list">
                { this.state.systems.map(system => {
                  let active = system == this.state.activeSystem;
                  return <li onClick={() => this.handleSelect(system)} class={`system ${active ? 'active' : ''}`}>{system.friendly_name}</li>
                }) }
              </ul>
              { footer }
            </div>
            </ClickOutside>
          </div>
      </div>
    );
  }
}
