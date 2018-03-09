import React from 'react';
import { SiteButton } from './bundles/buttons';
import LabelSlider from './LabelSlider';

const AddMessageWithSystems = ({ onClick }) => (
    <button class="btn btn-primary pull-right" onClick={onClick}>
        Add Another System
    </button>
);

const AddMessageWithNoSystems = ({ onClick }) => (
    <div class="hero hero--small">
        <div class="hero__inner">
            <div class="card button-box">
            <div class="button-box__inner">
                <span>No systems added yet.</span>
                <SiteButton type="primary" size="large" onClick={onClick}>
                    Select a system!
                </SiteButton>
            </div>
            </div>
        </div>
    </div>
);


const SystemOutputContainer = props => {
    const { systems, onAdd,
            onRemove, timeline, code, api, audioCode } = props;
    return (
        <div>
            <div>
                { systems.map(system => (
                    <LabelSlider system={system} onRemove={onRemove}
                        timeline={timeline} onError={console.error}
                        api={api} audioCode={audioCode}/>
                )).asArray}
            </div>

            {systems.length
             ? <AddMessageWithSystems onClick={onAdd}/>
             : <AddMessageWithNoSystems onClick={onAdd}/>
            }
        </div>
    );
};

export default SystemOutputContainer;
