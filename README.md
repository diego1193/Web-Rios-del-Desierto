# Web-Rios-del-Desierto

A comprehensive client and purchase management system for Rios del Desierto SAS. This web application enables efficient tracking of client information, purchase history, and loyalty program management.

## Features

- **Client Management**: Add, edit, and search clients by document type and number
- **Purchase Recording**: Record individual purchases or bulk import via CSV/Excel
- **Loyalty Program**: Generate reports for high-value clients (purchases over 5,000,000 COP)
- **Document Types**: Support for multiple document types (ID, Passport, NIT)
- **User Authentication**: Secure admin access to system features

## Tech Stack

- **Backend**: Django 4.2.6
- **Frontend**: Bootstrap, JavaScript
- **Database**: SQLite (containerized)
- **Containerization**: Docker & Docker Compose
- **Data Processing**: Pandas, NumPy
- **File Handling**: openpyxl for Excel generation
- **Deployment**: Gunicorn for WSGI server
- **Static Files**: WhiteNoise for serving static assets

## Installation & Setup

### Prerequisites

- Docker and Docker Compose
- Git

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/diego1193/Web-Rios-del-Desierto.git
   cd web-rios-del-desierto
   ```

2. Create a `.env` file (or use the existing one for development):
   ```
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DEBUG=0
   ALLOWED_HOSTS=localhost,127.0.0.1
   DJANGO_SETTINGS_MODULE=web_sac.settings_docker
   ```

3. Build and start the Docker container:
   ```bash
   docker-compose up --build
   ```

4. Access the application at http://localhost:8000 or http://127.0.0.1:8000

### Default Admin User

The application automatically creates an admin user on first startup:
- **Username**: admin
- **Password**: 1234
- **Email**: admin@example.com


## Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `SECRET_KEY` | Django secret key | Generated default key |
| `DEBUG` | Debug mode (1=True, 0=False) | 0 |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | localhost,127.0.0.1 |
| `DJANGO_SETTINGS_MODULE` | Settings module to use | web_sac.settings_docker |
| `DJANGO_SUPERUSER_USERNAME` | Admin username | admin |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | 1234 |
| `DJANGO_SUPERUSER_EMAIL` | Admin email | admin@example.com |

## Docker Setup Details

The application is containerized using Docker with the following components:

### Dockerfile

- Base image: Python 3.9.21-slim
- Installs required system dependencies
- Sets up a non-root user for security
- Pre-collects static files during image build
- Exposes port 8000

### Docker Compose Configuration

The `docker-compose.yml` file defines the following:

- Web service built from local Dockerfile
- Environment variable configuration
- Port mapping (8000:8000)
- Volume mounts for code, static files, and database
- Startup commands to:
  - Create static directory
  - Run migrations
  - Create superuser
  - Load test data
  - Start Gunicorn server

## Usage Guide

### Managing Clients

1. **Adding a New Client**
   - Navigate to the Clients section
   - Click "Add New Client"
   - Fill in the client details and submit the form

2. **Searching for a Client**
   - Use the search box at the top of the clients page
   - Search by name, document type, or document number
   - Click on a client to view their details

### Recording Purchases

1. **Adding a Single Purchase**
   - Go to the Purchases section
   - Click "Add Purchase"
   - Search for the client
   - Enter purchase amount, date, and optional description
   - Submit the form

2. **Bulk Upload Purchases**
   - Prepare a CSV or Excel file with the required columns:
     - document_type_id
     - document_number
     - purchase_date
     - amount
     - description (optional)
   - Navigate to Purchases > Bulk Upload
   - Select your file and check "Skip header" if needed
   - Submit the form

### Generating Reports

1. **Loyalty Report**
   - Navigate to the Reports section
   - Click "Loyalty Report"
   - Click "Download Excel Report"
   - The report shows clients with purchases over 5,000,000 COP

## Development

### Project Structure

```
web-rios-del-desierto/
├── clients/                         # Client management app
│   ├── management/                  # Custom management commands
│   │   └── commands/
│   │       └── load_test_data.py    # Data loading command
│   ├── migrations/                  # Database migrations
│   ├── static/                      # Static assets for client app
│   │   └── clients/
│   │       ├── css/
│   │       │   └── styles.css
│   │       └── js/
│   │           └── add_client.js
│   ├── templates/                   # HTML templates
│   │   └── clients/
│   │       ├── base.html
│   │       ├── search.html
│   │       └── add_client.html
│   ├── models.py                    # Client data models
│   └── views.py                     # Client view functions
├── reports/                         # Reporting and purchase app
│   ├── migrations/                  # Database migrations
│   ├── static/                      # Static assets
│   │   └── reports/
│   │       └── js/
│   │           └── manage_purchases.js
│   ├── templates/                   # HTML templates
│   │   └── reports/
│   │       ├── loyalty_report.html
│   │       └── manage_purchases.html
│   ├── models.py                    # Purchase data models
│   └── views.py                     # Report view functions
├── web_sac/                         # Main project directory
│   ├── settings.py                  # Base settings
│   ├── settings_docker.py           # Docker-specific settings
│   ├── urls.py                      # URL routes
│   └── wsgi.py                      # WSGI entry point
├── .dockerignore                    # Files to exclude from Docker context
├── .env                             # Environment variables
├── docker-compose.yml               # Docker Compose configuration
├── Dockerfile                       # Docker build instructions
├── manage.py                        # Django management script
├── README.md                        # Project documentation
└── requirements.txt                 # Python dependencies
```

### Local Development with Docker

1. Start the development server:
   ```bash
   docker-compose up --build
   ```

2. Access the application at http://localhost:8000 or http://127.0.0.1:8000


## Database Schema

### Main Models

1. **DocumentType**
   - name: Document type name (e.g., "National ID")
   - code: Short code (e.g., "ID", "PASS", "NIT")

2. **Client**
   - document_type: ForeignKey to DocumentType
   - document_number: Document identifier
   - first_name, last_name: Client name
   - email, phone_number: Contact info
   - address, city: Location info
   - created_at, updated_at: Timestamps

3. **Purchase**
   - client: ForeignKey to Client
   - amount: Purchase amount (decimal)
   - purchase_date: Date of purchase
   - invoice_number: Optional reference number
   - description: Optional text description
   - created_at: Record creation timestamp

## Testing

The application includes test data that can be loaded with:

```bash
python manage.py load_test_data
```

This creates:
- Sample document types (ID, Passport, NIT)
- Sample clients with different document types
- Sample purchases, including one client with purchases over 5,000,000 COP for testing the loyalty report

## Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   - Ensure the static directory exists: `mkdir -p /app/static`
   - Run collectstatic: `python manage.py collectstatic --noinput`

2. **Migration Issues**
   - If you encounter database schema issues, try:
     ```bash
     docker-compose exec web python manage.py makemigrations
     docker-compose exec web python manage.py migrate
     ```

3. **Permission Errors**
   - If you see permission errors with the database, check that the `/app/db` directory has proper permissions.

4. **Container Not Starting**
   - Check Docker logs: `docker-compose logs`
   - Ensure all required environment variables are set

## Production Deployment

For production deployment, make the following changes:

1. Set `DEBUG=0` in your `.env` file
2. Generate a strong unique `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your production domain
4. Consider using a more robust database like PostgreSQL
5. Set up proper SSL/TLS with a reverse proxy (Nginx, Caddy, etc.)
6. Use stronger credentials for the superuser
7. Set up backup procedures for your database

## Security Considerations

- The container runs as a non-root user (`appuser`) for improved security
- In production, change the default admin credentials immediately
- Use HTTPS in production environments
- Consider implementing rate limiting for API endpoints
- Regularly update dependencies to patch security vulnerabilities
