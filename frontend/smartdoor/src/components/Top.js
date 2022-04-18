import React from 'react'

const Top = () => {
  return (
    <div className='row1'>
      <div className='value_box'>
        <div style={{fontSize: "50px", marginRight: "30px"}}>
          Số người trong phòng: 
        </div>
        <div className='value'>
          <h1>5/5</h1>
        </div>
        
      </div>
      <div className='buzzer'>
        <button className='button-19'>Buzzer</button>
      </div>
    </div>
  )
}

export default Top