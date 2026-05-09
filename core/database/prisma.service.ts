import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }

  // Enable transaction support
  async transaction<T>(fn: (tx: Omit<PrismaService, '$connect' | '$disconnect' | '$on' | '$transaction' | '$use'>) => Promise<T>): Promise<T> {
    return this.$transaction(fn);
  }
}
