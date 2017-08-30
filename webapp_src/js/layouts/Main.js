import React from 'react';

const Main = props => {
    return (
      <div class="main-layout">
         <header class="main-header">
              <h1>Sound Event Detection Visualisation</h1>
          </header>
          { props.children }
      </div>
    )
};

export default Main;
