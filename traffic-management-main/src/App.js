import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  // State variables
  const [startLocation, setStartLocation] = useState('');
  const [endLocation, setEndLocation] = useState('');
  const [vehicleCount, setVehicleCount] = useState(0);
  const [delayTime, setDelayTime] = useState('N/A');
  const [optimizedRouteTime, setOptimizedRouteTime] = useState('N/A');
  const [vehicleData, setVehicleData] = useState([]);

  // Call the backend to fetch data when the component loads
  useEffect(() => {
    fetchApiData();
  }, []);

  // Fetch data from the /api route of Flask backend
  const fetchApiData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api');
      setVehicleData(response.data);
    } catch (error) {
      console.error("Error fetching data from backend", error);
    }
  };

  // Handle route optimization when user submits the form
  const handleRouteOptimization = async () => {
    try {
      const response = await axios.post('http://localhost:5000/traffic', {
        startLocation,
        endLocation,
      });
      const data = response.data;
      setVehicleCount(data.vehicleCount);
      setDelayTime(data.delay);
      setOptimizedRouteTime(data.optimizedRouteTime);
    } catch (error) {
      console.error('Error fetching data from backend', error);
    }
  };

  return (
    <div className="container">
      <h1>WayWise</h1>
      <p>Traffic Management System</p>

      {/* Inputs for route optimization */}
      <div className="inputs">
        <input
          type="text"
          placeholder="Start Location"
          value={startLocation}
          onChange={(e) => setStartLocation(e.target.value)}
        />
        <input
          type="text"
          placeholder="End Location"
          value={endLocation}
          onChange={(e) => setEndLocation(e.target.value)}
        />
        <button onClick={handleRouteOptimization}>Optimize Route</button>
      </div>

      {/* Display route optimization results */}
      <div className="results">
        <p>Vehicle Count: {vehicleCount}</p>
        <p>Delay Time: {delayTime}</p>
        <p>Optimized Route Time: {optimizedRouteTime} minutes</p>
      </div>

      {/* Display fetched data from Flask */}
      <div className="vehicle-data">
        <h2>Vehicle Data</h2>
        <ul>
          {vehicleData.map((data, index) => (
            <li key={index}>{data}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
