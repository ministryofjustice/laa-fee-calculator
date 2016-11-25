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
  showThird,
  selectedThird,
  setThird
}) => {
  const ThirdRadios = (
    <div className="form-group">
      <label className="form-label">Which third?</label>
      <fieldset className="inline">
        <RadioWithLabel
          id="1st"
          value="1st"
          label="1st"
          selected={ selectedThird === 1 }
          handleChange={ () => setThird(1) }
        />
        <RadioWithLabel
          id="2nd"
          value="2nd"
          label="2nd"
          selected={ selectedThird === 2 }
          handleChange={ () => setThird(2) }
        />
        <RadioWithLabel
          id="3nd"
          value="3nd"
          label="3rd"
          selected={ selectedThird === 3 }
          handleChange={ () => setThird(3) }
        />
      </fieldset>
    </div>);
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
      { showThird ? ThirdRadios: null}
      { Uplift }
    </div>
  )
};

export default Selectors;
