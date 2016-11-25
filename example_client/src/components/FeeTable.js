import React, { PropTypes } from 'react';

const displayPrice = ( price, isUplifted ) => {
  if (price === undefined) {
    return '';
  }
  let feePerUnit = parseFloat(price.feePerUnit);
  let prefix = '\u00a3';
  const upliftPercent = parseFloat(price.upliftPercent);
  if (isUplifted && upliftPercent !== 0) {
    feePerUnit += feePerUnit * upliftPercent / 100;
    prefix = '\u2191' + prefix;  // upwards arrow
  }
  return `${ prefix }${ feePerUnit.toFixed(2) } / ${price.unit.toLowerCase()}`;
}

const SingleFee = (fee, isUplifted, handlePlus, handleMinus, handleChange) => {
  const { id, name, code, prices, qty, amount } = fee;
  const price = prices[0];
  let exceedMax;
  if ( price === undefined || price.limitTo === null ) {
    exceedMax = false;
  } else if ( price.limitTo < qty ) {
    exceedMax = true;
  }
  const qtyClassName = exceedMax ? "quantity-input error" : "quantity-input";
  return (
    <tr key={ id }>
      <td>{ name }</td>
      <td>{ code }</td>
      <td>{ displayPrice(price, isUplifted) }</td>
      <td>{ price !== undefined ? `${price.limitFrom}~${price.limitTo || ''}` : '' }</td>
      <td className="quantity-td">
        <i className="fa fa-plus-circle" aria-hidden="true" onClick={ e => handlePlus(id) }></i>
        <input type="number" className={ qtyClassName } value={ qty } onChange={ e => handleChange(id, e.target.value) }/>
        <i className="fa fa-minus-circle" aria-hidden="true" onClick={ e => handleMinus(id) }></i>
        { exceedMax ? (<p className="error-message">{`max ${price.limitTo}`}</p>) : null }
      </td>
      <td>{ amount.sum !== 0 ? `\u00a3${ amount.sum.toFixed(2) }` : '' }</td>
    </tr>
  );
}


const MultiFee = (fee, isUplifted, handlePlus, handleMinus, handleChange) => {
  const { id, name, code, amount, qty, prices } = fee;

  const lastPrice = prices[ prices.length -1 ];
  let exceedMax;
  if ( lastPrice === undefined || lastPrice.limitTo === null ) {
    exceedMax = false;
  } else if ( lastPrice.limitTo < qty ) {
    exceedMax = true;
  }

  const qtyClassName = exceedMax ? "quantity-input error" : "quantity-input";
  const rowSpan = fee.prices.length + 1;
  const firstRow = (
    <tr key={ id }>
      <td rowSpan={ rowSpan }>{ name }</td>
      <td rowSpan={ rowSpan }>{ code }</td>
      <td></td>
      <td></td>
      <td className="quantity-td">
        <i className="fa fa-plus-circle" aria-hidden="true" onClick={ e => handlePlus(id) }></i>
        <input type="number" className={ qtyClassName } value={ qty } onChange={ e => handleChange(id, e.target.value) }/>
        <i className="fa fa-minus-circle" aria-hidden="true" onClick={ e => handleMinus(id) }></i>
        { exceedMax ? (<p className="error-message">{`max ${lastPrice.limitTo}`}</p>) : null }
      </td>
      <td rowSpan={ rowSpan }>{ amount.sum !== 0 ? `\u00a3${ amount.sum.toFixed(2) }` : '' }</td>
    </tr>
  );
  const priceRows = prices.map((price, ind)=> (
    <tr key={ `${id}-${ind}` }>
      <td>{ displayPrice(price, isUplifted) }</td>
      <td>{ price !== undefined ? `${price.limitFrom}~${price.limitTo || ''}` : '' }</td>
      <td>{ amount.attribute[price.id] }</td>
    </tr>
  ));
  return [firstRow, ...priceRows];
}


const Fee = ( fee, isUplifted, handlePlus, handleMinus, handleChange ) => {
  if (fee.prices.length <= 1) {
    return SingleFee(fee, isUplifted, handlePlus, handleMinus, handleChange)
  }
  return MultiFee(fee, isUplifted, handlePlus, handleMinus, handleChange);
}

const FeeTable = ({ fees, isUplifted, handleChange, handlePlus, handleMinus }) => {
  if (fees.length === 0) {
    return null;
  }
  return (
    <table>
      <thead>
        <tr>
          <th scope="col">Fee type</th>
          <th scope="col">CCR Subtype ID</th>
          <th scope="col">Rate</th>
          <th scope="col">Limit</th>
          <th scope="col">Quantity</th>
          <th scope="col">Amount</th>
        </tr>
      </thead>
      <tbody>
        { fees.map(fee => Fee(fee, isUplifted, handlePlus, handleMinus, handleChange)) }
      </tbody>
    </table>
  );
}

FeeTable.propTypes = {
  fees: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    code: PropTypes.string,
    prices: PropTypes.arrayOf(PropTypes.object),
    amount: PropTypes.shape({
      sum: PropTypes.number.isRequired,
      attribute: PropTypes.object
    })
  })),
  isUplifted: PropTypes.bool,
  handleChange: PropTypes.func,
  handlePlus: PropTypes.func,
  handleMinus: PropTypes.func
}

export default FeeTable
