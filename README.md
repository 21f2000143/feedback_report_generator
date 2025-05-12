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

2. **Setup and Start Docker Desktop on your machine**
   [https://docs.docker.com/](https://docs.docker.com/)

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

> Note: I have added the jwt-auth feature so registration and login is required.

- **URL:** `register-admin`
- **Method:** `POST`
- **Description:** Accepts JSON payload and returns username.
- **Payload Example:** Input
  ```json
  {
    "username": "admin3",
    "password": "password"
  }
  ```
- **Response:** Output
  `json
    {
    "username": "admin3"
    }
    `
  > > Now you can login and test out all the required API endpoints

> You can also see all the users without login

- **URL:** `users`
- **Method:** `GET`
- **Description:** return all the usernames and their role.

- **Response:** Output
  ```json
  {
    "count": 7,
    "next": null,
    "previous": null,
    "results": [
      {
        "username": "student2",
        "role": "admin"
      },
      {
        "username": "admin3",
        "role": "admin"
      },
      {
        "username": "adim4",
        "role": "admin"
      },
      {
        "username": "student3",
        "role": "student"
      }
    ]
  }
  ```

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
  ```json
  {
    "task_id": "6d2552c6-55d8-4562-92eb-c996a2ebbfed",
    "status": "SUCCESS",
    "html_content": "<!DOCTYPE html>\n<html lang=\"en\">\n\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Assignment Report</title>\n</head>\n\n<body>\n    <div id=\"reports\">\n        \n        <div>\n            <h2>Student ID: 00a9a76518624b02b0ed57263606fc26</h2>\n            <p>Event Order: Q1</p>\n        </div>\n        \n    </div>\n</body>\n\n</html>\n"
  }
  ```
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
  <img src="docs/pdfresult.png" width="300" height="100" />
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

- Efficient schema design for storing large HTML and PDF content. We are are okay with the default TOAST feature of Postgresql and Storing pdf files in the server file system.
- Proper error handling and task retries configured from default(3) to (2) assuming we are dealing with large files.
- For testing the api please use testing client which supports binary data(pdf) download or execute this url `/assignment/pdf/<task_id>` in browser.

---
