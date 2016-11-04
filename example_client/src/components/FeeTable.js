import React, { PropTypes } from 'react';

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
          <tr key={ fee.id }>
            <td>{ fee.name }</td>
            <td>{ fee.code }</td>
            <td>{ fee.price !== undefined ? `\u00a3${ parseFloat(fee.price).toFixed(2) }` : '' }</td>
            <td className="quantity-td">
              <i className="fa fa-plus-circle" aria-hidden="true" onClick={ e => handlePlus(fee.id) }></i>
              <input type="number" className="quantity-input" value={ fee.qty } onChange={ e => handleChange(fee.id, e.target.value) }/>
              <i className="fa fa-minus-circle" aria-hidden="true" onClick={ e => handleMinus(fee.id) }></i>
            </td>
            <td>{ fee.amount !== 0 ? `\u00a3${ fee.amount.toFixed(2) }` : '' }</td>
          </tr>
        ))
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
