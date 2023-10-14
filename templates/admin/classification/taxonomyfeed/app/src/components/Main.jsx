import React, { useState } from 'react';
import { Tabs, Tab } from 'react-bootstrap';
import ReactNotification from 'react-notifications-component';
import { Hierarchy } from './hierarchy/Hierarchy';
import { Facet } from './facet/Facet';
import { NodeFacet } from './node-facet/NodeFacet';

export const Main = () => {
    const [key, setKey] = useState('node-facet');

    return (
        <div className="container-fluid">
            <ReactNotification />
            <header>Taxonomy Change Feed</header>
            <Tabs
                id="controlled-tab-example"
                activeKey={key}
                onSelect={(k) => setKey(k)}
                className="tcf-tabs"
            >
                <Tab eventKey="hierarchy" title="Hierarchy">
                    {key === 'hierarchy' && <Hierarchy />}
                </Tab>
                <Tab eventKey="facets" title="Facets">
                    {key === 'facets' && <Facet />}
                </Tab>
                <Tab eventKey="node-facet" title="Node-Facet Relationship">
                    {key === 'node-facet' && <NodeFacet />}
                </Tab>
            </Tabs>
        </div>
    );
};
