import React from 'react';

export default class AudioUploader extends React.Component {

  constructor() {
    super();
    this.state = {
      file: null,
      uploading: false
    };
  }

  handleFileSelect = (e) => {
    e.preventDefault();
    let uploader = this.refs.fileUpload;
    uploader.click();
  };



  handleUpload = (e) => {
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

    let uploadMessage = this.state.file ? 'Confirm' : 'Upload an audio file to analyse (wav)'
    let button;

    if (this.state.uploading) {
      button = (
        <div class="loader-box">
          <div><img src="/images/loading.svg" alt="loader"/></div>
          <span class="loader-box__text">Uploading</span>
        </div>
      );
    } else if (this.state.file) {
      button = [
        <input onClick={this.handleFileSelect} type="submit" class="btn btn-secondary btn-large" value="Change" />,
        <input onClick={this.handleUploading} type="submit" class="btn btn-primary btn-large" value="Confirm" />
      ];
    } else {
      button = <input onClick={this.handleFileSelect} type="submit" class="btn btn-secondary btn-large" value={uploadMessage}/>
    }

    return (
      <div>
        <input onChange={this.handleUpload} ref="fileUpload" class="hidden file-upload" name="file" type="file"/>
        { button }
        <div class="notice">All audio files uploaded are publically visible.</div>
      </div>
    );
  }
}
