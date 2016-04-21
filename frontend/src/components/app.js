import React from 'react'
import VisibleChainList from '../containers/VisibleChainList'
import Sampler from './Sampler'
import UrlEntryBox from './UrlEntryBox'

const App = () => (
  <div>
    <h1>Streamkov</h1>
    <VisibleChainList />
    <Sampler />
    <UrlEntryBox />
  </div>
)

export default App
