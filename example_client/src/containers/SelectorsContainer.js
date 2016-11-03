import { connect } from 'react-redux';
import Selectors from '../components/Selectors';
import { setScenario, setAdvocateType, setOffenceClass } from '../actions';

const mapStateToProps = (state) => state;

const mapDispatchToProps = ({
  handleScenarioChange: setScenario,
  handleAdvocateTypeChange: setAdvocateType,
  handleOffenceClassChange: setOffenceClass
});

const SelectorsContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(Selectors)

export default SelectorsContainer;
