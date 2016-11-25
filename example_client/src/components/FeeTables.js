import React from 'react';
import FeeTable from './FeeTable';
import Total from './Total';

const FeeTables = ({
  basicFees,
  miscFees,
  isUplifted,
  handleChange,
  handlePlus,
  handleMinus
}) => (
  <div>
    {
      basicFees.length > 0 ?  <h3 className="heading-medium">Basic fees</h3> : null
    }
    <FeeTable
      fees={ basicFees }
      isUplifted={ isUplifted }
      handleChange={ handleChange }
      handlePlus={ handlePlus }
      handleMinus={ handleMinus }
    />
    {
      miscFees.length > 0 ?  <h3 className="heading-medium">Misc fees</h3> : null
    }
    <FeeTable
      fees={ miscFees }
      isUplifted={ isUplifted }
      handleChange={ handleChange }
      handlePlus={ handlePlus }
      handleMinus={ handleMinus }
    />
    <Total fees={ basicFees.concat(miscFees) } />
  </div>
);

export default FeeTables;
