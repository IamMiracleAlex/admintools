import React from "react";
import Table from "react-bootstrap/Table";
import { FiCheckSquare, FiXSquare } from "react-icons/fi";

import "../App.css";

function Status({ status }) {
  const statusSummary = status?.slice(0, 7);

  const statusTable = statusSummary?.map((el, key) => {
    return (
      <tr className="status-table-row">
        <td>{el.Id ? el.Id.replace(/\_/g, " ").toUpperCase() : " N/A "}</td>
        <td>
          {el.data ? new Date(el.data[0].timestamp).toLocaleString() : "N/A"}
        </td>
        <td>
          {el.data[0].values === 0 ? (
            <FiCheckSquare style={{ color: "green" }} />
          ) : (
            <FiXSquare style={{ color: "#FFA500" }} />
          )}
        </td>
      </tr>
    );
  });

  return (
    <div className="status-container">
      <div className="status-top"> Status Page </div>
      <div className="status">
        <Table bordered hover>
          <thead>
            <tr>
              <th>Tables</th>
              <th>Timestamp</th>
              <th>State</th>
            </tr>
          </thead>
          <tbody>{statusTable}</tbody>
        </Table>
      </div>
      <button className="styled-button">
        <a href="https://admin.centricity.cloud/admintool/status/">
          View all Status
        </a>
      </button>
    </div>
  );
}

export default Status;
