import React from 'react'
const Log = ({logs, from_log, to_log, init_log, moveUp, moveDown, moveDownDisabled}) => {
    

    const getTime = (a) => {
        const pattern = new RegExp("[0-9]{2}\:[0-9]{2}\:[0-9]{2}")
        return pattern.exec(a)
    }

  return (
    <div className='log_box'>
        <div className='logs'>
            {logs.slice(from_log, to_log).map((log) => (
                <h3 key={log.id}>{getTime(log.time)}: số người {log.nop}</h3>
            ))}
        </div>
        <div className='controlbtn'>
            <div className='btn_box'>
                <button className='btn' onClick={() => init_log()}>To Newest</button>
                <button className='btn' onClick={moveUp}>Up</button>
                <button className='btn' onClick={moveDown}>Down</button>
            </div>
            {moveDownDisabled ? null : (
                <div className='new_log_noti'> You have a new log </div>
            ) }
        </div>
        
    </div>
  )
}

export default Log