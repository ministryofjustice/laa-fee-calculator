import React, { PropTypes } from 'react';

const Total = ({ fees }) => {
  if (fees.length === 0) {
    return null;
  }
  const total = fees
    .map(f => f['amount']).reduce(( pre, cur ) => pre + cur, 0);
  return (
    <div>
      <h3 className="heading-medium">Total</h3>
      <span className="total-fee">{ `\u00a3${parseFloat(total).toFixed(2)}` }</span>
    </div>
  );
}

Total.propTypes = {
  fees: PropTypes.array
}

export default Total;
