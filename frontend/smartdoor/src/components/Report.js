import React from 'react'
import Table from 'react-bootstrap/Table'
import { useState } from 'react'

const Report = ({report}) => {

    const headtr = {
        borderBottom: "solid 2px black"
    }

    const each_td = {
        lineHeight: 2,
        textTransform: 'capitalize'
    }

    const getDate = (a) => {
        const datePattern = new RegExp("[0-9]+ [a-zA-Z]+ [0-9]{4}")
        console.log(datePattern.exec(a))
        return datePattern.exec(a)
    }

    const displayReport = (report) => report.
                            map( (day) => { 
                                return (
                                        <tr key={day.date}>
                                            <td style={each_td}> {day.weekday} </td>
                                            <td style={each_td}> {getDate(day.date)} </td>
                                            <td style={each_td}> {day.avg_nop} </td>
                                            <td style={each_td}> {day.alert} </td>
                                        </tr>
                                );
                            });
    
  return (
    <div>
        <Table bordered style={{width: 800, margin:'0 auto', textAlign: 'center', borderCollapse: "collapse"}} responsive >
            <thead>
                <tr style={headtr}>
                    <th >Day</th>
                    <th>Date</th>
                    <th>Average nop</th>
                    <th>Buzzer alert</th>
                </tr>
            </thead>
            <tbody>
                {displayReport(report)}
            </tbody>
        </Table>
    </div>
  )
}

export default Report