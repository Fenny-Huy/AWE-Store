# AWE Electronics Online Store (Assignment 3)

This is a starter Flask project for implementing the object-oriented design of the AWE Electronics online store.

## To Run
First, install all the necessary dependencies for the project

```bash
pip install flask flask-cors
```

Then change the directory to backend folder and run app.py

```bash
cd backend
python app.py
```

To host the frontend website, you can either host it with python built in function on another terminal and open localhost:8000 on a browser
```bash
cd frontend
python -m http.server
```

Or you can host it using live server extension on VSCode


## Folder Structure

- `/backend/models/` – the class implementations
- `/backend/app.py` – the application endpoints (e.g., add to cart, place order)
- `/backend/data` - the datasets
- `/frontend` - the frontend web interface