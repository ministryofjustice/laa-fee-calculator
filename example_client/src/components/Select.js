import React, { PropTypes } from 'react';

const Select = ({ id, items, label, selected, handleChange }) => (
  <div className="form-group">
    <label className="form-label" htmlFor={ id }>
      { label }
    </label>
    <select className="form-control" id={ id } value={ selected } onChange={ handleChange }>
      <option value="" key=""></option>
      { items.map(item => (
          <option id={ item.id } value={ item.id } key={ item.id }>
            { item.name }
          </option>
        ))
      }
    </select>
  </div>
)

Select.propTypes = {
  id: PropTypes.string,
  items: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    name: PropTypes.string
  })),
  label: PropTypes.string,
  selected: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number
  ]),
  handleChange: PropTypes.func
}

export default Select
