import React from 'react';
import { Link } from 'react-router-dom';

import AudioUploader from '../components/AudioUploader';

const submitForm = (e) => {
  let form = document.getElementById('form');
  form.submit();
}

const Index = (props) => {
  return (
    <div class="page">
      <div class="hero">
        <div class="hero__inner">
          <div class="card button-box">
            <div class="button-box__inner">
              <form id="form" method="post" encType="multipart/form-data" action="/upload" class="upload-form">
                <AudioUploader onUpload={submitForm}/>
                <Link to={'/play/w664'} class="btn btn-primary btn-large">Or use an example file.</Link>
                {/*<Link to={'/play/w664'} class="btn btn-primary btn-large">Test</Link>*/}
                {/*<input class="file-upload" name="file" type="file"/>
                <Link to={'/play/w664'} class="btn btn-primary btn-large">Test</Link>
                <input type="submit" class="btn btn-primary btn-large" value="Upload"/>*/}
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Index;
