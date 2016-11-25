import React, { Component } from 'react';

class RadioWithLabel extends Component {
  constructor(props) {
    super(props);
    this.state = { focused : false };
  }

  render() {
    let className = 'block-label';
    if (this.props.selected) {
      className += ' selected';
    };
    if(this.state.focused) {
      className += ' focused';
    }
    return (
      <label className={ className } htmlFor={ this.props.id }>
        <input
          id={ this.props.id }
          type="radio"
          value={ this.props.value }
          checked={ this.props.selected }
          onChange={ this.props.handleChange }
          onFocus={ () => this.setState({ focused: true }) }
          onBlur={ () => this.setState({ focused: false }) }
        />
        { this.props.label }
      </label>
    );
  }
}

RadioWithLabel.propTypes = {
  id: React.PropTypes.string.isRequired,
  value: React.PropTypes.string.isRequired,
  selected: React.PropTypes.bool.isRequired,
  handleChange: React.PropTypes.func.isRequired
}


export default RadioWithLabel;
