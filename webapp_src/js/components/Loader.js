import React from 'react';

const Loader = ({ message }) => (
    <div class="loader-box">
        <div><img src="/images/loading.svg" alt="loader"/></div>
        <span class="loader-box__text">{ message }</span>
    </div>
);

export default Loader;