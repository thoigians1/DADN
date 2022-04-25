import React from 'react'
const Log = ({logs}) => {
    
    const item_count = 9
    const getTime = (a) => {
        const pattern = new RegExp("[0-9]{2}\:[0-9]{2}\:[0-9]{2}")
        return pattern.exec(a)
    }

  return (
    <div className='log_box'>
        <div className='logs'>
            {logs.slice(Math.max(0,logs.length - item_count), logs.length).map((log) => (
                <h3 key={log.id}>{getTime(log.time)}: số người {log.nop}</h3>
            ))}
        </div>
    </div>
  )
}

export default Log