import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import ProgressBar from "react-bootstrap/ProgressBar";
import "../App.css";

import { formatMetricString } from "../helper";

function ScoreBoard({ statsBreakdown }) {
  statsBreakdown?.forEach(
    (el) => (
      (el.metric = formatMetricString(el.metric)),
      (el.count = el.count.toLocaleString())
    )
  );

  const stat = statsBreakdown?.map((stat, key) => {
    return (
      <>
        <div className="progress-content">
          <div className="progress-content-child" key={key}>
            {stat.metric}
          </div>
          <div> {stat.count} </div>
        </div>
        <ProgressBar variant="success" animated now={100} />
      </>
    );
  });

  return (
    <>
      <div className="progress-bar-container">
        <div className="progress-bar-top"> Annotation Scoreboard </div>
        <div className="bar">{stat}</div>
        <button className="styled-button">
          <a href="https://admin.centricity.cloud/annotation/annotationstats/">
            View Breakdown
          </a>
        </button>
      </div>
    </>
  );
}

export default ScoreBoard;
