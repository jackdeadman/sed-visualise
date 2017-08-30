import React from 'react';
import HiddenFileUpload from './HiddenFileUpload';
import { SiteButton } from './bundles/buttons';

const UploadLabelsButton = (onClick) => (
    <div class="hero hero--small">
        <div class="hero__inner">
            <div class="card button-box">
                <div class="button-box__inner">
                    <span>Upload a labels file.</span>
                    <button onClick={onClick} class="btn btn-secondary btn-large">
                        Upload
                    </button>
                </div>
            </div>
        </div>
    </div>
);

export default class LabelsPicker extends React.Component {
    
    openFilePicker() {
        this.refs.labelInput.invoke();
    };

    async handleFileChange() {
        const file = e.target.files[0];
        if (file) return;

        const reader = new TextFileReader();
        
        let rawLabels;
        try {
            rawLabels = reader.read();
        } catch (e) {
            return this.props.onError('Failed to read text file.');
        }

        let labels;
        try {
            labels = new EventLabels(await rawLabels);
        } catch (e) {
            return this.props.onError('Failed to parse labels file.');
        }

        this.props.onChange(labels);
    }

    render() {
        const { labels, onClick } = this.props;

        return (
            <div>
                <HiddenFileUpload ref="labelInput" onChange={this.handleFileChange}/>
                { labels
                    ? <LabelSlider name="Labels file" labels={labels}
                            onRemove={this.props.onRemove} />
                    : <UploadLabelsButton onClick={onClick} />
                }
            </div>
        );
    }
};