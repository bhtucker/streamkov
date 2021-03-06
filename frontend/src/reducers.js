import { CHAINS_URL as chainsUrl, INITIAL_STATE } from './config'
import { INITIALIZE, TOGGLE_CHAIN, RECEIVE_PHRASE, RECEIVE_CHAINS, RECEIVE_MODEL, UPDATE_INPUT, NOTIFY_SAVE} from './actions'
import { combineReducers } from 'redux'

var chainData = [{"id": 1, "name": "hard", }, {"id": 2, "name": "coded"}];
function fetchChains (chainsUrl) {
  return chainData.map(
    datum => Object.assign(
        {}, datum, {chkbox: false})
  )
}

function toggleChain (chains, action) {
  return chains.map(chain => {
    if (chain.id == action.id) {
      return Object.assign({}, chain, {
        chkbox: !chain.chkbox
      })
    }
    return chain
  })
}

 
function reducer(state = INITIAL_STATE, action) {
  switch (action.type) {
    case INITIALIZE:
        // console.log('trying to init');
        // console.log('current chainsUrl: ' + chainsUrl);
        return Object.assign({}, state, {chains: fetchChains(chainsUrl)})
    case TOGGLE_CHAIN:
        // console.log('trying to toggle');
        // console.log('current action: ' + action);
        return Object.assign(
          {}, state, {chains: toggleChain(state.chains, action)}
        )
    case RECEIVE_PHRASE:
      return Object.assign({}, state, {
        isFetching: false,
        text: action.text,
        textLastUpdated: action.receivedAt
      })
    case RECEIVE_CHAINS:
      return Object.assign({}, state, {
        isFetching: false,
        chains: action.chains,
        chainsLastUpdated: action.receivedAt
      })    
    case RECEIVE_MODEL:
      // if the model is not 'blended', uncheck everything
      let chains;
      if (action.blended) {
        chains = state.chains;
      } else {
        chains = state.chains.map(
          chain => Object.assign({}, chain, {chkbox: false})
        );
      }
      return Object.assign({}, state, {
        modelName: action.modelName,
        chains
      })
    case NOTIFY_SAVE:
      return Object.assign({}, state, {
        saveText: action.value,
      })
    case UPDATE_INPUT:
      return Object.assign({}, state, {
        inputValue: action.inputValue
      })
    default:
      return state
  }
}

export const rootReducer = reducer

export default rootReducer
