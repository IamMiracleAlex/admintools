import React from "react";
import "../App.css";

function Members({ annotators, loading }) {

  const cleanData = annotators.filter((user) => 
  user.first_name &&  user.last_name
  )

  return (
    <div className="member-container">
      <div className="member-top"> Annotators </div>
      <div className="members-grid">
        {cleanData?.map((el, idx) => (
          <div key={idx}>
            <div className="avatar-placeholder">
              {`${el.first_name[0].toUpperCase()}${el.last_name[0].toUpperCase()}`}
            </div>
            <div
              style={{
                textAlign: "center",
                color: "#434343",
                fontSize: ".8rem",
              }}
            >
              {`${el.first_name.replace(
                /^./,
                el.first_name[0].toUpperCase()
              )} ${el.last_name.replace(/^./, el.last_name[0].toUpperCase())}`}
            </div>
          </div>
        ))}
      </div>
      <div className="members-bottom"></div>
      <button className="styled-button">
        <a href="https://admin.centricity.cloud/users/user/"> View all Users</a>
      </button>
    </div>
  );
}

export default Members;
