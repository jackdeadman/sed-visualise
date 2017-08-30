import React from 'react';

export default class HiddenFileUpload extends React.Component {
    
    invoke() {
        this.refs.element.click();
    }
    
    render() {
        return (
            <input onChange={ this.props.onChange }
                    ref="element"
                    class="hidden file-upload"
                    name="file" type="file"/>
        );
    }
}
