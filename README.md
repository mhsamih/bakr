# CMMS Platform - Comprehensive Preventive Maintenance Management System

A complete, dynamic, and professional **Preventive Maintenance Web Application** built from scratch for general-purpose facility maintenance. Designed to be applicable to any facility: hospitals, schools, hotels, factories, residential complexes, and government buildings.

## 🚀 Features

### Core Modules
- **Equipment Management** - Track equipment with detailed specifications, locations, and PM schedules
- **Work Order Management** - Create, assign, and track work orders with interactive checklists
- **Preventive Maintenance** - Auto-generate PM tasks based on configurable schedules (Daily/Weekly/Monthly/Quarterly/Annual)
- **Checklist System** - Dynamic checklist builder with equipment-specific templates (Chiller: 15 items, AHU: 14 items, Split AC: 11 items)
- **Technician Management** - Track skills, workload, performance metrics, and time tracking
- **Inventory Management** - Manage spare parts with stock alerts and consumption tracking
- **Dashboard & Analytics** - KPI cards, dynamic calendar, overdue alerts, completion rates
- **Notifications** - Real-time alerts via WhatsApp, email, and in-app notifications
- **PDF Reports** - Generate printable work order reports with three signature fields

### User Roles & Permissions
| Role | Permissions |
|------|-------------|
| **Super Admin** | Full access + user management + settings |
| **Maintenance Engineer** | Dashboard + reports + assign tasks + print PDF + view all |
| **Technician** | View own tasks + update status + write problems + attach photos |
| **Viewer** | Read-only access, no editing |

### Technical Features
- JWT Authentication with refresh tokens (8-hour expiry)
- Role-based access control (RBAC)
- Real-time updates via WebSockets
- REST API with Swagger documentation
- PostgreSQL database with Prisma ORM
- Redis caching
- Docker & Docker Compose support
- Multi-language support (English + Arabic RTL)
- Dark/Light mode themes
- Responsive PWA design
- Offline-first mobile support for field technicians

## 📁 Project Structure

```
cmms-platform/
├── apps/
│   ├── api/              # NestJS backend
│   │   └── prisma/
│   │       ├── schema.prisma
│   │       └── seeds/
│   │           └── seed.ts
│   └── web/              # Next.js frontend
├── modules/
│   ├── auth/             # Authentication module
│   ├── users/            # User management
│   ├── assets/           # Asset management
│   ├── equipment/        # Equipment management (NEW)
│   ├── work-orders/      # Work order management
│   ├── preventive-maintenance/  # PM scheduling
│   ├── inventory/        # Spare parts inventory
│   ├── notifications/    # Notification system (WhatsApp, Email)
│   ├── dashboard/        # Analytics dashboard
│   └── reports/          # PDF report generation
├── core/
│   ├── database/         # Database configuration
│   └── security/         # Security middleware
├── shared/
│   ├── config/           # Shared configurations
│   ├── constants/        # Application constants
│   ├── types/            # TypeScript types
│   └── utils/            # Utility functions
└── packages/
    ├── ui/               # Shared UI components
    └── common/           # Common utilities
```

## 🛠️ Tech Stack

### Frontend
- Next.js 14
- React 18
- TypeScript
- TailwindCSS
- shadcn/ui components
- Framer Motion
- React Query (TanStack Query)
- Zustand (state management)
- Recharts / Chart.js
- jsPDF (PDF generation)

### Backend
- NestJS
- PostgreSQL
- Prisma ORM
- Redis
- Socket.io (WebSockets)
- JWT authentication
- bcrypt password hashing

### Infrastructure
- Docker & Docker Compose
- Kubernetes-ready
- CI/CD ready

## 🚦 Getting Started

### Prerequisites
- Node.js >= 18
- npm >= 9
- Docker & Docker Compose (optional)
- PostgreSQL 15+ (if not using Docker)
- Redis 7+ (if not using Docker)

### Quick Start with Docker

```bash
# Clone the repository
git clone <repository-url>
cd cmms-platform

# Copy environment file
cp .env.example .env

# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec api npm run db:migrate

# Seed database with sample data
docker-compose exec api npm run db:seed
```

### Manual Setup

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Start databases (PostgreSQL & Redis)
docker-compose up -d postgres redis

# Run database migrations
npm run db:migrate

# Seed database
npm run db:seed

# Start development servers
npm run dev
```

Access the applications:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **API Documentation**: http://localhost:3001/docs

## 📊 Database Schema

The comprehensive database includes tables for:
- **Users & Authentication** - With roles, signatures, technician profiles
- **Departments & Facilities** - Hierarchical organization
- **Buildings, Floors, Rooms** - Location management
- **Equipment** - Detailed equipment tracking with PM schedules
- **Asset Categories** - HVAC, Electrical, Mechanical, Civil, Communication
- **Work Orders** - With checklists, spare parts, attachments, signatures
- **Checklist Templates** - Equipment-specific templates (Chiller, AHU, Split AC, etc.)
- **PM Schedules** - Recurring maintenance schedules
- **Inventory Items & Warehouses** - Spare parts management
- **Suppliers** - Vendor management
- **Notifications** - In-app, WhatsApp, Email
- **Audit Logs** - Complete activity tracking
- **Import Logs** - Excel import tracking

## 🔐 Default Login Credentials

After seeding the database:

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@cmms.local | Admin123! |
| Maintenance Engineer | engineer@cmms.local | Admin123! |
| Technician (HVAC) | tech1@cmms.local | Admin123! |
| Technician (Electrical) | tech2@cmms.local | Admin123! |
| Viewer | viewer@cmms.local | Admin123! |

## 🌍 Language Support

The platform supports:
- **English (LTR)**
- **Arabic (RTL)** - Full bilingual support

Language can be switched from user settings. All content including:
- Equipment names and descriptions
- Work order titles
- Checklist items
- Notifications
- Reports

## 📱 Mobile Support

The frontend is a Progressive Web App (PWA) that:
- Works offline (offline-first for field technicians)
- Supports background sync
- Has native-like experience
- Supports QR code scanning for equipment
- Simplified technician mobile view

## 📋 Sample Data Included

The seed script creates:
- **5 Users** (1 Admin, 1 Engineer, 2 Technicians, 1 Viewer)
- **4 Departments** (HVAC, Electrical, Mechanical, Civil)
- **1 Facility** (Hospital Complex - customizable)
- **2 Buildings** with floors and rooms
- **10 Equipment Items** across multiple categories:
  - 2 Chillers (Quarterly PM - 15 checklist items)
  - 1 AHU (Monthly PM - 14 checklist items)
  - 2 Split AC Units (Monthly PM - 11 checklist items)
  - 1 Transformer (Annual PM)
  - 1 Water Pump (Monthly PM)
  - 1 Exhaust Fan (Monthly PM)
  - 1 Boiler (Monthly PM)
  - 1 MCC Panel (Monthly PM)
- **3 Checklist Templates** (Chiller, AHU, Split AC)
- **4 PM Schedules**
- **4 Work Orders** (various statuses)
- **5 Inventory Items**

## 🔔 WhatsApp Notification System

Integrated with CallMeBot (free) or Twilio (paid):

| Event | Recipient |
|-------|-----------|
| New task assigned | Worker |
| PM due in 3 days | Worker + Engineer |
| Task overdue | Engineer + Admin |
| Task completed | Engineer |
| Problem reported | Engineer (immediate) |
| Warranty expiring (30 days) | Admin |
| Equipment breakdown | Engineer + Admin |

## 📄 PDF Report Generation

Generate printable PDF reports:
1. **Work Order Report** - Equipment details, checklist, spare parts, signatures
2. **Monthly Summary Report** - Completion rates, overdue tasks, worker performance
3. **Equipment History Report** - Full maintenance history
4. **Worker Performance Report** - Tasks completed, average time, on-time rate

## 📅 PM Schedule Examples

Based on the original Excel sheets:

### Chiller (Quarterly PM - 15 items)
1. Clean condenser coil with water pressure
2. Check fans and fan guards
3. Check fan motor bearings
... (15 total items)

### AHU (Monthly PM - 14 items)
1. Clean evaporator coil with water pressure
2. Clean/replace air filter
3. Check blower motor
... (14 total items)

### Split AC (Monthly PM - 11 items)
1. Clean condenser coil with water pressure
2. Clean indoor unit completely
3. Check fan motor bearings
... (11 total items)

## 🔮 Future Extensibility

The architecture supports future modules:
- Excel Import (48 sheets from original PPM program)
- IoT Sensor Integration
- AI Predictive Maintenance
- Vendor Portal
- ERP Integrations
- Multi-tenant SaaS
- Hijri Calendar display

## 📝 API Documentation

Once the API is running, visit http://localhost:3001/docs for interactive Swagger documentation.

## 🧪 Testing

```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e
```

## 📄 License

MIT License - see LICENSE file for details

## 👥 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

---

**Built with ❤️ for facility maintenance professionals**
