import { call, put, fork, take, select } from 'redux-saga/effects'

export function fetchEndPoint(url) {
  return fetch(url)
      .then(rsp => rsp.json())
      .then(data => data['results']);
}

export function* fetchScenarios(baseURL) {
  const scenarios = yield call(fetchEndPoint, baseURL + '/scenarios');
  yield put({type: 'FETCH_SCENARIOS_SUCCEEDED', scenarios});
}

export function* fetchAdvocateTypes(baseURL) {
  const advocateTypes = yield call(fetchEndPoint, baseURL + '/advocate-types');
  yield put({type: 'FETCH_ADVOCATE_TYPES_SUCCEEDED', advocateTypes});
}

export function* fetchOffenceClasses(baseURL) {
  const offenceClasses = yield call(fetchEndPoint, baseURL + '/offence-classes');
  yield put({type: 'FETCH_OFFENCE_CLASSES_SUCCEEDED', offenceClasses});
}

export function* fetchPrices(baseURL) {
  let prevSenarioId;
  let prevAdvocateTypeId;
  let prevOffenceClassId;
  while(true) {
    yield take(['SET_SCENARIO', 'SET_ADVOCATE_TYPE', 'SET_OFFENCE_CLASS']);
    const scenarioId = yield select(state => state.selectedScenarioId);
    const advocateTypeId = yield select(state => state.selectedAdvocateTypeId);
    const offenceClassId = yield select(state => state.selectedOffenceClassId);
    const allSet = scenarioId && advocateTypeId && offenceClassId;
    const anyUpdated = scenarioId !== prevSenarioId
      || advocateTypeId !== prevAdvocateTypeId
      || offenceClassId !== prevOffenceClassId;
    if (allSet && anyUpdated) {
      const url = `${baseURL}/prices?scenario_id=${scenarioId}&advocate_type_id=${advocateTypeId}&offence_class_id=${offenceClassId}`;
      const prices = yield call(fetchEndPoint, url);
      yield put({type: 'FETCH_PRICES_SUCCEEDED', prices});
    }
    prevSenarioId = scenarioId;
    prevAdvocateTypeId = advocateTypeId;
    prevOffenceClassId = offenceClassId;
  }
}


export default function* root(baseURL) {
  yield fork(fetchScenarios, baseURL);
  yield fork(fetchAdvocateTypes, baseURL);
  yield fork(fetchOffenceClasses, baseURL);
  yield fork(fetchPrices, baseURL);
}
