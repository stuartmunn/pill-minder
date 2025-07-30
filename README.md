# Pill Minder

This is a multi-user medication reminder application with a web interface.

Warning: The application is still under development and contains many issues!

## Features

- Multi-user system with registration and login.
- Web dashboard to view and manage medications.
- Mark medications as 'Taken' from the web interface.
- Medication information lookup using the British National Formulary (BNF).

## Next Steps

- Improve Registration & Login Experience
- UX Improvements
- Notications

## Setup

### 1. Set Environment Variables

Create a `.env` file in the project root and add the following:

```
SECRET_KEY=a_very_secret_key
```

Replace `a_very_secret_key' with a secure key

### 2. Build and Run the Docker Container

1.  Build the Docker image:

    ```bash
    docker build -t pill-minder .
    ```

2.  Run the Docker container:

    ```bash
    docker run -d -p 5003:5000 -e SECRET_KEY="testing" -v pill-minder-data:/app/instance --name pill-minder-app pill-min
der-app
    ```

    The application will be available at [http://localhost:5000](http://localhost:5000).
