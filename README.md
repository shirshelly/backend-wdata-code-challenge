# Weather API Service

This API will give the you a timeline of a weather insight - if a certain condition, based on the weather parameters, is met for a specific location.

`https://backend-wdata-code-challenge-shirsh.onrender.com/weather/insight?condition={condition}&lat={lat}&lon={lon}` - will return either `true` or `false` for every timestamp, for the conditions:`veryHot` or `rainyAndCold`

## Table of Contents

- [How to Use this Service](#how-to-use-this-service)
- [Optimizations and Pitfalls](#optimizations-and-pitfalls)
- [Assumptions](#assumptions)
- [Missing Features for Production](#missing-features-for-production)

## How to Use this Service

### Prerequisites

- Python 3.x
- pandas
- flask

### Access the API

The API will be available at `https://backend-wdata-code-challenge-shirsh.onrender.com/weather/insight?condition={condition}&lat={lat}&lon={lon}`.

The service will return either `true` or `false` for every timestamp, for two predefined conditions:

    1. `veryHot`  - based on the condition `temperature > 30`
    2. `rainyAndCold` - based on the condition `temperature < 10 AND precipitation > 0.5`

**Please note that Temperature is in Celsius, and Precipitation Rate is in mm/hr.

- **Query Parameters**: lat, lon, condition
    - `condition` can be either `veryHot` or `rainyAndCold`
    - **Note that the URL is case sensitive!**
 
- **Example Query**: `https://backend-wdata-code-challenge-shirsh.onrender.com/weather/insight?lon=51.5&lat=24.5&condition=veryHot`
  
- **Output (JSON)**:

      ```json
      [
          {
              "forecastTime": "2021-04-02T13:00:00Z",
              "conditionMet": true
          },
          {
              "forecastTime": "2021-04-02T14:00:00Z",
              "conditionMet": true
          },
          {
              "forecastTime": "2021-04-02T15:00:00Z",
              "conditionMet": false
          }
      ]
      ```
      

## Optimizations and Pitfalls

### Optimizations
- Indexing: Add indexes to the database for faster query performance.

### Pitfalls
- Error Handling: More robust error handling and logging are needed, especially for database operations and HTTP requests.
- Scalability: SQLite is not suitable for high-concurrency applications. Consider using a more robust DBMS like PostgreSQL or MySQL for production.
- Framework Choice: This project uses Flask, which is great for small to medium-sized applications. However, for larger projects, a more robust framework like Django or a microservices architecture might be more suitable.
- Data Duplication: In this project, running the data ingestion more than once on the same data will produce in duplication of data.

## Assumptions
- The CSV file is well-formed and does not contain malformed rows
- The CSV file is small to medium in size, suitable for ingestion into a SQLite database.
- The data types of CSV columns are consistent and predictable.
- The Data ingestion will run only once.

## Missing Features for Production
1. Authentication and Authorization:
   - Implement authentication and authorization to secure the API endpoints.
2. Advanced Error Handling:
   - Add comprehensive error handling and logging mechanisms.
3. Data Validation:
   - Implement data validation to handle malformed CSV data gracefully.
4. Scalability:
   - Switch to a more robust database system (e.g., PostgreSQL, MySQL) for better scalability and concurrency handling.
   - Implement caching mechanisms to reduce database load and improve response times.
5. Testing:
   - Write unit tests and integration tests to ensure code reliability and correctness.
6. Real World Data:
   - Use a database that is being updated regularly with real world data.
   
