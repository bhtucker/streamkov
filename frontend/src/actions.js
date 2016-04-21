// Actions
import fetch from 'isomorphic-fetch'
import { CHAINS_URL as chainsUrl,
         PHRASE_URL as phraseUrl, 
         BLEND_URL as blendUrl,
         READ_URL as readUrl,
         SAVE_URL as saveUrl} from './config'
/*
 * action types
 */

export const INITIALIZE = 'INITIALIZE'
export const TOGGLE_CHAIN = 'TOGGLE_CHAIN'
export const RECEIVE_CHAINS = 'RECEIVE_CHAINS'
export const RECEIVE_PHRASE = 'RECEIVE_PHRASE'
export const RECEIVE_MODEL = 'BLEND_SELECTED'
export const CREATE_MODEL = 'CREATE_MODEL'
export const UPDATE_INPUT = 'UPDATE_INPUT'
export const NOTIFY_SAVE = 'NOTIFY_SAVE'

export const initChains = {
    type: INITIALIZE
}

export const toggleChain = (id) => {
  return {
    type: TOGGLE_CHAIN,
    id
  }
}

function fetchAndPromiseData(targetUrl) {
  return fetch(targetUrl, {
        headers: {'Content-Type': 'application/json'}
        })
        .then(response => {
            let data = response.json()
            return data})
  }

export function fetchChains() {
  return function (dispatch) {
    return fetchAndPromiseData(chainsUrl)
      .then(json => dispatch(receiveChains(json)))
  }
};


function receiveChains(data) {
  return {
    type: RECEIVE_CHAINS,
    chains: data.map(
        datum => Object.assign(
            {}, datum, {chkbox: false})
        ),
    receivedAt: Date.now()
  }
}


export function fetchPhrase() {
  return function (dispatch) {
    return fetchAndPromiseData(phraseUrl)
        .then(json => dispatch(receivePhrase(json)))
  }
};


function receivePhrase(data) {
  return {
    type: RECEIVE_PHRASE,
    text: data
  }
}


export function blendModel() {
  return function (dispatch, getState) {
    let state = getState();
    let chainIds = state.chains
          .filter(chain => chain.chkbox)
          .map(chain => chain.id)
          .join(',');
    console.info(chainIds);
    let targetUrl = blendUrl + chainIds;
    return fetchAndPromiseData(targetUrl)
        .then(data => dispatch(receiveModel(
          data.map(datum => datum.name).join("_"), true
        )))
    }
};

export function createModel(textUrl) {
  return function (dispatch, getState) {
    let state = getState();
    let textUrl = escape(state.inputValue).split('/').join('%2F')
    let targetUrl = readUrl + textUrl
    return fetchAndPromiseData(targetUrl)
      .then(data => dispatch(receiveModel(data.modelName, false)))
    }
};

function receiveModel(modelName, blended) {
  return {
    type: RECEIVE_MODEL,
    modelName,
    blended
  }
}

export function updateReadInput(value) {
  return {
    type: UPDATE_INPUT,
    inputValue: value.trim()
  }
}

export function saveModel() {
  return function (dispatch, getState) {
    let state = getState();
    let targetUrl = saveUrl + state.modelName
    return fetchAndPromiseData(targetUrl)
      .then(data => {
        dispatch(receiveModel(data.modelName, false));
        dispatch(notifySaved('Saved ' + data.modelName));
        dispatch(fetchChains());
      })
    }
};


export function notifySaved(value) {
  return {
    type: NOTIFY_SAVE,
    value
  }
}