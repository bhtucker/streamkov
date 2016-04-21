import React from 'react'
import Chain from './Chain'

const ChainList = ({ chains, onChainClick, blendChains }) => (
     <div className="chainList">
         <h1>Available models:</h1>
            {chains.map(chain =>
              <Chain
                  key={chain.id}
                  name={chain.name}
                  chkbox={chain.chkbox}
                  onUpdate={onChainClick.bind(null, chain.id)}
            />)}
       <button onClick={blendChains} className='btn'>
         Blend selected models into a metamodel
       </button>
     </div>
     )

export default ChainList
