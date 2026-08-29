# Romanian Railways (CFR) Search Engine

A full-stack web application built with **Django** and **Tailwind CSS** that acts as a real-time search engine for the Romanian Railway system. It parses official XML datasets, structures them into a relational database, and provides users with a clean, fast interface to find direct train routes between any two cities.

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Framework](https://img.shields.io/badge/Framework-Django_5-092E20?logo=django)
![Styling](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC?logo=tailwind-css)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)

## Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML5, Tailwind CSS, JavaScript
* **Database:** PostgreSQL

## Database Architecture

The system is built on a scalable relational model:
1. `Train`: Static data about the physical train (Number, Type/Rank, Company).
2. `Station`: Geographic data (City, Exact Station Name).
3. `Journey`: A specific instance of a Train running on a specific Date.
4. `Stop`: The intersection table linking a `Cursa` to a `Station`, containing Arrival Time, Departure Time, and Sequence Number.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites
* Python 3.10+
* pip (Python package manager)

### Installation

1. **Clone the repository:**
```bash
git clone [https://github.com/IonutMocanu/Train-schedules.git](https://github.com/IonutMocanu/Train-schedules.git)
cd Train-schedules
   ```
2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3. **Install dependecies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Import the Railway Dataset**
   ```bash
   python manage.py importa_date
   ```
6. **Start the development server**
   ```bash
   python manage.py runserver
   ```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser
