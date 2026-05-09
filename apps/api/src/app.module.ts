import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { ScheduleModule } from '@nestjs/schedule';
import { ThrottlerModule } from '@nestjs/throttler';

// Core modules
import { DatabaseModule } from '../../core/database/database.module';
import { SecurityModule } from '../../core/security/security.module';

// Shared modules
import { AuthModule } from '../../modules/auth/auth.module';
import { UsersModule } from '../../modules/users/users.module';
import { AssetsModule } from '../../modules/assets/assets.module';
import { WorkOrdersModule } from '../../modules/work-orders/work-orders.module';
import { PreventiveMaintenanceModule } from '../../modules/preventive-maintenance/preventive-maintenance.module';
import { InventoryModule } from '../../modules/inventory/inventory.module';
import { NotificationsModule } from '../../modules/notifications/notifications.module';
import { DashboardModule } from '../../modules/dashboard/dashboard.module';

@Module({
  imports: [
    // Configuration
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),

    // Cron jobs for preventive maintenance
    ScheduleModule.forRoot(),

    // Rate limiting
    ThrottlerModule.forRoot([
      {
        ttl: 60000,
        limit: 100,
      },
    ]),

    // Core modules
    DatabaseModule,
    SecurityModule,

    // Feature modules
    AuthModule,
    UsersModule,
    AssetsModule,
    WorkOrdersModule,
    PreventiveMaintenanceModule,
    InventoryModule,
    NotificationsModule,
    DashboardModule,
  ],
})
export class AppModule {}
