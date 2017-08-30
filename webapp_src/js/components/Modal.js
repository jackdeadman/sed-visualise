import React from 'react';

export default class Modal extends React.Component {

    componentWillReceiveProps(nextProps) {
        const opening = !this.props.open && nextProps.open;
        // accessibility
        if (opening) {
            // Need to let the focus finish first
            setTimeout(() => document.activeElement.blur(), 1);
        }
    }

    handleModalClick = evt => {
        if (evt.target.classList.contains('modal')) {
            this.props.onClose();
        }
    }

    render() {
        const { open, title, onClose, children } = this.props;
        if (!open) return null;
        
        return (
        <div class="modal"
                onClick={this.handleModalClick}>
            <div class="modal__inner">
                <header class="card-header cf">
                <h2 class="pull-left">{title}</h2>
                <button class="btn btn-danger btn-medium pull-right"
                        onClick={onClose}>
                    <i class="fa fa-times" aria-hidden="true"></i>
                </button>
                </header>
                { children }       
            </div>
        </div>)
    }
};
