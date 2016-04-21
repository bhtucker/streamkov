
export const CHAINS_URL = '/chains/'
export const PHRASE_URL = '/draw/'
export const BLEND_URL = '/blend/'
export const READ_URL = '/read/'
export const SAVE_URL = '/persist/'


export const INITIAL_STATE = {
  isFetching: false,
  didInvalidate: false,
  chains: [],
  text: 'Initial text',
  modelName: 'Initial Model',
  inputValue: 'http://',
  saveText: ''
}
//export default config