## Breezelytics

## Overview
Breezelytics provides real-time air quality data by displaying current PM2.5 values for a given location. 

It also offers historical records and future predictions of air pollution levels. 

The system is designed with a scalable architecture utilizing various modern technologies for data processing and storage.

I have extensively documented my learnings as well.

This project is also an exploration of big data handling technologies.

### Key Features:
- **Real-time PM2.5 Data**: Retrieves air quality information from the API of `https://aqicn.org/`.
- **Historical & Forecast Data**: Stores past records and  future values.
- **Docker Compose Network**: Orchestrates Django, Spark, and Cassandra services efficiently.
- **Scalable Architecture**: Supports large-scale data processing with Spark and Cassandra.


## Tech Stack
- **Backend**: Django (API communication and Frontend interaction)
- **Frontend**: Flutter (Mobile application for UI/UX)
- **Processing Engine**: Apache Spark (Data processing)
- **Database**: Apache Cassandra (Storage of records)
- **Containerization**: Docker (Encapsulation and portability of services)

## Workflow
The system operates as follows:
1. The **mobile app (Flutter)** requests PM2.5 data records from the **Django backend**.
2. **Apache Spark** processes and retrieves records from Cassandra for historical data access.
3. The data is then sent back to the mobile app for display.
4. Django fetches real-time data from `https://aqicn.org/` and stores it in **Cassandra**.
5. All services communicate within the **Docker Compose Network** (`aqinet`).

![Workflow](https://github.com/user-attachments/assets/a672c044-86f1-4701-ad57-c7a123ba0dec)

## Setup & Installation
### Prerequisites
Ensure you have the following installed on your system:
- Docker
- Python & Django
- Flutter SDK
- Apache Spark
- Apache Cassandra

### Steps to Run the App
1. **Clone the repository:**
   ```bash
   git clone https://github.com/DS-1090/Breezelytic
   cd StoreData_Django_Cdb
   ```
   
2. **Build Django App Image:**
   ```bash
   docker build -t djangoapp .
   ```
   
3. **Set up and run Docker containers and create Docker Compose Network:**
   ```bash
   docker-compose up --build
   ```

4. **Run the Flutter App:**
   ```bash
   cd Breezelytic
   flutter run
   ```

## Future Improvements
- **Redis/MySQL Integration**: Implement caching to enable faster access to past records.
- **Kafka Integration**: Utilize Apache Kafka for direct and automated storage of PM2.5 records in Cassandra, eliminating manual intervention.
- **Enhanced Spark Processing**: Optimize Spark jobs for better performance.

## Spark Web
![Spark Web](https://github.com/user-attachments/assets/94f55e09-195e-42b4-856e-b3cc0c316cd9)

## Cassandra DataBase
![Cassandra Database](https://github.com/user-attachments/assets/94e67de0-5303-4649-a422-fceea65f2e85)

## Mobile App

![Mobile App](https://github.com/user-attachments/assets/4260a545-a308-410e-8830-6448ca05d9c9)

- **Current Location PM2.5 Data**
  
![PM2.5 Data](https://github.com/user-attachments/assets/d65642a2-7553-47db-9de3-d78307509d98)

- **Home Screen**
  
![Home Screen](https://github.com/user-attachments/assets/bbfbddf3-60ae-4588-a07d-c9083e2ff383)

- **Records Page**
  
![Records](https://github.com/user-attachments/assets/8b5f5bc1-f3eb-410f-bfba-4a1706686c80)

- **Loading Screen**
  
![Loading Screen](https://github.com/user-attachments/assets/5cafba9f-85ad-4138-9636-a1a91ccddee7)

