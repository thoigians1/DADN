import React from 'react'
import Top from './Top.js'
import MyChart from './MyChart.js'
import Log from './Log'

const Main = () => {
  return (
    <div className='main'>
        <div className='data'>
          <Top/>
          <div className='chart_box'>
            <MyChart/>
          </div>
        </div>
        <div className='live_log'>
          <Log/>
        </div>
    </div>
  )
}

export default Main