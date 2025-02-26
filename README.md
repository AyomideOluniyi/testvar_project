# TestVar Flashcards

## Overview  
TestVar Flashcards is a web application designed for creating, sharing, and studying flashcard sets. Built using Flask, SQLAlchemy, and Bootstrap, it offers a modern and responsive user interface along with a robust API backend.

## Features
- **Flashcard Sets:** Create, view, update, and delete sets.
- **Flashcards:** Add flashcards with questions and answers, with an option to mark them as hidden.
- **Comments & Reviews:** Post user comments and reviews with star ratings.
- **Telemetry:** Record user interactions (e.g., when a flashcard's answer is revealed).
- **Admin Interface:** Update the daily flashcard set creation limit.
- **API Endpoints:** Access application data in JSON format (see `openapi.yaml` for full specifications).

##  Prerequisites
- Python 3.6 or later
- Git

## Steps

- **Clone the Repository:**
  ```bash 
   git clone https://github.com/AyomideOluniyi/testvar_project  

- **Create and Activate a Virtual Environment:**  
   python -m venv venv  
  
   # on Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate 

- **Install Dependencies:** 
   pip install flask flask_sqlalchemy  


## Running the Application 
- Start the server by running: python app.py  
- Open your browser and go to http://127.0.0.1:5000/  

## Running the Tests
Use the command: python test_app.py  
All tests should pass, indicating the application is functioning correctly.

## API Documentation 
Refer to the openapi.yaml file for detailed endpoint specifications.