import React from 'react';
import Select from './Select';
import RadioWithLabel from './RadioWithLabel';

const Selectors = ({
  scenarios,
  selectedScenarioId,
  handleScenarioChange,
  advocateTypes,
  selectedAdvocateTypeId,
  handleAdvocateTypeChange,
  offenceClasses,
  selectedOffenceClassId,
  handleOffenceClassChange,
  isUplifted,
  setUplift,
}) => {
  const Uplift = (
    <div className="form-group">
      <label className="form-label">Uplift?</label>
      <fieldset className="inline">
        <RadioWithLabel
          id="uplift-yes"
          value="yes"
          label="Yes"
          selected={ isUplifted }
          handleChange={ () => setUplift(true) }
        />
        <RadioWithLabel
          id="uplift-no"
          value="no"
          label="No"
          selected={ !isUplifted }
          handleChange={ () => setUplift(false) }
        />
      </fieldset>
    </div>);
  return (
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
        handleChange={ e => handleAdvocateTypeChange(e.target.value) }
      />
      <Select
        id="offence-class"
        items={ offenceClasses }
        label="Offence class"
        selected={ selectedOffenceClassId }
        handleChange={ e => handleOffenceClassChange(e.target.value) }
      />
      { Uplift }
    </div>
  )
};

export default Selectors;
