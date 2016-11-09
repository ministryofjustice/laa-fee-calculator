import React, { PropTypes } from 'react';

const Fee = ({ id, name, code, price, qty, amount, maxCount, handlePlus, handleMinus, handleChange }) => {
  const exceedMax = maxCount !== null ? qty > maxCount : false;
  const qtyClassName = exceedMax ? "quantity-input error" : "quantity-input";
  return (
    <tr key={ id }>
      <td>{ name }</td>
      <td>{ code }</td>
      <td>{ price !== undefined ? `\u00a3${ parseFloat(price).toFixed(2) }` : '' }</td>
      <td className="quantity-td">
        <i className="fa fa-plus-circle" aria-hidden="true" onClick={ e => handlePlus(id) }></i>
        <input type="number" className={ qtyClassName } value={ qty } onChange={ e => handleChange(id, e.target.value) }/>
        <i className="fa fa-minus-circle" aria-hidden="true" onClick={ e => handleMinus(id) }></i>
        { exceedMax ? (<p className="error-message">{`max ${maxCount}`}</p>) : null }
      </td>
      <td>{ amount !== 0 ? `\u00a3${ amount.toFixed(2) }` : '' }</td>
    </tr>
  );
}

const FeeTable = ({ fees, handleChange, handlePlus, handleMinus }) => {
  if (fees.length === 0) {
    return null;
  }
  return (
    <table>
      <thead>
        <tr>
          <th scope="col">Fee type</th>
          <th scope="col">Code</th>
          <th scope="col">Rate</th>
          <th scope="col">Quantity</th>
          <th scope="col">Amount</th>
        </tr>
      </thead>
      <tbody>
      { fees.map(fee => (
        <Fee key={ fee.id } { ...fee }
          handleChange={ handleChange }
          handlePlus={ handlePlus }
          handleMinus={ handleMinus }
        />))
      }
      </tbody>
    </table>
  );
}

FeeTable.propTypes = {
  fees: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    code: PropTypes.string,
    price: PropTypes.number,
    amount: PropTypes.number.isRequired
  })),
  handleChange: PropTypes.func,
  handlePlus: PropTypes.func,
  handleMinus: PropTypes.func
}

export default FeeTable
