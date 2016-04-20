import React from 'react'
import { render } from 'react-dom'
import configureStore from './configureStore'
import { Provider } from 'react-redux'
import App from './components/App'
import { fetchChains, initChains, dummyObj } from './actions'
import { INITIAL_STATE } from './config'

console.log('Fetchchains' + fetchChains)
const store = configureStore(INITIAL_STATE)

console.log(store);
console.log(store.getState());

console.log(initChains);

store.dispatch(initChains);

store.dispatch(fetchChains());

const rootElement = document.getElementById('content')
render(
  <Provider store={store}>
    <App />
  </Provider>,
  rootElement
)

