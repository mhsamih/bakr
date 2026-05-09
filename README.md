# CMMS Platform - Modern Maintenance Management System

A comprehensive, modular Computerized Maintenance Management System (CMMS) built for general maintenance operations. Designed to be production-ready, scalable, and easily extensible for future requirements.

## 🚀 Features

### Core Modules
- **Asset Management** - Track assets with QR codes, hierarchical organization, maintenance history
- **Work Order Management** - Create, assign, and track work orders with real-time updates
- **Preventive Maintenance** - Schedule recurring maintenance tasks automatically
- **Inventory Management** - Manage spare parts with stock alerts and consumption tracking
- **Technician Management** - Track skills, workload, and performance metrics
- **Dashboard & Analytics** - MTTR, MTBF, compliance tracking, and more
- **Notifications** - Real-time alerts via WebSocket, email, and push notifications

### Technical Features
- JWT Authentication with refresh tokens
- Role-based access control (Admin, Manager, Supervisor, Technician, Requester)
- Real-time updates via WebSockets
- REST API with Swagger documentation
- PostgreSQL database with Prisma ORM
- Redis caching
- Docker & Docker Compose support
- Kubernetes-ready architecture
- Multi-language support (English + Arabic RTL)
- Dark/Light mode themes
- Responsive PWA design
- Offline-first mobile support

## 📁 Project Structure

```
cmms-platform/
├── apps/
│   ├── api/              # NestJS backend
│   └── web/              # Next.js frontend
├── modules/
│   ├── auth/             # Authentication module
│   ├── users/            # User management
│   ├── assets/           # Asset management
│   ├── work-orders/      # Work order management
│   ├── preventive-maintenance/  # PM scheduling
│   ├── inventory/        # Spare parts inventory
│   ├── notifications/    # Notification system
│   └── dashboard/        # Analytics dashboard
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
- Recharts

### Backend
- NestJS
- PostgreSQL
- Prisma ORM
- Redis
- Socket.io (WebSockets)
- JWT authentication

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
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001
- API Documentation: http://localhost:3001/docs

## 📊 Database Schema

The database includes tables for:
- Users & Authentication
- Assets & Asset Categories
- Buildings, Floors, Rooms
- Work Orders
- Preventive Maintenance Schedules
- Inventory Items & Warehouses
- Suppliers
- Notifications
- Audit Logs

## 🔐 Default Admin Account

After seeding the database:
- Email: admin@cmms.local
- Password: Admin123!

## 🌍 Language Support

The platform supports:
- English (LTR)
- Arabic (RTL)

Language can be switched from the user settings.

## 📱 Mobile Support

The frontend is a Progressive Web App (PWA) that:
- Works offline
- Supports background sync
- Has native-like experience
- Supports QR code scanning

## 🔮 Future Extensibility

The architecture is designed to support future modules:
- Healthcare CMMS
- Biomedical Engineering
- IoT Sensor Integration
- AI Predictive Maintenance
- Vendor Portal
- ERP Integrations
- Multi-tenant SaaS
- Compliance Systems

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
