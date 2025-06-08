import React, { useEffect, useState, useCallback } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "../styles/ResultPage.css";

function ResultPage() {
  const { user, isAuthenticated, isLoading } = useAuth0();
  const [status, setStatus] = useState("processing");
  const [matchDetails, setMatchDetails] = useState(null);

  const fetchMatchStatus = useCallback(async () => {
    if (!user) return;

    try {
      setStatus("processing");
      const auth0Id = user.sub;

      const userInfoRes = await fetch(`http://localhost:5000/get_user_details/${auth0Id}`);
      const userInfo = await userInfoRes.json();

      if (!userInfo.user_id || !userInfo.role) {
        setStatus("no-match");
        return;
      }

      const res = await fetch("http://localhost:5000/match", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ auth0Id, role: userInfo.role })
      });

      const data = await res.json();

      if (!res.ok) {
        console.error("Server returned an error:", data.error || "Unknown error");
        if (data.missing_features) console.error("Missing features:", data.missing_features);
        if (data.extra_features) console.error("Extra features:", data.extra_features);
        setStatus("no-match");
        return;
      }

      if (data.match_found === false) {
        setStatus("no-match");
      } else if (data.cid) {
        const ipfsRes = await fetch(`http://localhost:5000/ipfs/${data.cid}`);
        const matchData = await ipfsRes.json();
        setMatchDetails({ ...matchData, cid: data.cid });
        setStatus("match");
      } else {
        setStatus("processing");
      }
    } catch (err) {
      console.error("Error during match fetch:", err);
      setStatus("no-match");
    }
  }, [user]);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchMatchStatus();
    }, 3000);
    return () => clearTimeout(timer);
  }, [fetchMatchStatus]);

  const renderContent = () => {
    if (isLoading) return <p>Loading...</p>;
    if (!isAuthenticated) return <p>You need to log in to view your match results.</p>;

    if (status === "processing") {
      return <p>🔄 Matching is under process. Please wait...</p>;
    } else if (status === "match" && matchDetails) {
      return (
        <>
          <h2>✅ Match Found!</h2>
          <p><strong>Phone:</strong> {matchDetails.phone_number}</p>
          <p><strong>Organ Type:</strong> {matchDetails.organ_type}</p>
          <p><strong>Location:</strong> {matchDetails.location}</p>
          {matchDetails.cid && (
            <p>
              <strong>IPFS Record:</strong>{" "}
              <a
                href={`https://ipfs.io/ipfs/${matchDetails.cid}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                View on IPFS
              </a>
            </p>
          )}
        </>
      );
    } else {
      return (
        <>
          <h2>⚠️ No Matches Found</h2>
          <p>
            We understand the importance of time and how crucial it is. Currently, no matches have been found. Please check back later, or click the button below to try matching again.
          </p>
          <button className="try-again-button" onClick={fetchMatchStatus}>Try Again</button>
        </>
      );
    }
  };

  return (
    <div className="result-container">
      <div className="result-content slide-down">
        {renderContent()}
      </div>
    </div>
  );
}

export default ResultPage;
