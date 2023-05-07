import React, { useState, useEffect } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, BarChart, Bar, CartesianGrid } from "recharts";

function App() {
  // State variables
  const [currentPrice, setCurrentPrice] = useState([]);
  const [avgPrice, setAvgPrice] = useState(null);
  const [max, setMax] = useState(null);
  const [min, setMin] = useState(null);
  const [maxTwo, setMaxTwo] = useState(null);
  const [minTwo, setMinTwo] = useState(null);
  const [volatility, setVolatility] = useState(null);
  const [selectedYear, setSelectedYear] = useState("2022");
  const [selectedMonth, setSelectedMonth] = useState("05");
  const [chartData, setChartData] = useState(null);

  // Helper function to generate an array of years
  const getYears = (start, end) => {
    const years = [];
    for (let year = start; year <= end; year++) {
      years.push(year);
    }
    return years;
  };

  // Array of months
  const months = [ "01","02","03","04","05","06","07","08","09","10","11","12" ];

  // Fetch current bitcoin price
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/bitcoin-price");
        setCurrentPrice(response.data.price.toFixed(2));
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, []);

  // Fetch KPIs
  useEffect(() => {
    const fetchKPIs = async () => {
      try {
        const response = await axios.get("http://localhost:8000/bitcoin-kpis");
        if (response.data != null) {
          setAvgPrice(response.data.avg_price);
          setMax(response.data.max_price);
          setMin(response.data.min_price);
          setVolatility(response.data.volatility);
          setMaxTwo(response.data.max_two);
          setMinTwo(response.data.min_two);
        }
      } catch (error) {
        console.error(error);
      }
    };
    fetchKPIs();
  }, []);

  // Fetch historic data
  useEffect(() => {
    const fetchHistoric = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/get-historic?year=${selectedYear}&month=${selectedMonth}`
        );
        if (response.data != null) {
          const chartData = response.data.map(({ price, year, month, day }) => ({
            year,
            month,
            day,
            price: parseFloat(price),
          }));
          setChartData(chartData);
        }
      } catch (error) {
        console.error(error);
      }
    };
    fetchHistoric();
  }, [selectedYear, selectedMonth]);

  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
      <div className="title">
        <h1>
          <center>
            <u>Bitcoin Dashboard</u>
          </center>
        </h1>
      </div>
      <div className="bottombar">
        <div style={{ borderBottom: '1px solid black', marginBottom: '10px' }}></div>
        <p><strong>Current Price:</strong> {currentPrice}$</p>
        <p><strong>Overall Average Price:</strong> {avgPrice}$</p>
        <p><strong>Historic Maximum Price:</strong> {max}$</p>
        <p><strong>Historic Minimum Price:</strong> {min}$</p>
        <p><strong>Overall Volatility:</strong> {volatility}$</p>
        <div style={{ borderBottom: '1px solid black', marginBottom: '10px' }}></div>
      </div>
      <div style={{ display: "flex", flexDirection: "row", flex: 1 }}>
        <div style={{ flex: 1 }}>
          <h3>Average Bitcoin price</h3>
          <LineChart width={600} height={300} data={chartData}>
            <XAxis dataKey="day" />
            <YAxis domain={[28300, 30001]} />
            <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
            <Line type="monotone" dataKey="price" stroke="#8884d8" />
            <Tooltip />
            <Legend />
          </LineChart>
          <div>
            <label htmlFor="year">Year: </label>
            <select
              id="year"
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
            >
              {getYears(2013, 2023).map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="month">Month: </label>
            <select
              id="month"
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
            >
              {months.map((month) => (
                <option key={month} value={month}>
                  {month}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div style={{ flex: 1 }}>
          <h3>Maximum and Minimum Price (2022) </h3>
          {minTwo && maxTwo && (
            <BarChart width={600} height={300} data={[{ name: 'Price Range', min: parseFloat(minTwo), max: parseFloat(maxTwo) }]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 30000]} />   
              <Tooltip />
              <Legend />
              <Bar dataKey="min" fill="#82ca9d" />
              <Bar dataKey="max" fill="#8884d8" />
            </BarChart>
          )}
        </div>
      </div>      
    </div>
  );
}

export default App;

  


// start frontend:
// cd react-frontend && npm start

