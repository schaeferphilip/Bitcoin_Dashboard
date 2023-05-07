# Bitcoin Dashboard

![Bitcoin Dashboard Preview](/btcimg.png)

Bitcoin Dashboard is a Full-stack Data Engineering project that fetches current and historic Bitcoin prices from an external API, stores them in a MongoDB database, computes KPIs and displays them in a dashboard. This project demonstrates full stack software development, data engineering, data analysis, data visualization, and containerization using modern technologies.

## Technologies Used

- ReactJS (with Hooks) - Frontend
- FastAPI - Backend
- MongoDB - Data Storage
- Pandas, Numpy - Data Processing
- Recharts - Data Visualization
- APScheduler - Daily Scheduling
- Docker - Containerization

## Features

- Fetches current Bitcoin price from CoinDesk API and stores it in MongoDB 'bitcoin_prices' collection once a day using APScheduler
- Fetches and stores historic Bitcoin data in MongoDB 'bitcoin_historic' collection on app start
- Computes and displays various KPIs based on historic and current data stored in the database using Numpy and Pandas, including Current Price, Overall Average Price, Historic Maximum Price, Historic Minimum Price, Overall Volatility
- Visualizes data using Recharts line charts to displays historic Bitcoin prices from the database, with the option to select a year and month
- Visualizes data using Recharts bar charts to display the historical maximum and minimum Bitcoin prices for a selected year, currently set to 2022
- Dockerized for easy deployment

## To run the project

1. Clone the repository and navigate to the root directory
2. (Start the Docker container: `docker-compose up --build`)
3. Open MongoDB connection with MongoDB compass
4. Create 'emertondb' Databse and 'bitcoin_prices' and 'bitcoin_historic' collections
3. Start the frontend: `cd react-frontend && npm start`
4. Start the backend: `cd fastapi-backend && uvicorn main:app --reload`

## Future Improvements

- Implement login and authentication for better security
- Expand data analysis and metrics computation
- Add more data visualization options
- Improve user interface and user experience

This project serves as an example of how modern technologies can be used to develop efficient and scalable solutions for full stack software development, data engineering, analysis, and visualization.
