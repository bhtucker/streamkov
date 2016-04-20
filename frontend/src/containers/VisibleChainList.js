import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import { toggleChain, blendModel } from '../actions'
import ChainList from '../components/ChainList'

const mapStateToProps = (state, ownProps) => {
  return {
    chains: state.chains
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return bindActionCreators({
    onChainClick: toggleChain,
    blendChains: blendModel
    }, dispatch)
}

const VisibleChainList = connect(
  mapStateToProps,
  mapDispatchToProps
)(ChainList)

export default VisibleChainList
