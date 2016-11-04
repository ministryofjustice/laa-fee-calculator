import React from 'react';
import Select from './Select';

const Selectors = ({
  scenarios,
  selectedScenarioId,
  handleScenarioChange,
  advocateTypes,
  selectedAdvocateTypeId,
  handleAdvocateTypeChange,
  offenceClasses,
  selectedOffenceClassId,
  handleOffenceClassChange
}) => (
  <div>
    <h3 className="heading-medium">Options</h3>
    <Select
      id="scenario"
      items={ scenarios }
      label="Scenario"
      selected={ selectedScenarioId }
      handleChange={ e => handleScenarioChange(parseInt(e.target.value, 10)) }
    />
    <Select
      id="advocate-type"
      items={ advocateTypes }
      label="Advocate type"
      selected={ selectedAdvocateTypeId }
      handleChange={ e => handleAdvocateTypeChange(parseInt(e.target.value, 10)) }
    />
    <Select
      id="offence-class"
      items={ offenceClasses }
      label="Offence class"
      selected={ selectedOffenceClassId }
      handleChange={ e => handleOffenceClassChange(parseInt(e.target.value, 10)) }
    />
  </div>
);

export default Selectors;
