'use client';

import { motion } from 'framer-motion';
import { 
  Wrench, 
  Building2, 
  ClipboardCheck, 
  Package, 
  Users, 
  BarChart3,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';

const features = [
  {
    icon: Building2,
    title: 'Asset Management',
    description: 'Track and manage all your assets with QR codes, maintenance history, and hierarchical organization.',
  },
  {
    icon: ClipboardCheck,
    title: 'Work Orders',
    description: 'Create, assign, and track work orders with real-time updates and digital signatures.',
  },
  {
    icon: Wrench,
    title: 'Preventive Maintenance',
    description: 'Schedule recurring maintenance tasks automatically to reduce downtime.',
  },
  {
    icon: Package,
    title: 'Inventory Management',
    description: 'Manage spare parts inventory with stock alerts and consumption tracking.',
  },
  {
    icon: Users,
    title: 'Technician Management',
    description: 'Track technician skills, workload, and performance metrics.',
  },
  {
    icon: BarChart3,
    title: 'Analytics & Reports',
    description: 'Get insights with MTTR, MTBF, compliance tracking, and more.',
  },
];

const benefits = [
  'Reduce equipment downtime by up to 50%',
  'Improve technician productivity',
  'Extend asset lifespan',
  'Lower maintenance costs',
  'Real-time visibility into operations',
  'Mobile-friendly for field technicians',
];

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Wrench className="h-6 w-6 text-primary" />
            <span className="text-xl font-bold">CMMS Platform</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition">Features</a>
            <a href="#benefits" className="text-sm text-muted-foreground hover:text-foreground transition">Benefits</a>
            <button className="bg-primary text-primary-foreground px-4 py-2 rounded-md text-sm font-medium hover:bg-primary/90 transition">
              Get Started
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Modern Maintenance<br />
            <span className="text-primary">Management System</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Streamline your maintenance operations with our comprehensive CMMS platform. 
            Track assets, manage work orders, and reduce downtime—all in one place.
          </p>
          <div className="flex gap-4 justify-center">
            <button className="bg-primary text-primary-foreground px-8 py-3 rounded-md font-medium hover:bg-primary/90 transition flex items-center gap-2">
              Start Free Trial
              <ArrowRight className="h-4 w-4" />
            </button>
            <button className="border border-input bg-background px-8 py-3 rounded-md font-medium hover:bg-accent transition">
              Watch Demo
            </button>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section id="features" className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">Everything You Need</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-card border rounded-lg p-6 hover:shadow-lg transition"
            >
              <feature.icon className="h-12 w-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="container mx-auto px-4 py-20 bg-muted/50 rounded-3xl">
        <h2 className="text-3xl font-bold text-center mb-12">Why Choose CMMS Platform?</h2>
        <div className="max-w-3xl mx-auto grid md:grid-cols-2 gap-4">
          {benefits.map((benefit, index) => (
            <motion.div
              key={benefit}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center gap-3"
            >
              <CheckCircle2 className="h-5 w-5 text-green-500 flex-shrink-0" />
              <span>{benefit}</span>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t mt-20 py-8">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p>&copy; 2024 CMMS Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
