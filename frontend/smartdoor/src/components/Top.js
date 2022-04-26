import React from 'react'
import { useState, useEffect } from 'react'

const Top = ({current_pp}) => {
  const [buzzer_style, setBuzzerStyle] = useState('button-19')

  const fetchBuzzerStatus = async() => {
    const res = await fetch('http://127.0.0.1:8000/api/buzzer/status')
    const data = await res.json()
    return data
  }

  useEffect(() => {
    const getBuzzerStyle = async() => {
      const data = await fetchBuzzerStatus()
      const status = data.status
      if (status) 
        setBuzzerStyle('button-off')
      else 
        setBuzzerStyle('button-19')
    }

    setInterval(() => {
      getBuzzerStyle()
    }, 1000)
    
  },[])

  const buzzerOff = async() => {
    await fetch('http://127.0.0.1:8000/api/buzzer/off')
  }

  // const get_buzzer_style = () => {
  //   // if (buzzer_status)
  //   //   return 'button_off'
  //   // else
  //     return 'button_19'
  // }
  return (
    <div className='row1'>
      <div className='value_box'>
        <div style={{fontSize: "50px"}}>
          Số người trong phòng: 
        </div>
        <div className='value'>
          <h1>{current_pp}/5</h1>
        </div>
        
      </div>
      <div className='buzzer-box'>
        <div className='buzzer'>
          <button className={buzzer_style} onClick={() => buzzerOff()}>Buzzer</button>
          {/* <button className='reportbtn' onClick={() => showHidereport()}>Buzzer</button> */}
        </div>
      </div>
    </div>
  )
}

export default Top