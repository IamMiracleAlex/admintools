import React from 'react';

const URLState = ({ state }) => {
    if (state.bad) {
        return 'Bad';
    } else if (state.known) {
        return 'Known';
    } else if (state.raw) {
        return 'Raw';
    } else if (state.tbaq) {
        return 'TBAQ';
    } else {
        return '';
    }
};

export default URLState;
