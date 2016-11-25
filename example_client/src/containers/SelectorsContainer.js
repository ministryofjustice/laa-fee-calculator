import { connect } from 'react-redux';
import Selectors from '../components/Selectors';
import { setScenario, setAdvocateType, setOffenceClass, setUplift, setThird } from '../actions';

const showThird = (state) => {
  const selectedScenario = state.scenarios.filter(s => s.id === state.selectedScenarioId)[0];
  return selectedScenario === undefined ? false : selectedScenario['force_third'];
}

const mapStateToProps = (state) => Object.assign({ showThird: showThird(state) }, state);

const mapDispatchToProps = ({
  handleScenarioChange: setScenario,
  handleAdvocateTypeChange: setAdvocateType,
  handleOffenceClassChange: setOffenceClass,
  setUplift,
  setThird
});

const SelectorsContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Selectors);

export default SelectorsContainer;
