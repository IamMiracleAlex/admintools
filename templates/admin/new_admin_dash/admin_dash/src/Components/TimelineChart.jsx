import React from "react";
import Chart from "react-apexcharts";

import "../App.css";

function TimelineChart({
  annotationStats: { annotated_figures, categories },
  loading,
}) {
  const graghData = {
    series: [
      {
        name: "Annotated",
        data: annotated_figures,
      },
    ],
    options: {
      chart: {
        height: 300,
        type: "area",
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "smooth",
      },
      xaxis: {
        type: "week",
        categories: categories,
      },
      tooltip: {
        x: {
          format: "dd/MM/yy HH:mm",
        },
      },
    },
  };

  return (
    <div className="graph-container">
      <div className="graph-top">
        Annotation Stats
        {/* <div className="graph-top-month">
            <Form.Control
              style={{ fontSize: "12px" }}
              as="select"
              onChange={(e) => console.log(e)}
            >
              <option value="" disabled selected>
                Month
              </option>
              <option value="Jan"> Jan </option>;
              <option value="Feb"> Feb </option>;
              <option value="March"> March </option>;
            </Form.Control>
          </div> */}
      </div>
      <div className="timeline-chart">
        {annotated_figures && categories ? (
          <Chart
            options={graghData.options}
            series={graghData.series}
            type="area"
            width="100%"
            height="300px"
          />
        ) : (
          <div className="spinner"> </div>
        )}
      </div>
    </div>
  );
}

export default TimelineChart;
