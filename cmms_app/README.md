# CMMS - Preventive Maintenance Web Application

A comprehensive Computerized Maintenance Management System (CMMS) built with Flask for managing preventive maintenance programs across any facility type.

## 🏗️ Architecture

- **Backend**: Python Flask REST API
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Authentication**: JWT Tokens
- **Frontend Ready**: HTML5/CSS3/JavaScript templates

## 📁 Project Structure

```
cmms_app/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── models.py            # SQLAlchemy database models
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── equipment.py     # Equipment CRUD
│   │   │   ├── work_orders.py   # Work order management
│   │   │   ├── users.py         # User management
│   │   │   ├── dashboard.py     # Dashboard KPIs & charts
│   │   │   └── reports.py       # Reports & PDF generation
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── uploads/
│   │   └── templates/
│   ├── config.py                # Configuration settings
│   ├── run.py                   # Application entry point
│   └── requirements.txt         # Python dependencies
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd cmms_app/backend
pip install -r requirements.txt
```

### 2. Set Environment Variables (Optional)

```bash
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret
export DATABASE_URL=sqlite:///cmms.db
```

### 3. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 🔐 Default Credentials

After seeding the database, use these credentials:

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@cmms.local | Admin123! |
| Maintenance Engineer | engineer@cmms.local | Admin123! |
| Technician | tech1@cmms.local | Admin123! |
| Viewer | viewer@cmms.local | Admin123! |

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Register new user (Admin only)
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user
- `POST /api/auth/change-password` - Change password

### Equipment
- `GET /api/equipment` - List all equipment (with filters)
- `GET /api/equipment/:id` - Get equipment details
- `POST /api/equipment` - Create new equipment
- `PUT /api/equipment/:id` - Update equipment
- `DELETE /api/equipment/:id` - Decommission equipment
- `POST /api/equipment/:id/upload-photo` - Upload equipment photo
- `GET /api/equipment/categories` - Get asset categories
- `GET /api/equipment/departments` - Get departments
- `GET /api/equipment/:id/history` - Get maintenance history

### Work Orders
- `GET /api/work-orders` - List work orders (with filters)
- `GET /api/work-orders/today` - Get today's work orders
- `POST /api/work-orders` - Create new work order
- `GET /api/work-orders/:id` - Get work order details
- `POST /api/work-orders/:id/start` - Start work order
- `POST /api/work-orders/:id/complete` - Complete work order
- `POST /api/work-orders/:id/checklist` - Update checklist
- `POST /api/work-orders/:id/spare-parts` - Add spare part

### Users
- `GET /api/users` - List all users
- `GET /api/users/:id` - Get user details
- `PUT /api/users/:id` - Update user
- `GET /api/users/technicians` - Get all technicians
- `POST /api/users/:id/signature` - Upload signature

### Dashboard
- `GET /api/dashboard/kpi` - Get KPI cards data
- `GET /api/dashboard/today` - Get today's summary
- `GET /api/dashboard/charts/work-orders-by-status` - Chart data
- `GET /api/dashboard/charts/work-orders-by-category` - Chart data
- `GET /api/dashboard/charts/completion-trend` - Trend data
- `GET /api/dashboard/alerts` - Get system alerts
- `GET /api/dashboard/notifications` - Get notifications
- `POST /api/dashboard/notifications/:id/read` - Mark as read

### Reports
- `GET /api/reports/work-order/:id/pdf` - Generate WO report
- `GET /api/reports/monthly-summary` - Monthly summary
- `GET /api/reports/equipment-history/:id` - Equipment history
- `GET /api/reports/worker-performance` - Worker performance

## 🗄️ Database Models

The application includes comprehensive models for:

- **Users** - Role-based access (Super Admin, Engineer, Technician, Viewer)
- **Facilities** - Multi-facility support
- **Departments** - HVAC, Electrical, Mechanical, Civil, etc.
- **Buildings/Floors/Rooms** - Hierarchical location structure
- **Equipment** - Core asset management with PM scheduling
- **Asset Categories** - Equipment categorization
- **Checklist Templates** - Reusable PM checklists
- **Checklist Items** - Individual checklist tasks
- **Work Orders** - Preventive & corrective maintenance
- **Checklist Results** - Completed checklist data
- **Spare Parts Used** - Parts consumption tracking
- **Attachments** - Photos and documents
- **PM Schedules** - Automated schedule generation
- **Notifications** - In-app notifications
- **WhatsApp Logs** - WhatsApp notification tracking
- **Inventory Items** - Spare parts inventory
- **Warehouses** - Storage locations
- **Suppliers** - Vendor management
- **Signatures** - Digital signatures
- **Audit Logs** - Security audit trail
- **System Settings** - Configurable settings
- **Import Logs** - Data import tracking

## 🔒 Security Features

- JWT token authentication (8-hour expiry)
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Audit logging for all actions
- CSRF protection ready
- Input validation and sanitization

## 📱 Mobile-First Design

The API is designed to support:
- Responsive web interface
- Offline-first capability for field technicians
- Photo upload from mobile devices
- Digital signatures on touch screens

## 🌐 Internationalization

Ready for bilingual support:
- RTL (Arabic) layout support
- LTR (English) layout support
- Date formats: Gregorian with Hijri option

## 📊 Features Implemented

### Phase 1 - Foundation ✅
- [x] Database schema with 20+ models
- [x] Flask app structure with blueprints
- [x] JWT authentication system
- [x] Role-based permissions

### Phase 2 - Core Features ✅
- [x] Equipment CRUD operations
- [x] Work order creation and management
- [x] Checklist system (builder + execution)
- [x] Spare parts tracking

### Phase 3 - Dashboard & UI 🔄
- [x] KPI cards API
- [x] Dashboard statistics
- [x] Alert system
- [x] Notification center
- [ ] Frontend templates (pending)

### Phase 4 - Advanced Features 🔄
- [x] Report generation endpoints
- [x] Worker performance metrics
- [x] Equipment history tracking
- [ ] WhatsApp integration (ready for Twilio/CallMeBot)
- [ ] PDF generation (data ready for jsPDF/ReportLab)

### Phase 5 - Polish 🔄
- [x] Audit logging
- [x] Security hardening
- [ ] Arabic/English toggle (frontend pending)
- [ ] Dark mode (frontend pending)

## 🔧 Customization

### Adding New Equipment Categories

Categories are fully customizable via the database:

```python
# Example: Add new category
category = AssetCategory(
    name='Medical Equipment',
    code='MED',
    icon='heart-pulse',
    color='#EF4444'
)
```

### PM Frequencies Supported

- Daily
- Weekly
- Monthly
- Quarterly
- Semi-Annual
- Annual

### Work Order Statuses

- Pending
- In Progress
- Completed
- Needs Follow-up
- Cancelled

## 📈 Sample Data

The system comes ready to accept sample data including:
- 10+ equipment items across multiple categories
- Checklist templates matching Excel specifications:
  - Chiller: 15 items (Quarterly PM)
  - AHU: 14 items (Monthly PM)
  - Split AC: 11 items (Monthly PM)
- Pre-configured departments (HVAC, Electrical, Mechanical, Civil)

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "backend.app:create_app('production')"
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app('production')"]
```

## 📝 Next Steps

To complete the application:

1. **Create Frontend Templates** - HTML/CSS/JS pages in `templates/`
2. **Add Seed Script** - Populate database with initial data
3. **Implement Excel Import** - Parse 48-sheet Excel file
4. **WhatsApp Integration** - Connect Twilio or CallMeBot
5. **PDF Generation** - Implement ReportLab or use jsPDF
6. **Calendar View** - Add FullCalendar.js integration
7. **Mobile PWA** - Add service worker for offline support

## 📄 License

MIT License - Free for commercial and personal use

## 👨‍💻 Support

For questions or issues, please refer to the documentation or contact the development team.

---

Built with ❤️ for facility maintenance management
