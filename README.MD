# Health Monitoring Solution Deployment Guide

This guide will help you quickly deploy the Health Monitoring solution using Docker Compose.

## Deployment Steps

1. **Ensure Docker and Docker Compose are installed** on your system.

2. **Clone the repository** containing the Health Monitoring solution.

3. **Navigate to the repository directory** in your terminal.

4. **Run the following command** to build and start the services:

   ```sh
   docker compose up -d --build
   ```

## Exposed Endpoints

Once the services are up and running, the following endpoints will be available:

- **API Server**: [http://localhost:5001](http://localhost:5001)
- **Database (MySQL)**: [http://localhost:3306](http://localhost:3306)
- **Redis**: [http://localhost:6379](http://localhost:6379)
- **SMTP4Dev Dashboard**: [http://localhost:5000](http://localhost:5000)

## API Routes

You can find the API routes in the Postman Collection included in the repository. Import the Postman Collection into your Postman app to view and test the available API endpoints.