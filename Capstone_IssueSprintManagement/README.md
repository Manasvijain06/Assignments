# Issue & Sprint Management System

## Overview

This is a backend + frontend full-stack project built using FastAPI, React, and MongoDB.
It follows Agile workflow concepts like Issue Tracking and Sprint Management.

---

## Tech Stack

### Backend:

- FastAPI
- MongoDB (Atlas)
- PyMongo
- Pydantic
- Pytest
- JWT Authentication (coming soon)

### Frontend:

- React (Vite)
- Axios
- React Router DOM

---

## Project Structure

```
Capstone_Issue_Sprint_Management_System/
│
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   └── (React app)
│
└── README.md
```

---

## Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-link>
cd Capstone_Issue_Sprint_Management_System
```

---

### 2. Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run server:

```
uvicorn app.main:app --reload
```

---

### 3. Frontend Setup

```
cd frontend
npm install
npm run dev
```

---

## Testing

Run backend tests:

```
pytest
```

---

## Database

- MongoDB Atlas is used
- Connection is managed using environment variables (.env)

---

## Current Progress

- Backend setup completed
- FastAPI initialized
- MongoDB connected
- Pytest configured
- Frontend initialized (React)

---

## Upcoming Features

- User Authentication (JWT)
- Project Management APIs
- Issue Tracking System
- Sprint Management System
- Comments System
- Frontend Dashboard

---

## 👨‍💻 Author

Capstone Project - Issue & Sprint Management System
