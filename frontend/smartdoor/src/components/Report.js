import React from 'react'
import Table from 'react-bootstrap/Table'
import { useState } from 'react'

const Report = () => {

    const headtr = {
        borderBottom: "solid 2px black"
    }

    const each_td = {
        lineHeight: 2,
    }

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

    const displayReport = (report) => report.
                            map( (day) => { 
                                return (
                                        <tr>
                                            <td style={each_td}> {day.weekday} </td>
                                            <td style={each_td}> {day.date} </td>
                                            <td style={each_td}> {day.avg_nop} </td>
                                            <td style={each_td}> {day.alert} </td>
                                        </tr>
                                );
                            });
    const displayLastReport = async () => {
        const list_report = await fetch_report_list()
        const lst_len = list_report.reports.length
        const last_report_id = list_report.reports[lst_len - 1].id
        const last_report = await fetch_report_id(last_report_id)
        // console.log(last_report.weekday_report)
        return displayReport(last_report.weekday_report)
    }
  return (
    <div>
        <Table bordered style={{width:1100, margin:'0 auto', textAlign: 'center', borderCollapse: "collapse"}} responsive >
            <thead>
                <tr style={headtr}>
                    <th >Day</th>
                    <th>Date</th>
                    <th>Average nop</th>
                    <th>Buzzer alert</th>
                </tr>
            </thead>
            <tbody>
                {()=>displayLastReport()}
            </tbody>
        </Table>
    </div>
  )
}

export default Report