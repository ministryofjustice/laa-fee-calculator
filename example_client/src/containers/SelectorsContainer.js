import { connect } from 'react-redux';
import Selectors from '../components/Selectors';
import { setScenario, setAdvocateType, setOffenceClass, setUplift } from '../actions';

const mapStateToProps = (state) => state;

const mapDispatchToProps = ({
  handleScenarioChange: setScenario,
  handleAdvocateTypeChange: setAdvocateType,
  handleOffenceClassChange: setOffenceClass,
  setUplift
});

const SelectorsContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Selectors);

export default SelectorsContainer;
