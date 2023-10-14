import React from "react";
import Card from "react-bootstrap/Card";
import "../App.css";
import { urlColors, camelCaseStringToTitleCase } from "../helper";

function UrlCard({ urlStats, loading }) {
  return (
    <div className="card-container">
      {urlStats?.map((el, idx) => (
        <Card
          style={{
            width: "12.5rem",
            textAlign: "right",
            height: "120px",
            fontFamily: "Poppins",
            fontWeight: "bold",
            color: "#6B6B6B",
          }}
          key={idx}
        >
          <Card.Header
            style={{
              backgroundColor: "white",
              borderBottom: "None",
              fontSize: ".8rem",
            }}
          >
            {camelCaseStringToTitleCase(el.name)}
          </Card.Header>
          <div className="card-figure">{el.figures.toLocaleString()} </div>
          <span
            className="card-bar"
            style={{ backgroundColor: `${urlColors[idx]}` }}
          ></span>
        </Card>
      ))}
    </div>
  );
}

export default UrlCard;
