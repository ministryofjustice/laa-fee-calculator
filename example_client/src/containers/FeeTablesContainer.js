import { connect } from 'react-redux';
import FeeTables from '../components/FeeTables';
import { setQuantity, incQuantity, decQuantity } from '../actions';

function getFeeTypes(prices) {
  const feeTypes = {};
  for (const price of prices) {
    const feeType = price['fee_type'];
    if (!(feeType.id in feeTypes)) {
      feeTypes[feeType.id] = feeType;
    };
  };
  return Object.values(feeTypes);
}

function getFeeTypeIdToPrices(feeTypes, prices, selectedAdvocateTypeId, selectedOffenceClassId, selectedThird) {
  const feeIdToPrices = new Map();
  for (const price of prices) {

    const advocateType = price['advocate_type'];
    const offenceClass = price['offence_class'];
    const third = price['third'];
    const feeTypeId = price['fee_type']['id'];

    const priceList = feeIdToPrices.get(feeTypeId) || [];
    if ((advocateType === null || advocateType.id === selectedAdvocateTypeId)
        && (offenceClass === null || offenceClass.id === selectedOffenceClassId)
        && (third === null || selectedThird === third)) {
      const item = {
        id: price['id'],
        feePerUnit: parseFloat(price['fee_per_unit']),
        limitFrom: price['limit_from'],
        limitTo: price['limit_to'],
        unit: price['unit'],
        upliftPercent: price['uplift_percent']
      }
      priceList.push(item);
    }
    feeIdToPrices.set(feeTypeId, priceList.sort((a, b) => a.limitFrom - b.limitFrom));
  };
  return feeIdToPrices;
}


function getFees(feeTypes, feeIdToPrices, feeIdToQty, isUplifted) {
  return feeTypes.map(feeType => {
    const feeId = feeType.id;
    const prices = feeIdToPrices.get(feeId) || [];
    const qty = feeIdToQty.get(feeId) || 0;

    const attribute = {};
    let remaining = qty;
    let sum = 0;

    for (const price of prices) {
      const { id, limitFrom, limitTo, unit, upliftPercent } = price;
      let feePerUnit = price.feePerUnit;
      if (isUplifted) {
        feePerUnit += feePerUnit * upliftPercent / 100;
      }
      let val;
      if (limitTo === null || remaining <= (limitTo - limitFrom + 1)) {
        val = remaining;
      } else {
        val = limitTo - limitFrom + 1;
      };
      attribute[id] = val;
      remaining -= val;
      if (unit !== 'Fixed Amount') {
        sum += feePerUnit * val;
      } else {
        sum += val > 0 ? feePerUnit : 0;
      };
    }
    if (remaining > 0) {
      console.log(`qty ${qty} not attributed for feeId ${feeId}`);
    }

    const amount = { sum, attribute };

    return Object.assign({ prices, qty, amount }, feeType);
  });
}


const mapStateToProps = (state) => {
  const feeTypes = getFeeTypes(state.prices);
  const feeIdToPrices = getFeeTypeIdToPrices(
    feeTypes,
    state.prices,
    state.selectedAdvocateTypeId,
    state.selectedOffenceClassId,
    state.selectedThird);
  const fees = getFees(feeTypes, feeIdToPrices, state.feeIdToQty, state.isUplifted);
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
