import { connect } from 'react-redux';
import FeeTables from '../components/FeeTables';
import { setQuantity, incQuantity, decQuantity } from '../actions';

function getFeeTypes(scenarios, selectedScenarioId) {
  const scenario = scenarios.filter(item => item['id'] === selectedScenarioId)[0];
  return scenario ? scenario['fee_types'] : [];
}

function getFeeIdToPrice(prices) {
  const feeIdToPrice = new Map();
  for (const price of prices) {
    const feeTypeId = price['fee_type']['id'];
    const priceList = feeIdToPrice.get(feeTypeId) || [];
    priceList.push(price);
    feeIdToPrice.set(feeTypeId, priceList);
  }
  for (const [feeTypeId, priceList] of feeIdToPrice.entries()) {
    if (priceList.length > 1) {
      console.log('multiple prices found for feeTypeId:', feeTypeId, 'prices:', prices, '!');
    }
    feeIdToPrice.set(feeTypeId, parseFloat(priceList[0]['amount']));
  };
  return feeIdToPrice;
}


function getFees(feeTypes, feeIdToPrice, feeIdToQty) {
  return feeTypes.map(feeType => {
    const feeId = feeType.id;
    const price = feeIdToPrice.get(feeId);
    const qty = feeIdToQty.get(feeId) || 0;
    const amount = price ? price * qty : 0;
    return Object.assign({ price, qty, amount}, feeType);
  });
}


const mapStateToProps = (state) => {
  const feeTypes = getFeeTypes(state.scenarios, state.selectedScenarioId);
  const feeIdToPrice = getFeeIdToPrice(state.prices);
  const fees = getFees(feeTypes, feeIdToPrice, state.feeIdToQty);
  const basicFees = fees.filter( fee => fee['is_basic'] );
  const miscFees = fees.filter( fee => !fee['is_basic'] );
  return Object.assign({ basicFees, miscFees }, state);
};


const mapDispatchToProps = ({
  handleChange: setQuantity,
  handlePlus: incQuantity,
  handleMinus: decQuantity
});


const FeeTablesContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(FeeTables);


export default FeeTablesContainer;
