import 'babel-polyfill';
import React from 'react';
import { render } from 'react-dom';
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import createSagaMiddleware from 'redux-saga'

import App from './components/App';
import reducer from './reducers';
import root from './sagas';

const apiBaseURL = process.env.REACT_APP_API_URL
  || `http://${window.location.hostname}:8000/api/v1`;

const sagaMiddleware = createSagaMiddleware()
const store = createStore(reducer, applyMiddleware(sagaMiddleware));

sagaMiddleware.run(() => root(apiBaseURL));

render(
  <Provider store={ store }>
    <App />
  </Provider>,
  document.getElementById('root')
);
