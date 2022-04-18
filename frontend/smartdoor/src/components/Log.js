import React from 'react'
import { useState, useEffect } from 'react'
const Log = () => {
    const [logs, setLogs] = useState([
        'log1',
        'log2',
        'log3',
        'log4',
        'log5',
        'log6',
        'log7',
        'log8',
        'log9',
        'log10',
        'log11',
        'log12',
        'log13',
    ])
    const fetch_log = () => {
        setLogs((oldlogs) => [...oldlogs, 'logA'] )
    }
    
    const total_log = logs.length
    const item_count = 9
    const [headIdx, setHeadIdx] = useState(total_log)
    const moveUpDisabled = (headIdx - item_count === 0)
    const moveDownDisabled = ( headIdx === total_log)
    const moveUp = () => {
        if (moveUpDisabled)
          return;
        setHeadIdx((curHead) => curHead-1)
      }
      const moveDown = () => {
        if (moveDownDisabled)
          return;
        setHeadIdx((curHead) => curHead+1)
      }

    useEffect(() => {
        setInterval(() => {
            fetch_log();
        }, 1000)
    }, []);

  return (
    <div className='log_box'>
        <div className='logs'>
            {logs.slice(headIdx - item_count,headIdx).map((log) => (
                <h3>{log}</h3>
            ))}
        </div>
        <div className='controlbtn'>
            <div className='btn_box'>
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