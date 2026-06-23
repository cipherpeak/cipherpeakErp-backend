# Docker Setup and Usage Guide

This guide provides instructions for setting up and running the CipherERP Django application using Docker.

## Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. Start the Application

```bash
# Navigate to project directory
cd /path/to/peaku

# Build and start all services
docker-compose up --build
```

The application will be available at: **http://localhost:8000**

### 2. Stop the Application

```bash
# Stop services (keeping data)
docker-compose down

# Stop services and remove volumes (WARNING: deletes database data)
docker-compose down -v
```

## Detailed Usage

### Building Specific Services

```bash
# Build only the web service
docker-compose build web

# Rebuild without cache
docker-compose build --no-cache
```

### Running in Background

```bash
# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f web
docker-compose logs -f db
```

### Database Management

#### Execute Django Commands

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Open Django shell
docker-compose exec web python manage.py shell
```

#### Access PostgreSQL Database

```bash
# Connect to database
docker-compose exec db psql -U postgres -d cipherERPv1dev

# Backup database
docker-compose exec db pg_dump -U postgres cipherERPv1dev > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres cipherERPv1dev < backup.sql
```

### Migrating Existing Data

If you have existing data in your local PostgreSQL database:

```bash
# 1. Dump your current database
pg_dump -U postgres cipherERPv1dev > cipherERP_backup.sql

# 2. Start Docker containers
docker-compose up -d

# 3. Restore to Docker database
docker-compose exec -T db psql -U postgres cipherERPv1dev < cipherERP_backup.sql
```

## Development Workflow

### File Changes

The `backend` directory is mounted as a volume, so code changes are automatically reflected:

1. Edit your Python files
2. Django auto-reloads (when using `runserver`)
3. No need to rebuild the container

### Installing New Dependencies

When adding Python packages:

```bash
# Add package to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# 2. Rebuild the web service
docker-compose build web

# 3. Restart services
docker-compose up -d
```

## Production Deployment

### Using Gunicorn (Recommended)

Update `docker-compose.yml` web service command:

```yaml
command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

Then rebuild:

```bash
docker-compose up --build -d
```

### Using Nginx

Uncomment the nginx service in `docker-compose.yml` and restart:

```bash
docker-compose up -d
```

Access via: **http://localhost**

### Environment Variables for Production

Create a `.env.production` file:

```env
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
DB_NAME=cipherERPv1prod
DB_USER=postgres
DB_PASSWORD=secure-password-here
DB_HOST=db
DB_PORT=5432
```

Use it with:

```bash
docker-compose --env-file backend/.env.production up -d
```

## Troubleshooting

### Port Already in Use

If port 8000 or 5432 is already in use:

```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

### Database Connection Issues

```bash
# Check database is healthy
docker-compose ps

# View database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Container Won't Start

```bash
# View web service logs
docker-compose logs web

# Remove all containers and rebuild
docker-compose down
docker-compose up --build
```

### Reset Everything

```bash
# WARNING: This deletes all data!
docker-compose down -v
docker system prune -a
docker-compose up --build
```

## Useful Commands

```bash
# View running containers
docker-compose ps

# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# Execute bash in web container
docker-compose exec web bash

# Check disk usage
docker system df

# Clean up unused resources
docker system prune
```

## File Structure

```
peaku/                          # Main project directory
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Service orchestration
├── entrypoint.sh               # Container startup script
├── .dockerignore               # Files to exclude from build
├── .env.docker                 # Docker environment variables
├── requirements.txt            # Python dependencies
├── requirements-prod.txt       # Production dependencies
├── manage.py
├── config/                     # Django project config (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                       # All Django applications
│   ├── authapp/
│   ├── dashboard/
│   ├── home/
│   ├── office/
│   ├── profileapp/
│   └── task/
├── nginx/
│   └── nginx.conf              # Nginx configuration
└── DOCKER_README.md            # This file
```

## Support

For issues or questions, refer to:
- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
