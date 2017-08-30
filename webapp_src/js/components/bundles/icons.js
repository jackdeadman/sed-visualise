import React from 'react';

export const FontAwesomeIconGenerator = type => () => (
    <i class={`fa fa-${type}`} aria-hidden="true"></i>
);

export const PlayIcon = FontAwesomeIconGenerator('play');
export const PauseIcon = FontAwesomeIconGenerator('pause');