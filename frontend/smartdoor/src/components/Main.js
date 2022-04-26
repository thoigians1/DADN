import React from 'react'
import Top from './Top.js'
import MyChart from './MyChart.js'
import Log from './Log'
import { useState, useEffect } from 'react'
import Report from './Report.js'


const Main = ({fetch_log}) => {
  const [logs, setLogs] = useState([])
  // const [headIdx, setHeadIdx] = useState(0)
  const [total_log, setTotalLog] = useState(0)
  const [current_pp, setCurrent_pp] = useState(0)
  const [pp_per_hour, setPpPerHour] = useState([])
  const [showReport, setShowReport] = useState(false)

  const [report, setReport] = useState([])
  const fetch_report_list = async() => {
      const res = await fetch('http://127.0.0.1:8000/api/report/week')
      const data = await res.json()
      return data
  }

  const fetch_report_id = async(id) => {
      const res = await fetch('http://127.0.0.1:8000/api/report/week/' + id)
      const data = await res.json()
      return data
  }

  const displayLastReport = async () => {
    const list_report = await fetch_report_list()
    const lst_len = list_report.reports.length
    const last_report_id = list_report.reports[lst_len - 1].id
    const last_report = await fetch_report_id(last_report_id)
    setReport(last_report.weekday_report)
    setShowReport(()=> !showReport)
  }
  

  useEffect(() => {
    const getLogs = async () => {
      const logFromServer = await fetch_log()
      const room_logs = logFromServer.room_logs
      setLogs(room_logs)
      setTotalLog(room_logs.length)
      setCurrent_pp(room_logs[room_logs.length - 1].nop)
      setPpPerHour(getPpPerHour(room_logs))
      return room_logs
    }
    
    setInterval(() => {
      getLogs()
      
    }, 1000)
    
  }, []);

  const getPpPerHour = (roomLog) => {
    var lst = Array(24).fill(0);
    for (let i = 0; i < roomLog.length; i++){
      const pattern = new RegExp("[0-9]{2}\:[0-9]{2}\:[0-9]{2}")
      const time = pattern.exec(roomLog[i].time).toString()
      const hour = parseInt(time.slice(0,2))
      lst[hour] = roomLog[i].nop;
    }
    return lst
  }

  // const item_count = 9
  // const moveUpDisabled = (headIdx - item_count <= 0)
  // const moveDownDisabled = ( headIdx >= total_log)
  // const moveUp = () => {
  //   if (moveUpDisabled)
  //     return;
  //   setHeadIdx((curHead) => curHead-1)
  // }
  // const moveDown = () => {
  //   if (moveDownDisabled)
  //     return;
  //   setHeadIdx((curHead) => curHead+1)
  // }

  // const init_log = async() =>{
  //   const logFromServer = await fetch_log()
  //   const room_logs = logFromServer.room_logs
  //   setLogs(room_logs)
  //   setHeadIdx(room_logs.length)
  //   setTotalLog(room_logs.length)
  //   setCurrent_pp(room_logs[room_logs.length - 1].nop)
  //   setPpPerHour(getPpPerHour(room_logs))
  // }
  return (
    <div className='main'>
        <div className='data'>
          <Top current_pp={current_pp} displayLastReport={displayLastReport} showReport={showReport}/>
          <div className='chart_box'>
            {showReport ? (<Report report={report}/>) :(<MyChart pp_per_hour={pp_per_hour}/>)}
          </div>
        </div>
        <div className='live_log'>
          <Log 
            logs={logs} 
            // from_log={headIdx - item_count} 
            // to_log={headIdx} 
            // init_log={init_log} 
            // moveUp={moveUp} 
            // moveDown={moveDown} 
            // moveDownDisabled={moveDownDisabled}
          />
        </div>
    </div>
  )
}

export default Main