export const setScenario = (scenarioId) => ({
  type: 'SET_SCENARIO',
  scenarioId
})

export const setAdvocateType = (advocateTypeId) => ({
  type: 'SET_ADVOCATE_TYPE',
  advocateTypeId
})

export const setOffenceClass = (offenceClassId) => ({
  type: 'SET_OFFENCE_CLASS',
  offenceClassId
})

export const setQuantity = (id, qty) => ({
  type: 'SET_QTY',
  id,
  qty
})

export const incQuantity = (id) => ({
  type: 'INC_QTY',
  id
})

export const decQuantity = (id) => ({
  type: 'DEC_QTY',
  id
})

export const setUplift = (isUplifted) => ({
  type: 'SET_UPLIFT',
  isUplifted
})
