import React from 'react';
import { AllUrls } from './components/AllUrls';

import history from './history';

const App = () => {
    const [, forceUpdate] = React.useReducer((x) => x + 1, 0);

    React.useEffect(() => {
        // listen for changes to the URL and force the app to re-render
        history.listen(() => {
            forceUpdate();
        });
    }, []);

    return <AllUrls />;
};

export default App;
