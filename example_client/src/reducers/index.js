import { combineReducers } from 'redux';

function scenarios(state = [], action) {
  switch(action.type) {
    case 'FETCH_SCENARIOS_SUCCEEDED':
      return action.scenarios;
    default:
      return state;
  }
}


function advocateTypes(state = [], action) {
  switch(action.type) {
    case 'FETCH_ADVOCATE_TYPES_SUCCEEDED':
      return action.advocateTypes;
    default:
      return state;
  }
}


function offenceClasses(state = [], action) {
  switch(action.type) {
    case 'FETCH_OFFENCE_CLASSES_SUCCEEDED':
      return action.offenceClasses;
    default:
      return state;
  }
}


function prices(state = [], action) {
  switch(action.type) {
    case 'FETCH_PRICES_SUCCEEDED':
      return action.prices;
    default:
      return state;
  }
}


export const selectedAdvocateTypeId = (state = '', action) => {
  switch (action.type) {
    case 'SET_ADVOCATE_TYPE':
      return action.advocateTypeId;
    default:
      return state;
  }
}

export const selectedOffenceClassId = (state = '', action) => {
  switch (action.type) {
    case 'SET_OFFENCE_CLASS':
      return action.offenceClassId;
    default:
      return state;
  }
}

export const selectedScenarioId = (state = '', action) => {
  switch (action.type) {
    case 'SET_SCENARIO':
      return action.scenarioId;
    default:
      return state;
  }
}

const feeIdToQty = (state = new Map(), action) => {
  let qty;
  let newState;
  switch (action.type) {
    case 'SET_QTY':
      newState = new Map(state);
      newState.set(action.id, action.qty);
      return newState;
    case 'INC_QTY':
      newState = new Map(state);
      qty = state.get(action.id) || 0;
      newState.set(action.id, ++qty);
      return newState;
    case 'DEC_QTY':
      newState = new Map(state);
      qty = state.get(action.id) || 0;
      qty = qty > 0 ? --qty : 0;
      newState.set(action.id, qty);
      return newState;
    default:
      return state;
  }
}

const reducer = combineReducers({
  scenarios,
  advocateTypes,
  offenceClasses,
  prices,
  feeIdToQty,
  selectedScenarioId,
  selectedAdvocateTypeId,
  selectedOffenceClassId
});


export default reducer;
