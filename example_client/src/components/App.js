import React from 'react';
import SelectorsContainer from '../containers/SelectorsContainer';
import FeeTablesContainer from '../containers/FeeTablesContainer';

import 'font-awesome/css/font-awesome.css';
import '../css/govuk-elements.css';
import '../css/app.css';

const App = ({ apiBaseURL }) => (
  <div className="content">
    <main id="content">
      <SelectorsContainer />
      <FeeTablesContainer />
    </main>
  </div>
);

export default App;
