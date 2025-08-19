# Shorten It - Django URL Shortener

A comprehensive Django-based URL shortening service with user authentication, QR code generation, analytics, and URL customization features.

## Features

- **URL Shortening**: Create short, memorable URLs from long links
- **User Authentication**: Registration, login, and user-specific URL management
- **QR Code Generation**: Automatic QR codes for every shortened URL
- **URL Customization**: Custom slugs, expiration dates, and categories
- **Analytics**: Click tracking and category-based statistics
- **Responsive Design**: Mobile-friendly interface
- **AJAX Features**: Real-time updates without page refresh

## Installation & Setup

### Prerequisites
- Python 3.12+
- Django 5.2.5
- pip (Python package manager)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
```bash
pip install Django==5.2.5
pip install qrcode==8.2
pip install pillow==11.3.0
```

### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Run Development Server
```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

## Project Structure

```
shorten_it/
├── db.sqlite3                 # SQLite database
├── manage.py                 # Django management script
├── media/                    # Media files (QR codes)
│   └── qr_codes/            # Generated QR code images
├── shortenit/               # Main Django app
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Form definitions
│   ├── models.py            # Database models
│   ├── tests.py             # Test cases
│   ├── urls.py              # URL patterns
│   ├── utils.py             # Utility functions
│   ├── views.py             # View functions
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files
│   │   ├── css/
│   │   │   └── style.css    # Main stylesheet
│   │   └── js/
│   │       └── script.js    # JavaScript functionality
│   └── templates/           # HTML templates
│       ├── base.html        # Base template
│       ├── index.html       # Homepage
│       ├── register.html    # Registration
│       ├── login.html       # Login
│       ├── dashboard.html   # User dashboard
│       ├── my_urls.html     # User URLs list
│       ├── profile.html     # User profile
│       ├── customize_url.html
│       ├── short_url.html   # Shortened URL display
│       ├── analytics.html   # Analytics dashboard
│       └── expired_url.html # Expired URL page
└── urlshortener/            # Django project configuration
    ├── __init__.py
    ├── asgi.py              # ASGI configuration
    ├── settings.py          # Django settings
    ├── urls.py              # Root URL configuration
    └── wsgi.py              # WSGI configuration
```

## Configuration

### Database Settings
- **Engine**: SQLite3 (default)
- **File**: `db.sqlite3`

### Media & Static Files
- **Static URL**: `/static/`
- **Media URL**: `/media/`
- **Media Root**: `BASE_DIR / "media"`

### Site Configuration
- **Site Scheme**: http
- **Site Domain**: localhost:8000

## Database Schema

### URL Model
| Field | Type | Description |
|-------|------|-------------|
| `original_url` | URLField | Original long URL |
| `short_url` | SlugField | Unique short slug |
| `user` | ForeignKey | Associated user (nullable) |
| `click_count` | IntegerField | Click counter |
| `creation_date` | DateTimeField | Creation timestamp |
| `expiry_date` | DateTimeField | Optional expiration date |
| `category` | CharField | URL category (work/socials/other) |
| `qr_code_image` | ImageField | QR code image |

## URL Patterns

### Main URLs
- `/` - Homepage with URL shortening
- `/<short_url>/` - Redirect to original URL
- `/expired/<short_url>/` - Expired URL page

### Authentication
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout

### User Dashboard
- `/dashboard/` - User dashboard with statistics
- `/my-urls/` - List user's URLs
- `/profile/` - User profile

### URL Management
- `/customize/<int:url_id>/` - Customize URL settings
- `/preview-qr/` - QR code preview (AJAX)
- `/update-slug/<int:pk>/` - Update URL slug (AJAX)
- `/delete-url/<int:pk>/` - Delete URL (AJAX)

### Analytics
- `/analytics/` - Global analytics dashboard

## Key Features

### URL Shortening
- Automatic 6-character slug generation
- Custom slug support
- Click tracking and analytics
- URL expiration dates
- Category-based organization

### QR Code Generation
- Automatic QR code creation for each URL
- Customizable QR code generation
- PNG format with unique filenames

### User Management
- Registration and login system
- User-specific URL management
- Dashboard with personal statistics
- Profile management

### Analytics
- Click tracking for each URL
- Category-based statistics
- Global analytics dashboard
- Search functionality

### AJAX Features
- Real-time QR code preview
- Inline slug editing
- URL deletion without page refresh
- Dynamic updates

## Technologies Used

### Backend
- **Django 5.2.5** - Web framework
- **Python 3.12** - Programming language
- **SQLite3** - Database

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Styling
- **JavaScript (ES6+)** - Interactive features
- **Bootstrap** - Responsive design

### Libraries
- **qrcode 8.2** - QR code generation
- **Pillow 11.3.0** - Image processing
- **asgiref 3.9.1** - ASGI support
- **sqlparse 0.5.3** - SQL parsing
- **tzdata 2025.2** - Timezone data

## Security Features

- CSRF protection enabled
- User authentication required for sensitive operations
- URL ownership verification
- Input validation and sanitization
- Secure password handling

## Responsive Design

- Mobile-friendly interface
- Responsive layout for all screen sizes
- Touch-friendly interactions
- Optimized for mobile devices

## Deployment

### Development
```bash
python manage.py runserver
```

### Production
- Set `DEBUG = False` in settings.py
- Configure allowed hosts
- Set up static file serving
- Configure database for production use

## Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
- URL shortening functionality
- User authentication
- QR code generation
- Analytics tracking
- URL expiration

## Performance

- Efficient database queries
- Optimized image processing
- Caching support
- Scalable architecture

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support, email support@shortenit.com or create an issue in the repository.

---

**Built with using Django**
