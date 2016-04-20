import React from 'react'
import { connect } from 'react-redux'
import { fetchPhrase } from '../actions'

let Sampler = ({ text, onClick, modelName }) => {
  return (
          <div className="sampler">
          <h2> { modelName } </h2>
              <button onClick={onClick} className='btn'>
                Generate a sentence
              </button>
              <p>
                {text}
              </p>
          </div>
        )
}

const mapStateToProps = (state, ownProps) => {
  return {
    text: state.text,
    modelName: state.modelName
  }
}

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    onClick: () => {dispatch(fetchPhrase())}
    }
}

Sampler = connect(mapStateToProps, mapDispatchToProps)(Sampler)

export default Sampler
