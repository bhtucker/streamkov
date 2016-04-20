// Actions
import fetch from 'isomorphic-fetch'
import { CHAINS_URL as chainsUrl, PHRASE_URL as phraseUrl, BLEND_URL as blendUrl} from './config'
/*
 * action types
 */

export const INITIALIZE = 'INITIALIZE'
export const TOGGLE_CHAIN = 'TOGGLE_CHAIN'
export const RECEIVE_CHAINS = 'RECEIVE_CHAINS'
export const RECEIVE_PHRASE = 'RECEIVE_PHRASE'
export const RECEIVE_MODEL = 'BLEND_SELECTED'

export const initChains = {
    type: INITIALIZE
}

export const toggleChain = (id) => {
  return {
    type: TOGGLE_CHAIN,
    id
  }
}

export function fetchChains() {
  return function (dispatch) {
    return fetch(chainsUrl, {
        headers: {'Content-Type': 'application/json'}
        })
        .then(response => {
            let data = response.json()
            return data})
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
    return fetch(phraseUrl, {
        headers: {'Content-Type': 'application/json'}
        })
        .then(response => {
            let data = response.json()
            return data})
        .then(json => dispatch(receivePhrase(json)))
  }
};


function receivePhrase(data) {
  return {
    type: RECEIVE_PHRASE,
    text: data
  }
}


export function blendModel(chainIds) {
  return function (dispatch, getState) {
    let state = getState();
    let chainIds = state.chains
          .filter(chain => chain.chkbox)
          .map(chain => chain.id)
          .join(',');
    console.info(chainIds);
    let targetUrl = blendUrl + chainIds;
    return fetch(targetUrl, {
        headers: {'Content-Type': 'application/json'}
        })
        .then(response => {
            let data = response.json()
            return data})
        .then(json => dispatch(receiveModel(json)))
  }
};


function receiveModel(data) {
  return {
    type: RECEIVE_MODEL,
    modelName: data.map(datum => datum.name).join("_")
  }
}

export default fetchChains

//   // blendChains: function (argument) {
//   //   console.log('blendy');
//   //   console.log(this.state.data);
//   //   var chain_ids = this.state.data
//   //       .filter(function (chain) {return chain.chkbox})
//   //       .map(function (chain) {return chain.id});
//   //   console.log(chain_ids);
//   //   console.log(this.state.data);
//   //   var url = '/blend/' + chain_ids;
//   //   console.log(url);
//   //   $.ajax({
//   //     url: url,
//   //     dataType: 'json',
//   //     cache: false,
//   //     success: function(data) {
//   //       console.log('blended successfully!');
//   //     },
//   //     error: function(xhr, status, err) {
//   //       console.error(url, status, err.toString());
//   //     }
//   //   });
//   // },
