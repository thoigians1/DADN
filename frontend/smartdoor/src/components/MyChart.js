import React, { Component } from "react";
import Chart from "react-apexcharts";

class MyChart extends Component {
  constructor(props) {
    super(props);
    var times = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    this.state = {
      series: [{
        data: []
      }],
      options: {
        chart: {
          type: 'bar',
          height: 350
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
          }
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          categories: times,
        }
      },
    
    
    };
  }

  render() {
    return (
      <div className="app">
        <div className="row">
          <div className="mixed-chart">
            <Chart
              options={this.state.options}
              series={[{data: this.props.pp_per_hour}]}
              type="bar"
              height="400"
              width="800"
            />
          </div>
        </div>
      </div>
    );
  }
}

export default MyChart;