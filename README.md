# Feedback Report Generator

## Setup & Run

### Stack Requirements
- **Backend Framework:** Django with Django Rest Framework(DRF)
- **Database:** PostgreSQL 16
- **Asynchronous Processing:** Celery
- **Message Broker:** Redis
- **Task Monitoring:** Flower
- **PDF Generation:** Reportlab
- **Package Management:** Poetry
- **Containerization:** Docker Compose

### Steps to Run

1. **Clone the repository**
   ```sh
   git clone https://github.com/21f2000143/feedback_report_generator.git
   cd feedback_report_generator
   ```

2. **Start Docker Desktop on your machine**

3. **Run the application**
   ```sh
   docker-compose up --build
   ```

4. **Base URL of the API**
   [http://localhost:8000](http://localhost:8000)

5. **Access the flower monitor**
   Open your web browser and navigate to [http://localhost:5555](http://localhost:5555)

6. **Stop the application**
   ```sh
   docker-compose down
   ```
7. **To start the application if you have already build it**
   ```sh
   docker-compose up
   ```

## Endpoints

### Generate HTML Report

- **URL:** `/assignment/html`
- **Method:** `POST`
- **Description:** Accepts JSON payload and returns a task_id for processing.
- **Payload Example:** Input
    ```json
    [
      {
        "namespace": "ns_example",
        "student_id": "00a9a76518624b02b0ed57263606fc26",
        "events": [
            {
                "type": "saved_code",
                "created_time": "2024-07-21 03:04:55.939000+00:00",
                "unit": "17"
            }
        ]
      }
    ]
    ```
- **Response:** Output
    ```json
    {
      "task_id": "a8646b3b-96db-4239-9298-51589c6d7340"
    }
    ```

### Check HTML Task Status and Retrieve Report

- **URL:** `/assignment/html/<task_id>`
- **Method:** `GET`
- **Description:** Returns HTML content if completed else json response with task status.
- **Examples:**
- **Status:** SUCCESS.
![Report generation process](docs/htmlresult.png)
- **Status:** PENDING.
    ```json
    {
      "task_id": "4eb51705-5b30-4fc3-a81b-8d8eaeca2117",
      "status": "PENDING"
    }
    ```
- **Status:** FAILURE.
    ```json
    {
      "task_id": "dd907d57-9a7a-4c46-84a6-05b2e231b893",
      "status": "FAILURE",
      "error": "division by zero"
    }
    ```
### Generate PDF Report

- **URL:** `/assignment/pdf`
- **Method:** `POST`
- **Description:** Accepts JSON payload and returns a task_id for processing.
- **Payload Example:** Input
    ```json
    [
      {
        "namespace": "ns_example",
        "student_id": "00a9a76518624b02b0ed57263606fc26",
        "events": [
            {
                "type": "saved_code",
                "created_time": "2024-07-21 03:04:55.939000+00:00",
                "unit": "17"
            }
        ]
      }
    ]
    ```
- **Response:** Output
    ```json
    {
      "task_id": "a8646b3b-96db-4239-9298-51589c6d7340"
    }
    ```

### Check PDF Task Status and Retrieve Report

- **URL:** `/assignment/pdf/<task_id>`
- **Method:** `GET`
- **Description:** downloads PDF file if completed else json response with task status.
- **Examples:**
- **Status:** SUCCESS.
![Report generation process](docs/htmlresult.png)
- **Status:** PENDING.
    ```json
    {
      "task_id": "4eb51705-5b30-4fc3-a81b-8d8eaeca2117",
      "status": "PENDING"
    }
    ```
- **Status:** FAILURE.
    ```json
    {
      "task_id": "dd907d57-9a7a-4c46-84a6-05b2e231b893",
      "status": "FAILURE",
      "error": "division by zero"
    }
    ```

## Assumptions and Design Decisions

- Efficient schema design for storing large HTML and PDF content.
- Followed REST principles in API design.
- Proper error handling and task retries configured.

---


