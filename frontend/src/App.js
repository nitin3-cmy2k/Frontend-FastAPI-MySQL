import React, { useEffect, useState } from 'react';

function App() {
  const [dbData, setDbData] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState("Connecting to backend...");

  // !!! CONFIGURATION POINT !!!
  // Replace with the specific VirtualBox VM Network IP hosting your Kubernetes Cluster
  const BACKEND_API_URL = "http://<YOUR_KUBERNETES_VM_IP>:30090/api/data";

  useEffect(() => {
    fetch(BACKEND_API_URL)
      .then(response => response.json())
      .then(resObj => {
        if (resObj.status === "success") {
          setDbData(resObj.data);
          setConnectionStatus("Successfully connected to MySQL database via FastAPI!");
        } else {
          setConnectionStatus("Backend API returned error: " + resObj.message);
        }
      })
      .catch(err => {
        setConnectionStatus("Failed to communicate with Backend API layer. Verify connection endpoint details.");
        console.error(err);
      });
  }, []);

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif', backgroundColor: '#f4f6f9', minHeight: '100vh' }}>
      <h2>Kubernetes Stack UI Console</h2>
      <div style={{ padding: '15px', background: '#fff', borderRadius: '5px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <h4>Network Status Pipeline Tracker:</h4>
        <p style={{ color: dbData.length > 0 ? 'green' : 'orange', fontWeight: 'bold' }}>{connectionStatus}</p>
      </div>
      
      <h3>Database Record Output Log:</h3>
      <ul>
        {dbData.map(item => (
          <li key={item.id}><strong>ID:</strong> {item.id} | <strong>User Registry Entity:</strong> {item.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

