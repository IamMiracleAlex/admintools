import React from 'react';

const URLStatus = ({ record: { url }, onChange, checked }) => {
    return (
        <>
            <div className="flex justify-content-between align-items-center" style={{ width: 400 }}>
                <input
                    type="checkbox"
                    id="exampleCheck1"
                    onChange={onChange}
                    style={{ marginRight: '14px' }}
                    checked={checked}
                />
                <a href={url} target="_blank" rel="noreferrer">
                    {url}
                </a>
            </div>
        </>
    );
};

export default URLStatus;
