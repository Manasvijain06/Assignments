
# Issue & Sprint Management System

A full-stack web application developed using **FastAPI**, **React**, and **MongoDB** to help Agile teams manage projects, sprints, and issues efficiently. The system provides secure authentication, role-based access control, sprint planning, issue tracking, and collaboration through comments.

---

# Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Database Design](#database-design)
- [User Roles](#user-roles)
- [API Modules](#api-modules)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)

---

# Overview

The Issue & Sprint Management System is designed to simplify Agile project management by allowing users to organize work into projects, plan sprints, track issues, and collaborate through comments.

The application follows a layered backend architecture using FastAPI with MongoDB and a modern React frontend built using Vite.

Authentication is secured using JWT Bearer Tokens and passwords are encrypted using bcrypt.

---

# Features

## Authentication

- Secure user registration with email validation.
- User login using JWT Bearer authentication.
- Passwords are securely encrypted using **bcrypt** before storage.
- Protected API endpoints using authentication middleware.
- Token-based authorization for accessing secured resources.
- Session persistence on the frontend using Local Storage.

---

## User Management

### Role-Based Access Control (RBAC)

The application supports three user roles with different permissions.

### Admin
- Create, update, and delete projects.
- Add or remove project members.
- View all projects in the system.
- Create and manage sprints.
- Start and complete sprints.
- Create and assign issues.
- Update the status of any issue.
- View project summaries and dashboard statistics.

### Member
- Access only assigned projects.
- Create new issues within assigned projects.
- View project issues and sprint details.
- Update the status of issues assigned to themselves.
- Add comments to issues.
- Edit and delete their own comments.

### Viewer
- View assigned projects.
- View sprint details.
- View issues and comments.
- Read-only access with no modification permissions.

---

## Project Management

- Create projects with a unique project key.
- Update project information.
- Delete existing projects.
- View all accessible projects.
- Assign and remove project members.
- Display project summaries including:
  - Total Issues
  - Open Issues
  - Closed Issues
  - Active Sprints
- Automatic project filtering based on user role.
- Persist selected project across pages using Local Storage.

---

## Sprint Management

- Create sprints for individual projects.
- Define sprint start and end dates.
- Start active sprints.
- Complete running sprints.
- View sprint details and associated issues.
- Add eligible issues to a sprint.
- Remove issues from a sprint.
- Prevent completed (DONE) issues from being added.
- Validate sprint date ranges.
- Search sprints by name.
- Filter sprints by project and status.
- Paginated sprint listing.

---

## Issue Management

- Create different issue types:
  - Story
  - Task
  - Bug
- Support parent-child relationships between stories and tasks/bugs.
- Assign issues to project members.
- Automatically generate unique issue keys.
- Update issue status following predefined workflow.
- View issue details.
- Search issues by:
  - Title
  - Description
  - Issue Key
- Filter issues by:
  - Status
  - Priority
  - Assignee
- Paginated issue listing.
- Nested display of child issues under parent stories.

Supported Status Workflow

```
Backlog
    ↓
Todo
    ↓
In Progress
    ↓
Done
```

Invalid status transitions are automatically rejected.

---

## Comment Management

- Add comments to issues.
- Edit existing comments.
- Delete comments.
- Restrict edit/delete operations to the comment owner.
- Display comment creation timestamp.
- Paginate comments for improved readability.

---

## Search & Filtering

- Search issues using keywords.
- Search sprints by name.
- Filter issues by:
  - Status
  - Priority
  - Assignee
- Filter sprints by:
  - Project
  - Sprint Status
- Server-side pagination for projects, sprints, issues, and comments.

---

## Dashboard & User Interface

- Clean and responsive React-based interface.
- Dashboard with project statistics.
- Notification system for success and error messages.
- Modal-based forms for create/update operations.
- Persistent project selection across modules.
- Dynamic navigation based on user role.
- Interactive issue and sprint detail views.

---

## Validation & Business Rules

- Unique project keys.
- Unique sprint names within a project.
- Sprint start date cannot be after the end date.
- Stories cannot have parent stories.
- Only stories can act as parent issues.
- Members can update only issues assigned to them.
- Users can edit or delete only their own comments.
- DONE issues cannot be added to a sprint.
- Invalid issue status transitions are prevented.
- Invalid sprint status transitions are prevented.

---

## Testing

- Unit testing using **pytest**.
- API testing using **FastAPI TestClient**.
- Mock-based testing using **unittest.mock**.
- Test coverage for:
  - Authentication
  - Authorization
  - Projects
  - Sprints
  - Issues
  - Comments
  - Search
  - Validation
  - Edge Cases

# Tech Stack

## Frontend
```
| Technology     | Purpose                                                                                |
|----------------|----------------------------------------------------------------------------------------|
| **React**      | Builds the user interface using reusable, component-based architecture.                |
| **Vite**       | Fast frontend build tool and development server with Hot Module Replacement.           |
| **Axios**      | Handles HTTP requests between the React frontend and FastAPI backend.                  |
| **JavaScript** | Implements frontend application logic, state management, and user interactions.        |
| **CSS**        | Styles the application with responsive layouts, modals, dashboards, and UI components. |
```
---

## Backend
```
| Technology   | Purpose                                                                             |
|--------------|-------------------------------------------------------------------------------------|
| **FastAPI**  | High-performance Python framework for building RESTful APIs.                        |
| **Python**   | Core programming language used for implementing backend business logic.             |
| **Pydantic** | Performs request validation, response serialization, and data validation.           |
| **PyMongo**  | Connects the FastAPI application with MongoDB and performs database operations.     |
| **JWT**      | Provides secure user authentication and protects API endpoints using Bearer tokens. |
| **bcrypt**   | Hashes user passwords securely before storing them in the database.                 |
```
---

## Database
```
| Technology  | Purpose                                                                               |
|-------------|---------------------------------------------------------------------------------------|
| **MongoDB** | NoSQL document database used to store users, projects, sprints, issues, and comments. |
```
---

## Testing
```
| Technology             | Purpose                                                                   |
|------------------------|---------------------------------------------------------------------------|
| **pytest**             | Framework used for writing and executing backend unit tests.              |
| **FastAPI TestClient** | Simulates HTTP requests to test API endpoints without running the server. |
| **unittest.mock**      | Mocks services and dependencies to isolate business logic during testing. |
```
---

## Development Tools
```
| Tool                     | Purpose                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| **Git**                  | Version control system used to track source code changes.               |
| **GitHub**               | Hosts the project repository and manages branches, pull requests.       |
| **VS Code**              | Primary IDE used for backend and frontend development.                  |
| **MongoDB Compass**      | GUI tool used to view and manage MongoDB collections and documents.     |
| **Postman / Swagger UI** | Used for testing and validating REST API endpoints during development.  |
```
---

# System Architecture

```
                    React Frontend
                           │
                           ▼
                 Axios HTTP Requests
                           │
                           ▼
                 FastAPI API Routers
                           │
                           ▼
        Authentication & Authorization
             (JWT + Role-Based Access)
                           │
                           ▼
             Request Validation (Pydantic)
                           │
                           ▼
                 Service Layer (Business Logic)
                           │
                           ▼
              Repository Layer (Database Access)
                           │
                           ▼
                     MongoDB Database
```
---

# Backend Folder Structure

```
backend
│
├── app
|   ├── constants
|   ├── core
|   ├── database
│   ├── dependencies
│   ├── exceptions
│   ├── models
│   ├── repositories
│   ├── router
│   ├── schemas
│   │   ├── requests
│   │   └── responses
│   ├── services
│   └── utils
│
├── tests
│   ├── auth
│   ├── users
│   ├── projects
│   ├── sprints
│   └── issues
│
├── requirements.txt
└── main.py
```

---

# Frontend Folder Structure

```
frontend
│
├── src
│   ├── api
│   ├── assets
│   ├── components
│   │   ├── issues
│   │   ├── projects
│   │   ├── sprints
|   |   ├── notification.jsx
│   │   └── sidebar.jsx
│   │
│   ├── pages
|   |   ├── issue.jsx
|   |   ├── login.jsx
|   |   ├── profile.jsx
|   |   ├── project.jsx
|   |   ├── register.jsx
|   |   └── sprint.jsx
|   |
│   ├── services
|   ├── styles
|   |   ├── auth.css
|   |   ├── feature.css
|   |   ├── global.css
|   |   └── layout.css
|   |
|   ├── utils
│   ├── App.jsx
│   └── main.jsx
|
├── gitignore
├── package.json
└── vite.config.js
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

---

## Backend Setup

```bash
cd backend
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run application

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# Environment Variables

Backend (.env)

```
MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=issue_sprint_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Frontend (.env)

```
VITE_API_URL=http://127.0.0.1:8000
```

---

# Database Collections

## Users

Stores user information.

Fields

- _id
- name
- email
- password
- role
- created_at

---

## Projects

Stores project details.

Fields

- _id
- name
- description
- project_key
- created_by
- members

---

## Sprints

Stores sprint information.

Fields

- _id
- name
- project_id
- start_date
- end_date
- status
- issues

---

## Issues

Stores issue information.

Fields

- _id
- issue_key
- project_id
- title
- description
- type
- priority
- status
- assignee
- created_by
- parent_id
- comments

---

# User Roles

## Admin

- Create Projects
- Update Projects
- Delete Projects
- Add Members
- Remove Members
- Create Sprints
- Start Sprint
- Complete Sprint
- Create Issues
- Update Any Issue Status
- Dashboard Access

---

## Member

- View Assigned Projects
- Create Issues
- Update Assigned Issue Status
- Add Comments
- Edit Own Comments
- Delete Own Comments

---

## Viewer

- View Projects
- View Sprints
- View Issues

---

# API Modules

Authentication

- Register
- Login

Projects

- Create Project
- Update Project
- Delete Project
- Get Projects
- Add Member
- Remove Member

Sprints

- Create Sprint
- Get Sprints
- Start Sprint
- Complete Sprint
- Add Issue
- Remove Issue

Issues

- Create Issue
- Get Issues
- Update Status
- Search Issues
- Filter Issues

Comments

- Add Comment
- Update Comment
- Delete Comment

---

# Testing

The project includes automated backend testing using pytest.

Covered Modules

- Authentication
- Role Checks
- Projects
- Project Edge Cases
- Sprints
- Sprint Edge Cases
- Issues
- Issue Status
- Comments
- Search
- Edge Cases

Run Tests

```bash
pytest
```

---

# Business Rules

- Project key must be unique.
- Sprint names must be unique within a project.
- Sprint start date cannot be after end date.
- Stories cannot have parent stories.
- Only stories can have child issues.
- Members can update only issues assigned to them.
- Users can edit or delete only their own comments.
- DONE issues cannot be added to a sprint.
- Invalid issue status transitions are rejected.
- Invalid sprint status transitions are rejected.

---

# Future Enhancements

- Email Notifications
- File Attachments
- Activity Timeline
- Sprint Reports
- Dashboard Analytics
- Dark Theme
- Docker Support
- CI/CD Pipeline
- Real-Time Notifications

---

# Author

**Manasvi Jain**

Capstone Project

Issue & Sprint Management System
