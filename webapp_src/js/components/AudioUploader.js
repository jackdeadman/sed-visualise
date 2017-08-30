import React from 'react';

import HiddenFileUpload from './HiddenFileUpload';
import { SiteSubmitButton } from './bundles/buttons';
import Loader from './Loader';

const ConfirmationBox = ({ onChange, onUpload }) => (
    <div>
      <SiteSubmitButton type="secondary" onChange={onChange}
          size="large" message="Change"/>
      <SiteSubmitButton type="primary" onClick={onUpload}
          size="large" message="Confirm"/>
    </div>
);

const FileSelectorPrompts = ({ file, uploading, onChange, onUpload }) => {
    if (uploading) {
      return <Loader message="Uploading..."/>
    } else if (file) {
      return <ConfirmationBox
                  onChange={onChange}
                  onUpload={onUpload} />
    } else {
      // Intial state
      return <SiteSubmitButton onClick={onChange}
                size="large" type="secondary" submitOnClick={false}
                message="Upload an audio file to analyse (wav)"/>
    }
};

export default class AudioUploader extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      file: null,
      uploading: false
    };
  }

  openFilePicker() {
    if (this.refs.fileInput) {
      this.refs.fileInput.invoke();
    }
  };

  handleFileChosen = (e) => {
    if (e.target.files.length) {
      this.setState({
        file: e.target.files[0]
      });
    }
  };

  handleUploading = (e) => {
    e.preventDefault();
    this.setState({ uploading: true }, this.props.onUpload);
  }

  render() {
    const { file, uploading } = this.state;

    return (
      <div>
        <HiddenFileUpload onChange={this.handleFileChosen} ref="fileInput"/>
        <FileSelectorPrompts file={file} uploading={uploading}
              onChange={this.openFilePicker.bind(this)} onUpload={this.handleUploading} />
        <div class="notice">
          All audio files uploaded are publically visible.
        </div>
      </div>
    );
  }
}
