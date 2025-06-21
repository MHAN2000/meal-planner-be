# Smart Recipe & Meal Planner

[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](https://github.com/your-github-repo/workflows/CI/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

* [About the Project](#about-the-project)
* [Features](#features)
* [Technical Stack](#technical-stack)
* [Architecture](#architecture)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Local Development Setup](#local-development-setup)
* [CI/CD Pipeline](#cicd-pipeline)
* [AI Integration (AWS Bedrock)](#ai-integration-aws-bedrock)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)

---

## About the Project

The "Smart Recipe & Meal Planner" is a web application designed to simplify meal planning, recipe management, and grocery shopping. It empowers users to store their favorite recipes, effortlessly plan meals for the week, generate consolidated shopping lists, and even get creative recipe suggestions or adaptations using Artificial Intelligence.

---

## Features

* **User Authentication:** Secure registration and login.
* **Recipe Management:** CRUD operations (Create, Read, Update, Delete) for personal recipes with details like ingredients, instructions, prep/cook times, and tags. Supports recipe image uploads.
* **Meal Planning:** Intuitive weekly calendar to assign recipes to specific meal slots.
* **Shopping List Generation:** Automated creation of consolidated shopping lists based on planned meals, with item marking.
* **AI-Powered Recipe Adaptation:** Adapt existing recipes (e.g., make vegetarian, suggest substitutions, scale portions) using generative AI.
* **AI-Powered Recipe Suggestion:** Get new recipe ideas based on a list of ingredients you have on hand.

---

## Technical Stack

This project leverages a modern full-stack architecture with a focus on Python for the backend and React for the frontend.

* **Backend:**
    * **Language:** Python
    * **Framework:** FastAPI
    * **ORM:** SQLAlchemy
    * **Migrations:** Alembic
    * **Caching:** Redis (via `redis-py`)
    * **Database Driver:** PyMySQL
* **Frontend:**
    * **Framework:** React
    * **Language:** TypeScript
    * **Styling:** (e.g., Tailwind CSS, Material UI, or Ant Design - *Specify your choice here*)
* **Database:** MySQL (managed by AWS RDS in production)
* **AI:** AWS Bedrock (via `boto3`)
* **Containerization:** Docker, Docker Compose
* **CI/CD:** Jenkins (Orchestration), AWS CodeBuild, AWS Elastic Beanstalk, AWS S3, AWS CloudFront (for deployment to AWS)

---

## Architecture

The application follows a modular, layered architecture:

* **Frontend:** A single-page application (SPA) built with React, consuming data from the FastAPI backend.
* **Backend:** A FastAPI REST API that handles business logic, interacts with the MySQL database, Redis cache, and integrates with AWS Bedrock for AI capabilities. It's containerized with Docker.
* **Database:** A MySQL instance for persistent storage of user, recipe, and meal planning data.
* **Cache:** Redis acts as an in-memory data store for caching frequently accessed data and potentially for session management, speeding up API responses.
* **AI Layer:** Integrates with AWS Bedrock, providing access to large language models for complex AI features like recipe adaptation and generation.
* **CI/CD:** Jenkins orchestrates the automated build, test, and deployment process to AWS.

---

## Getting Started

Follow these steps to get your development environment up and running.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Git:** For cloning the repository.
* **Docker Desktop** (for Windows/macOS) or **Docker Engine** (for Linux): Essential for running the application services.
* **Python 3.10+** (Local Virtual Environment): Recommended for running Alembic commands locally for setup and managing project dependencies (`pip`).
* **Node.js & npm/Yarn** (for Frontend development): If you plan to work on the React frontend.

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-github-repo/smart-recipe-meal-planner.git](https://github.com/your-github-repo/smart-recipe-meal-planner.git)
    cd smart-recipe-meal-planner
    ```

2.  **Create and configure `.env` file:**
    In the root of your project directory, create a file named `.env`. Copy the contents from the `.env.example` (or the one we've been using) into it. **Crucially, ensure this file is in the same directory as your `docker-compose.yml` file.**

    ```env
    # .env
    # MySQL Database Credentials
    MYSQL_DATABASE=smart_recipe_db
    MYSQL_USER=mhan
    MYSQL_PASSWORD=mhan
    MYSQL_ROOT_PASSWORD=mhan # For MySQL container startup

    # Redis Credentials
    REDIS_HOST=redis
    REDIS
