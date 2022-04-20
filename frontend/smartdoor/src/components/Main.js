import React from 'react'
import Top from './Top.js'
import MyChart from './MyChart.js'
import Log from './Log'
import { useState, useEffect } from 'react'


const Main = ({fetch_log}) => {
  const [logs, setLogs] = useState([])
  const [headIdx, setHeadIdx] = useState(0)
  const [total_log, setTotalLog] = useState(0)
  const [current_pp, setCurrent_pp] = useState(0)

  useEffect(() => {
    const getLogs = async () => {
      const logFromServer = await fetch_log()
      const room_logs = logFromServer.room_logs
      setLogs(room_logs)
      setTotalLog(room_logs.length)
      setCurrent_pp(room_logs[room_logs.length - 1].nop)
      return room_logs
    }
    
    setInterval(() => {
      getLogs()
      
    }, 1000)
    
  }, []);

  const item_count = 9
  const moveUpDisabled = (headIdx - item_count === 0)
  const moveDownDisabled = ( headIdx >= total_log)
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

  const init_log = async() =>{
    const logFromServer = await fetch_log()
    const room_logs = logFromServer.room_logs
    setLogs(room_logs)
    setHeadIdx(room_logs.length)
    setTotalLog(room_logs.length)
    setCurrent_pp(room_logs[room_logs.length - 1].nop)
  }
  return (
    <div className='main'>
        <div className='data'>
          <Top current_pp={current_pp}/>
          <div className='chart_box'>
            <MyChart/>
          </div>
        </div>
        <div className='live_log'>
          <Log logs={logs} from_log={headIdx - item_count} to_log={headIdx} init_log={init_log} moveUp={moveUp} moveDown={moveDown} moveDownDisabled={moveDownDisabled}/>
        </div>
    </div>
  )
}

export default Main