# 1. MavunoHub API

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About the Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## 1.1. About the Project

MavunoHub API is an API for facilitating the following activities:

- **Marketplace for farm produce:** Farmers can post their products on the platform for potential buyers.
- **Facilitate Orders:** The platform handles orders along with the related transactions.
- **Register Retailer Accounts:** Retailers can register to buy products in bulk.
- **User Authentication:** Authorize requests and ensure security.

## 1.2. Built With

- [Django](https://www.djangoproject.com/) - A high-level Python web framework
- [Django REST Framework](https://www.django-rest-framework.org/) - A powerful toolkit for building Web APIs

## 1.3. Getting Started

To set up MavunoHub API locally, follow these steps.

### 1.3.1. Prerequisites

- **Python 3.12+**
- **PostgreSQL**
- **Git**
- **Poetry**

To install poetry, visit [Python Poetry](https://github.com/python-poetry/install.python-poetry.org)

### 1.3.2. Installation

1. **Clone the repository**
   ```sh
   git clone git@github.com:elisoft-engineer/mavunohub-api.git
   cd mavunohub-api
   ```

2. **Create a virtual environment**
   ```sh
   poetry env activate

   source $(poetry env info --path)  # Linux / MacOS
   source "$(poetry env info --path)/Scripts/activate" # Git Bash / MinGW (Windows)
   & "$(poetry env info --path)\Scripts\activate.ps1" # PowerShell (Windows)
   ```

3. **Install dependencies**
   ```sh
   poetry install --no-root
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env.dev` and update with your settings:
   ```env
   DEBUG=True
   SECRET_KEY=your_secret_key

   DATABASE_NAME=mavunohub
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_USER=your_user
   DATABASE_PASSWORD=your_password

   ACCESS_TOKEN_LIFETIME=15
   REFRESH_TOKEN_LIFETIME=7

   ALLOWED_ORIGINS=http://localhost:5173
   ```

   **To create a secret key run the following:**
   ```sh
   python manage.py shell
   ```
   After shell opens, run these commands to get a secret key:
   ```python
   from django.core.management.utils import get_random_secret_key
   get_random_secret_key()
   ```
   Copy the secret key and place it in .env.dev SECRET_KEY variable

   **To create the database follow these steps:**
   - Connect to postgres
   ```sh
   sudo -u postgres psql # Linux / MacOS
   psql -U postgres # Windows
   ```
   - Create the database with a user
   ```sql
   CREATE ROLE your_user WITH LOGIN PASSWORD 'your_password';
   CREATE DATABASE mavunohub OWNER your_user;
   GRANT ALL PRIVILEGES ON DATABASE mavunohub TO your_user;
   \c mavunohub
   GRANT ALL PRIVILEGES ON SCHEMA public TO your_user;
   \q
   ```

5. **Apply database migrations**
   ```sh
   python manage.py migrate
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/`.

## 1.4. Usage

After installation, you can interact with the API endpoints:
- **Visit Documentation** found in `/api/docs/` to see API endpoints

## 1.5. Contributing

To contribute:

1. Create a feature branch (`git checkout -b feature/your-feature`)
2. Commit your changes (`git commit -m 'Add some feature'`)
3. Push to the branch (`git push origin feature/your-feature`)
4. Open a Pull Request

Please ensure your code follows the existing style and includes tests where applicable.

## 1.6. License

This project is licensed under the **MavunoHub Software License Agreement**. See the [LICENSE](LICENSE) file for details.

## 1.7. Contact

Project Maintainer – [elisoft.engineer@gmail.com](mailto:elisoft.engineer@gmail.com)

## 1.8. Acknowledgments

- Hat tip to the Django and Django REST Framework communities
- Inspiration from various form processing and analytics platforms
