import React from 'react';

const identify = () => {};

const onClickProxy = (e, onClick, submitOnClick) => {
    if (!submitOnClick) {
        e.preventDefault();
    }
    onClick(e);
};

export const SiteSubmitButton = ({ message, type, size, onClick, submitOnClick }) => (
    <input onClick={e => onClickProxy(e, onClick, submitOnClick)}
                  type="submit"
                  class={`btn btn-${type} btn-${size}`}
                  value={ message }/>
);

export const SiteButton = ({type, size, onClick=identify, children}) => (
    <button class={`btn btn-${type} btn-${size}`} onClick={onClick}>
        { children }
    </button>
);