# Feedback Report Generator

## Setup

### Prerequisites
- Docker
- Docker Compose
- Poetry

### Steps to Run

1. **Clone the repository**
   ```sh
   git clone <repository-url>
   cd feedback_report_generator
   ```

2. **Install dependencies**
   ```sh
   poetry install 
   ```

3. **Run the application**
   ```sh
   docker-compose up --build
   ```

4. **Access the application**
   Open your web browser and navigate to [http://localhost:8000](http://localhost:8000)

5. **Stop the application**
   ```sh
   docker-compose down
   ```

6. **Clean up**
   ```sh
   docker system prune -af
   ```

## Endpoints

### Generate HTML Report

- **URL:** `/assignment/html`
- **Method:** `POST`
- **Description:** Accepts JSON payload and returns a task_id for processing.

### Check HTML Task Status and Retrieve Report

- **URL:** `/assignment/html/<task_id>`
- **Method:** `GET`
- **Description:** Returns task status and HTML content if completed.

### Generate PDF Report

- **URL:** `/assignment/pdf`
- **Method:** `POST`
- **Description:** Accepts JSON payload and returns a task_id for processing.

### Check PDF Task Status and Retrieve Report

- **URL:** `/assignment/pdf/<task_id>`
- **Method:** `GET`
- **Description:** Returns task status and PDF file if completed.

## Assumptions and Design Decisions

- Efficient schema design for storing large HTML and PDF content.
- Followed REST principles in API design.
- Proper error handling and task retries configured.

