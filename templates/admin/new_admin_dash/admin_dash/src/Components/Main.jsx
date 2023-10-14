import React from "react";
import ScoreBoard from "./ScoreBoard";
import TimelineChart from "./TimelineChart";
import Status from "./Status";
import UrlCard from "./UrlCard";
import Members from "./Members";

import "./../App.css";

// Custom Hook
import { useDashboardState } from "./Hooks/UseDashboardState";

function MainContent() {
  const [
    {
      state: {
        annotators,
        annotationStats,
        topAnnotators,
        urlStats,
        statsBreakdown,
        status,
      },
      loading,
      error,
    },
  ] = useDashboardState();

  if (loading) return <div className="spinner"> </div>;

  return (
    <>
      <UrlCard urlStats={urlStats} />
      <div className="container">
        <TimelineChart annotationStats={annotationStats} />
        <ScoreBoard
          topAnnotators={topAnnotators}
          statsBreakdown={statsBreakdown}
        />
      </div>
      <div className="status-annotators-container">
        <Status status={status} />
        <Members annotators={annotators} />
      </div>
    </>
  );
}

export default MainContent;
