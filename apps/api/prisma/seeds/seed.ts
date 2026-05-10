import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seeding...');

  // ============================================
  // 1. CREATE USERS
  // ============================================
  const hashedPassword = await bcrypt.hash('Admin123!', 10);

  const superAdmin = await prisma.user.upsert({
    where: { email: 'admin@cmms.local' },
    update: {},
    create: {
      email: 'admin@cmms.local',
      password: hashedPassword,
      firstName: 'System',
      lastName: 'Administrator',
      phone: '+966501234567',
      whatsapp: '+966501234567',
      role: 'SUPER_ADMIN',
      department: 'Administration',
      isActive: true,
      emailVerified: true,
    },
  });

  const engineer = await prisma.user.upsert({
    where: { email: 'engineer@cmms.local' },
    update: {},
    create: {
      email: 'engineer@cmms.local',
      password: hashedPassword,
      firstName: 'Ahmed',
      lastName: 'Al-Mahmoud',
      phone: '+966502345678',
      whatsapp: '+966502345678',
      role: 'MAINTENANCE_ENGINEER',
      department: 'Maintenance',
      specialization: 'HVAC',
      isActive: true,
      emailVerified: true,
    },
  });

  const technician1 = await prisma.user.upsert({
    where: { email: 'tech1@cmms.local' },
    update: {},
    create: {
      email: 'tech1@cmms.local',
      password: hashedPassword,
      firstName: 'Mohammed',
      lastName: 'Hassan',
      phone: '+966503456789',
      whatsapp: '+966503456789',
      role: 'TECHNICIAN',
      department: 'HVAC',
      specialization: 'HVAC',
      isActive: true,
      emailVerified: true,
    },
  });

  const technician2 = await prisma.user.upsert({
    where: { email: 'tech2@cmms.local' },
    update: {},
    create: {
      email: 'tech2@cmms.local',
      password: hashedPassword,
      firstName: 'Khalid',
      lastName: 'Ibrahim',
      phone: '+966504567890',
      whatsapp: '+966504567890',
      role: 'TECHNICIAN',
      department: 'Electrical',
      specialization: 'Electrical',
      isActive: true,
      emailVerified: true,
    },
  });

  const viewer = await prisma.user.upsert({
    where: { email: 'viewer@cmms.local' },
    update: {},
    create: {
      email: 'viewer@cmms.local',
      password: hashedPassword,
      firstName: 'Sarah',
      lastName: 'Ahmed',
      phone: '+966505678901',
      role: 'VIEWER',
      department: 'Administration',
      isActive: true,
      emailVerified: true,
    },
  });

  console.log('✅ Users created');

  // ============================================
  // 2. CREATE TECHNICIAN PROFILES
  // ============================================
  await prisma.technicianProfile.createMany({
    data: [
      {
        userId: technician1.id,
        employeeId: 'EMP-001',
        skills: ['Chiller Maintenance', 'AHU Repair', 'Refrigerant Handling'],
        specializations: ['HVAC'],
        certifications: ['HVAC Level 3', 'Safety Certified'],
        maxWorkload: 10,
        hireDate: new Date('2020-01-15'),
      },
      {
        userId: technician2.id,
        employeeId: 'EMP-002',
        skills: ['Electrical Panels', 'Motor Control', 'Lighting Systems'],
        specializations: ['Electrical'],
        certifications: ['Electrician License', 'High Voltage Certified'],
        maxWorkload: 10,
        hireDate: new Date('2019-06-01'),
      },
    ],
  });

  console.log('✅ Technician profiles created');

  // ============================================
  // 3. CREATE DEPARTMENTS
  // ============================================
  const hvacDept = await prisma.department.create({
    data: {
      name: 'HVAC',
      nameAr: 'التكييف والتهوية',
      code: 'HVAC',
      description: 'Heating, Ventilation, and Air Conditioning',
    },
  });

  const electricalDept = await prisma.department.create({
    data: {
      name: 'Electrical',
      nameAr: 'كهرباء',
      code: 'ELEC',
      description: 'Electrical Systems and Power Distribution',
    },
  });

  const mechanicalDept = await prisma.department.create({
    data: {
      name: 'Mechanical',
      nameAr: 'ميكانيكا',
      code: 'MECH',
      description: 'Mechanical Systems and Plumbing',
    },
  });

  const civilDept = await prisma.department.create({
    data: {
      name: 'Civil Works',
      nameAr: 'أعمال مدنية',
      code: 'CIVIL',
      description: 'Civil Works and Building Maintenance',
    },
  });

  console.log('✅ Departments created');

  // ============================================
  // 4. CREATE FACILITY
  // ============================================
  const facility = await prisma.facility.create({
    data: {
      name: 'Main Hospital Complex',
      nameAr: 'المجمع الصحي الرئيسي',
      code: 'FAC-001',
      type: 'HOSPITAL',
      address: 'King Fahd Road',
      city: 'Riyadh',
      country: 'Saudi Arabia',
      departmentId: hvacDept.id,
    },
  });

  console.log('✅ Facility created');

  // ============================================
  // 5. CREATE BUILDINGS, FLOORS, ROOMS
  // ============================================
  const building1 = await prisma.building.create({
    data: {
      name: 'Main Building',
      nameAr: 'المبنى الرئيسي',
      code: 'BLD-001',
      facilityId: facility.id,
      address: 'Block A',
    },
  });

  const building2 = await prisma.building.create({
    data: {
      name: 'Outpatient Clinic',
      nameAr: 'عيادة المرضى الخارجيين',
      code: 'BLD-002',
      facilityId: facility.id,
    },
  });

  const floor1 = await prisma.floor.create({
    data: {
      buildingId: building1.id,
      name: 'Ground Floor',
      nameAr: 'الطابق الأرضي',
      level: 0,
    },
  });

  const floor2 = await prisma.floor.create({
    data: {
      buildingId: building1.id,
      name: 'First Floor',
      nameAr: 'الطابق الأول',
      level: 1,
    },
  });

  const room1 = await prisma.room.create({
    data: {
      floorId: floor1.id,
      name: 'Mechanical Room A',
      nameAr: 'غرفة ميكانيكية أ',
      code: 'RM-001',
      type: 'Mechanical Room',
    },
  });

  const room2 = await prisma.room.create({
    data: {
      floorId: floor2.id,
      name: 'AHU Room 1',
      nameAr: 'غرفة وحدة مناولة الهواء 1',
      code: 'RM-002',
      type: 'Equipment Room',
    },
  });

  console.log('✅ Buildings, floors, and rooms created');

  // ============================================
  // 6. CREATE ASSET CATEGORIES
  // ============================================
  const chillerCategory = await prisma.assetCategory.create({
    data: {
      name: 'Chiller',
      nameAr: 'مبرد',
      code: 'HVAC-CHILLER',
      description: 'Central Water Chillers',
      icon: 'snowflake',
      color: '#3B82F6',
    },
  });

  const ahuCategory = await prisma.assetCategory.create({
    data: {
      name: 'AHU',
      nameAr: 'وحدة مناولة الهواء',
      code: 'HVAC-AHU',
      description: 'Air Handling Units',
      icon: 'wind',
      color: '#10B981',
    },
  });

  const splitAcCategory = await prisma.assetCategory.create({
    data: {
      name: 'Split AC',
      nameAr: 'مكيف منفصل',
      code: 'HVAC-SPLIT',
      description: 'Split Air Conditioners',
      icon: 'thermometer',
      color: '#F59E0B',
    },
  });

  const transformerCategory = await prisma.assetCategory.create({
    data: {
      name: 'Transformer',
      nameAr: 'محول كهربائي',
      code: 'ELEC-TRANS',
      description: 'Electrical Transformers',
      icon: 'zap',
      color: '#EF4444',
    },
  });

  const pumpCategory = await prisma.assetCategory.create({
    data: {
      name: 'Water Pump',
      nameAr: 'مضخة مياه',
      code: 'MECH-PUMP',
      description: 'Water Pumps',
      icon: 'droplet',
      color: '#06B6D4',
    },
  });

  console.log('✅ Asset categories created');

  // ============================================
  // 7. CREATE EQUIPMENT (Sample from Excel sheets)
  // ============================================
  
  // Chiller Equipment (Quarterly PM - 15 checklist items)
  const chiller1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-001',
      name: 'Chiller 1-A',
      nameAr: 'مبرد 1-أ',
      categoryId: chillerCategory.id,
      model: 'York YCAL 0147',
      serialNumber: 'YL147-2020-001',
      manufacturer: 'Johnson Controls York',
      brand: 'York',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor1.id,
      roomId: room1.id,
      subLocation: 'Mechanical Room A - Bay 1',
      purchaseDate: new Date('2020-03-15'),
      warrantyExpiration: new Date('2025-03-15'),
      assetTag: 'CHL-001',
      pmFrequency: 'QUARTERLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-01-15'),
      nextPmDate: new Date('2024-04-15'),
      pmDuration: 180,
      assignedToId: technician1.id,
      status: 'ACTIVE',
      priority: 'HIGH',
      description: 'Central water chiller for main building cooling',
      specifications: {
        capacity: '150 TR',
        voltage: '380V',
        phases: '3 Phase',
        refrigerant: 'R-134a',
        powerConsumption: '125 kW',
      },
    },
  });

  const chiller2 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-002',
      name: 'Chiller 2-B',
      nameAr: 'مبرد 2-ب',
      categoryId: chillerCategory.id,
      model: 'Trane CGAM 175',
      serialNumber: 'TR175-2019-002',
      manufacturer: 'Trane',
      brand: 'Trane',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor1.id,
      subLocation: 'Mechanical Room B',
      purchaseDate: new Date('2019-06-01'),
      warrantyExpiration: new Date('2024-06-01'), // Expiring soon
      assetTag: 'CHL-002',
      pmFrequency: 'QUARTERLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-01-10'),
      nextPmDate: new Date('2024-04-10'),
      pmDuration: 180,
      assignedToId: technician1.id,
      status: 'WARRANTY_EXPIRING',
      priority: 'HIGH',
    },
  });

  // AHU Equipment (Monthly PM - 14 checklist items)
  const ahu1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-003',
      name: 'AHU-1 Floor 1',
      nameAr: 'وحدة مناولة الهواء-1 طابق 1',
      categoryId: ahuCategory.id,
      model: 'Carrier 39M',
      serialNumber: 'CAR39M-2021-003',
      manufacturer: 'Carrier',
      brand: 'Carrier',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor2.id,
      roomId: room2.id,
      subLocation: 'North Wing',
      purchaseDate: new Date('2021-02-01'),
      warrantyExpiration: new Date('2026-02-01'),
      assetTag: 'AHU-001',
      pmFrequency: 'MONTHLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-02-01'),
      nextPmDate: new Date('2024-03-01'),
      pmDuration: 90,
      assignedToId: technician1.id,
      status: 'ACTIVE',
      priority: 'MEDIUM',
    },
  });

  // Split AC Units (Monthly PM - 11 checklist items)
  const splitAc1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-004',
      name: 'Split AC - Office 101',
      nameAr: 'مكيف منفصل - مكتب 101',
      categoryId: splitAcCategory.id,
      model: 'LG Dual Inverter',
      serialNumber: 'LG-DI-2022-004',
      manufacturer: 'LG',
      brand: 'LG',
      facilityId: facility.id,
      buildingId: building2.id,
      subLocation: 'Office 101',
      purchaseDate: new Date('2022-05-15'),
      warrantyExpiration: new Date('2027-05-15'),
      assetTag: 'SPL-001',
      pmFrequency: 'MONTHLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-02-15'),
      nextPmDate: new Date('2024-03-15'),
      pmDuration: 45,
      assignedToId: technician1.id,
      status: 'ACTIVE',
      priority: 'LOW',
    },
  });

  const splitAc2 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-005',
      name: 'Split AC - Conference Room',
      nameAr: 'مكيف منفصل - غرفة الاجتماعات',
      categoryId: splitAcCategory.id,
      model: 'Daikin FTXS35',
      serialNumber: 'DAI-FTX-2021-005',
      manufacturer: 'Daikin',
      brand: 'Daikin',
      facilityId: facility.id,
      buildingId: building2.id,
      subLocation: 'Conference Room A',
      purchaseDate: new Date('2021-08-20'),
      warrantyExpiration: new Date('2026-08-20'),
      assetTag: 'SPL-002',
      pmFrequency: 'MONTHLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-02-10'),
      nextPmDate: new Date('2024-03-10'),
      pmDuration: 45,
      assignedToId: technician1.id,
      status: 'ACTIVE',
      priority: 'MEDIUM',
    },
  });

  // Transformer (Electrical - Annual PM)
  const transformer1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-006',
      name: 'Main Transformer 1000kVA',
      nameAr: 'المحول الرئيسي 1000 كيلو فولت أمبير',
      categoryId: transformerCategory.id,
      model: 'Siemens 1000kVA',
      serialNumber: 'SIE-1000-2018-006',
      manufacturer: 'Siemens',
      brand: 'Siemens',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor1.id,
      subLocation: 'Electrical Room - Main',
      purchaseDate: new Date('2018-01-10'),
      warrantyExpiration: new Date('2023-01-10'), // Expired
      assetTag: 'TRF-001',
      pmFrequency: 'ANNUAL',
      pmInterval: 1,
      lastPmDate: new Date('2024-01-10'),
      nextPmDate: new Date('2025-01-10'),
      pmDuration: 240,
      assignedToId: technician2.id,
      status: 'ACTIVE',
      priority: 'URGENT',
      specifications: {
        capacity: '1000 kVA',
        primaryVoltage: '13.8 kV',
        secondaryVoltage: '380V',
        phases: '3 Phase',
        coolingType: 'Oil Cooled',
      },
    },
  });

  // Water Pump (Mechanical - Monthly PM)
  const pump1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-007',
      name: 'Raw Water Pump 1',
      nameAr: 'مضخة المياه الخام 1',
      categoryId: pumpCategory.id,
      model: 'Grundfos CR 90',
      serialNumber: 'GR-CR90-2020-007',
      manufacturer: 'Grundfos',
      brand: 'Grundfos',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor1.id,
      subLocation: 'Pump Room - Basement',
      purchaseDate: new Date('2020-04-01'),
      warrantyExpiration: new Date('2025-04-01'),
      assetTag: 'PMP-001',
      pmFrequency: 'MONTHLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-02-01'),
      nextPmDate: new Date('2024-03-01'),
      pmDuration: 60,
      assignedToId: technician2.id,
      status: 'ACTIVE',
      priority: 'HIGH',
      specifications: {
        flowRate: '90 m³/h',
        head: '50 m',
        power: '15 kW',
        voltage: '380V',
      },
    },
  });

  // Additional equipment to reach 10+ items
  const exhaustFan1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-008',
      name: 'Exhaust Fan - ICU',
      nameAr: 'مروحة شفط - العناية المركزة',
      categoryId: hvacDept.id ? undefined : undefined,
      model: 'Greenheck CF-18',
      serialNumber: 'GR-CF18-2021-008',
      manufacturer: 'Greenheck',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor2.id,
      subLocation: 'ICU - Room 1',
      purchaseDate: new Date('2021-03-01'),
      warrantyExpiration: new Date('2026-03-01'),
      assetTag: 'EXF-001',
      pmFrequency: 'MONTHLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-02-01'),
      nextPmDate: new Date('2024-03-01'),
      pmDuration: 30,
      status: 'ACTIVE',
      priority: 'HIGH',
    },
  });

  const boiler1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-009',
      name: 'Steam Boiler 500kW',
      nameAr: 'مرجل بخاري 500 كيلو واط',
      categoryId: mechanicalDept.id ? undefined : undefined,
      model: 'Viessmann Vitomax',
      serialNumber: 'VIE-VT-2019-009',
      manufacturer: 'Viessmann',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor1.id,
      subLocation: 'Boiler Room',
      purchaseDate: new Date('2019-09-01'),
      warrantyExpiration: new Date('2024-09-01'),
      assetTag: 'BLR-001',
      pmFrequency: 'MONTHLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-02-01'),
      nextPmDate: new Date('2024-03-01'),
      pmDuration: 120,
      assignedToId: technician2.id,
      status: 'ACTIVE',
      priority: 'URGENT',
    },
  });

  const mccPanel1 = await prisma.equipment.create({
    data: {
      equipmentId: 'EQ-2024-010',
      name: 'MCC Panel - HVAC',
      nameAr: 'لوحة التحكم بالمحركات - التكييف',
      categoryId: electricalDept.id ? undefined : undefined,
      model: 'ABB MNS',
      serialNumber: 'ABB-MNS-2020-010',
      manufacturer: 'ABB',
      facilityId: facility.id,
      buildingId: building1.id,
      floorId: floor1.id,
      subLocation: 'MCC Room - Panel 1',
      purchaseDate: new Date('2020-02-01'),
      warrantyExpiration: new Date('2025-02-01'),
      assetTag: 'MCC-001',
      pmFrequency: 'MONTHLY',
      pmInterval: 1,
      lastPmDate: new Date('2024-02-01'),
      nextPmDate: new Date('2024-03-01'),
      pmDuration: 90,
      assignedToId: technician2.id,
      status: 'ACTIVE',
      priority: 'HIGH',
      specifications: {
        voltage: '380V',
        current: '200A',
        phases: '3 Phase',
      },
    },
  });

  console.log('✅ Equipment created (10 items)');

  // ============================================
  // 8. CREATE CHECKLIST TEMPLATES
  // ============================================
  
  // Chiller Checklist (15 items from Excel)
  const chillerChecklist = await prisma.checklistTemplate.create({
    data: {
      name: 'Chiller Quarterly PM Checklist',
      nameAr: 'قائمة فحص الصيانة الربع سنوية للمبرد',
      description: 'Standard quarterly preventive maintenance for chillers',
      categoryId: chillerCategory.id,
      isDefault: true,
      items: {
        create: [
          { order: 1, description: 'Clean condenser coil with water pressure', descriptionAr: 'تنظيف ملف المكثف بضغط الماء', isRequired: true, expectedAction: 'Clean thoroughly', category: 'Clean' },
          { order: 2, description: 'Check fans and fan guards', descriptionAr: 'فحص المراوح وواقيات المروحة', isRequired: true, expectedAction: 'Inspect for damage', category: 'Check' },
          { order: 3, description: 'Check fan motor bearings', descriptionAr: 'فحص محامل محرك المروحة', isRequired: true, expectedAction: 'Lubricate if needed', category: 'Check' },
          { order: 4, description: 'Check crankcase heater operation', descriptionAr: 'فحص عمل سخان علبة المرفق', isRequired: true, expectedAction: 'Test operation', category: 'Check' },
          { order: 5, description: 'Check water & refrigerant pipework damage', descriptionAr: 'فحص تلف أنابيب المياه والمبردات', isRequired: true, expectedAction: 'Repair if damaged', category: 'Check' },
          { order: 6, description: 'Complete refrigerant leak check', descriptionAr: 'إجراء فحص شامل لتسرب المبردات', isRequired: true, expectedAction: 'Fix leaks', category: 'Check' },
          { order: 7, description: 'Check expansion/solenoid/check valves', descriptionAr: 'فحص صمامات التمدد والملفات والرجوع', isRequired: true, expectedAction: 'Replace if faulty', category: 'Check' },
          { order: 8, description: 'Check HP cut-outs & water flow switch', descriptionAr: 'فحص قواطع الضغط العالي ومفتاح تدفق الماء', isRequired: true, expectedAction: 'Test and calibrate', category: 'Check' },
          { order: 9, description: 'Clean electrical panel, check wiring', descriptionAr: 'تنظيف اللوحة الكهربائية وفحص الأسلاك', isRequired: true, expectedAction: 'Clean and tighten', category: 'Clean' },
          { order: 10, description: 'Check compressor contactors/overloads/breakers', descriptionAr: 'فحص ملامسات الضاغط وقواطع الحمل الزائد', isRequired: true, expectedAction: 'Test operation', category: 'Check' },
          { order: 11, description: 'Check compressor motor protectors', descriptionAr: 'فحص واقيات محرك الضاغط', isRequired: true, expectedAction: 'Verify settings', category: 'Check' },
          { order: 12, description: 'Check thermal insulation on cooler & piping', descriptionAr: 'فحص العزل الحراري على المبرد والأنابيب', isRequired: true, expectedAction: 'Repair insulation', category: 'Check' },
          { order: 13, description: 'Check vibration isolators', descriptionAr: 'فحص عوازل الاهتزاز', isRequired: true, expectedAction: 'Replace if worn', category: 'Check' },
          { order: 14, description: 'Check unit structure for loose bolts/screws', descriptionAr: 'فحص هيكل الوحدة بحثًا عن مسامير مفكوكة', isRequired: true, expectedAction: 'Tighten all fasteners', category: 'Check' },
          { order: 15, description: 'Check rusted/dented/damaged body parts', descriptionAr: 'فحص الأجزاء الصدئة/المقعرة/التالفة من الجسم', isRequired: true, expectedAction: 'Repair or replace', category: 'Check' },
        ],
      },
    },
  });

  // AHU Checklist (14 items from Excel)
  const ahuChecklist = await prisma.checklistTemplate.create({
    data: {
      name: 'AHU Monthly PM Checklist',
      nameAr: 'قائمة فحص الصيانة الشهرية لوحدة مناولة الهواء',
      description: 'Standard monthly preventive maintenance for AHUs',
      categoryId: ahuCategory.id,
      isDefault: true,
      items: {
        create: [
          { order: 1, description: 'Clean evaporator coil with water pressure', descriptionAr: 'تنظيف ملف المبخر بضغط الماء', isRequired: true, category: 'Clean' },
          { order: 2, description: 'Clean/replace air filter', descriptionAr: 'تنظيف/استبدال فلتر الهواء', isRequired: true, category: 'Clean' },
          { order: 3, description: 'Check blower motor', descriptionAr: 'فحص محرك المنفاخ', isRequired: true, category: 'Check' },
          { order: 4, description: 'Check blower belt tension, wear & replace if needed', descriptionAr: 'فحص شد حزام المنفاخ والتآكل والاستبدال عند الحاجة', isRequired: true, category: 'Check' },
          { order: 5, description: 'Check blower & motor bearings, replace if needed', descriptionAr: 'فحص محامل المنفاخ والمحرك والاستبدال عند الحاجة', isRequired: true, category: 'Check' },
          { order: 6, description: 'Check pulley alignment', descriptionAr: 'فحص محاذاة البكرة', isRequired: true, category: 'Check' },
          { order: 7, description: 'Clean drain pan and drain pipe', descriptionAr: 'تنظيف صينية التصريف وأنبوب التصريف', isRequired: true, category: 'Clean' },
          { order: 8, description: 'Check cold water pipe & clean strainer', descriptionAr: 'فحص أنبوب الماء البارد وتنظيف المصفاة', isRequired: true, category: 'Check' },
          { order: 9, description: 'Check canvas connections & duct insulation', descriptionAr: 'فحص وصلات القماش وعزل القنوات', isRequired: true, category: 'Check' },
          { order: 10, description: 'Check power and control wiring', descriptionAr: 'فحص أسلاك الطاقة والتحكم', isRequired: true, category: 'Check' },
          { order: 11, description: 'Check thermal insulation on pipes', descriptionAr: 'فحص العزل الحراري على الأنابيب', isRequired: true, category: 'Check' },
          { order: 12, description: 'Check vibration isolators', descriptionAr: 'فحص عوازل الاهتزاز', isRequired: true, category: 'Check' },
          { order: 13, description: 'Check structure for loose bolts', descriptionAr: 'فحص الهيكل بحثًا عن مسامير مفكوكة', isRequired: true, category: 'Check' },
          { order: 14, description: 'Check rusted/dented body parts', descriptionAr: 'فحص الأجزاء الصدئة/المقعرة من الجسم', isRequired: true, category: 'Check' },
        ],
      },
    },
  });

  // Split AC Checklist (11 items from Excel)
  const splitAcChecklist = await prisma.checklistTemplate.create({
    data: {
      name: 'Split AC Monthly PM Checklist',
      nameAr: 'قائمة فحص الصيانة الشهرية لمكيف الهواء المنفصل',
      description: 'Standard monthly preventive maintenance for split AC units',
      categoryId: splitAcCategory.id,
      isDefault: true,
      items: {
        create: [
          { order: 1, description: 'Clean condenser coil with water pressure', descriptionAr: 'تنظيف ملف المكثف بضغط الماء', isRequired: true, category: 'Clean' },
          { order: 2, description: 'Clean indoor unit completely', descriptionAr: 'تنظيف الوحدة الداخلية بالكامل', isRequired: true, category: 'Clean' },
          { order: 3, description: 'Check fan motor bearings', descriptionAr: 'فحص محامل محرك المروحة', isRequired: true, category: 'Check' },
          { order: 4, description: 'Complete refrigerant leak check', descriptionAr: 'إجراء فحص شامل لتسرب المبردات', isRequired: true, category: 'Check' },
          { order: 5, description: 'Clean PC board & check power/control wiring', descriptionAr: 'تنظيف لوحة الكمبيوتر وفحص أسلاك الطاقة/التحكم', isRequired: true, category: 'Clean' },
          { order: 6, description: 'Check compressor contactors/overloads/breakers', descriptionAr: 'فحص ملامسات الضاغط وقواطع الحمل الزائد', isRequired: true, category: 'Check' },
          { order: 7, description: 'Check compressor motor protectors', descriptionAr: 'فحص واقيات محرك الضاغط', isRequired: true, category: 'Check' },
          { order: 8, description: 'Check thermal insulation on cooler & piping', descriptionAr: 'فحص العزل الحراري على المبرد والأنابيب', isRequired: true, category: 'Check' },
          { order: 9, description: 'Check vibration isolators', descriptionAr: 'فحص عوازل الاهتزاز', isRequired: true, category: 'Check' },
          { order: 10, description: 'Check structure for loose bolts/screws', descriptionAr: 'فحص الهيكل بحثًا عن مسامير مفكوكة', isRequired: true, category: 'Check' },
          { order: 11, description: 'Check rusted/dented/damaged body parts', descriptionAr: 'فحص الأجزاء الصدئة/المقعرة/التالفة من الجسم', isRequired: true, category: 'Check' },
        ],
      },
    },
  });

  console.log('✅ Checklist templates created');

  // ============================================
  // 9. CREATE PM SCHEDULES
  // ============================================
  await prisma.pMSchedule.create({
    data: {
      equipmentId: chiller1.id,
      name: 'Chiller 1-A Quarterly PM',
      description: 'Quarterly preventive maintenance schedule',
      intervalType: 'QUARTERLY',
      intervalValue: 1,
      lastPerformed: new Date('2024-01-15'),
      nextDue: new Date('2024-04-15'),
      autoGenerateWO: true,
      assignedToId: technician1.id,
      startDate: new Date('2024-01-01'),
    },
  });

  await prisma.pMSchedule.create({
    data: {
      equipmentId: ahu1.id,
      name: 'AHU-1 Monthly PM',
      description: 'Monthly preventive maintenance schedule',
      intervalType: 'MONTHLY',
      intervalValue: 1,
      lastPerformed: new Date('2024-02-01'),
      nextDue: new Date('2024-03-01'),
      autoGenerateWO: true,
      assignedToId: technician1.id,
      startDate: new Date('2024-01-01'),
    },
  });

  await prisma.pMSchedule.create({
    data: {
      equipmentId: splitAc1.id,
      name: 'Split AC Office 101 Monthly PM',
      intervalType: 'MONTHLY',
      intervalValue: 1,
      lastPerformed: new Date('2024-02-15'),
      nextDue: new Date('2024-03-15'),
      autoGenerateWO: true,
      assignedToId: technician1.id,
      startDate: new Date('2024-01-01'),
    },
  });

  await prisma.pMSchedule.create({
    data: {
      equipmentId: transformer1.id,
      name: 'Main Transformer Annual PM',
      intervalType: 'YEARLY',
      intervalValue: 1,
      lastPerformed: new Date('2024-01-10'),
      nextDue: new Date('2025-01-10'),
      autoGenerateWO: true,
      assignedToId: technician2.id,
      startDate: new Date('2024-01-01'),
    },
  });

  console.log('✅ PM schedules created');

  // ============================================
  // 10. CREATE WORK ORDERS (Sample)
  // ============================================
  const today = new Date();
  const threeDaysAgo = new Date(today);
  threeDaysAgo.setDate(threeDaysAgo.getDate() - 3);

  const wo1 = await prisma.workOrder.create({
    data: {
      woNumber: 'PPM-2024-0001',
      title: 'Chiller 1-A Quarterly PM',
      titleAr: 'الصيانة الربع سنوية لمبرد 1-أ',
      description: 'Quarterly preventive maintenance as per checklist',
      type: 'PREVENTIVE',
      priority: 'HIGH',
      status: 'IN_PROGRESS',
      dueDate: new Date(today),
      equipmentId: chiller1.id,
      assignedToId: technician1.id,
      requesterId: engineer.id,
      estimatedHours: 3.0,
      startTime: new Date(today.setHours(8, 0, 0)),
    },
  });

  const wo2 = await prisma.workOrder.create({
    data: {
      woNumber: 'PPM-2024-0002',
      title: 'AHU-1 Monthly PM',
      titleAr: 'الصيانة الشهرية لوحدة مناولة الهواء 1',
      description: 'Monthly preventive maintenance',
      type: 'PREVENTIVE',
      priority: 'MEDIUM',
      status: 'OPEN',
      dueDate: new Date(today),
      equipmentId: ahu1.id,
      assignedToId: technician1.id,
      requesterId: engineer.id,
      estimatedHours: 1.5,
    },
  });

  const wo3 = await prisma.workOrder.create({
    data: {
      woNumber: 'PPM-2024-0003',
      title: 'Split AC Office 101 Monthly PM',
      titleAr: 'الصيانة الشهرية لمكيف مكتب 101',
      description: 'Monthly preventive maintenance',
      type: 'PREVENTIVE',
      priority: 'LOW',
      status: 'COMPLETED',
      dueDate: new Date(threeDaysAgo),
      equipmentId: splitAc1.id,
      assignedToId: technician1.id,
      requesterId: engineer.id,
      estimatedHours: 0.75,
      actualHours: 0.8,
      completedAt: new Date(threeDaysAgo),
      completedById: technician1.id,
    },
  });

  const wo4 = await prisma.workOrder.create({
    data: {
      woNumber: 'PPM-2024-0004',
      title: 'Overdue - Chiller 2-B Quarterly PM',
      titleAr: 'متأخر - الصيانة الربع سنوية لمبرد 2-ب',
      description: 'OVERDUE: Quarterly preventive maintenance',
      type: 'PREVENTIVE',
      priority: 'URGENT',
      status: 'OPEN',
      dueDate: threeDaysAgo,
      equipmentId: chiller2.id,
      assignedToId: technician1.id,
      requesterId: engineer.id,
      estimatedHours: 3.0,
    },
  });

  console.log('✅ Work orders created');

  // ============================================
  // 11. CREATE CHECKLIST RESULTS (for completed WO)
  // ============================================
  await prisma.checklistResult.createMany({
    data: [
      { workOrderId: wo3.id, checklistItemId: '', itemDescription: 'Clean condenser coil with water pressure', isRequired: true, isDone: true, completedAt: new Date() },
      { workOrderId: wo3.id, checklistItemId: '', itemDescription: 'Clean indoor unit completely', isRequired: true, isDone: true, completedAt: new Date() },
      { workOrderId: wo3.id, checklistItemId: '', itemDescription: 'Check fan motor bearings', isRequired: true, isDone: true, completedAt: new Date() },
      { workOrderId: wo3.id, checklistItemId: '', itemDescription: 'Complete refrigerant leak check', isRequired: true, isDone: true, completedAt: new Date() },
      { workOrderId: wo3.id, checklistItemId: '', itemDescription: 'Clean PC board & check wiring', isRequired: true, isDone: true, completedAt: new Date() },
    ],
  });

  console.log('✅ Checklist results created');

  // ============================================
  // 12. CREATE WAREHOUSE & INVENTORY
  // ============================================
  const warehouse = await prisma.warehouse.create({
    data: {
      name: 'Main Store',
      nameAr: 'المخزن الرئيسي',
      code: 'WH-001',
      address: 'Building A - Ground Floor',
      manager: 'Store Keeper',
    },
  });

  await prisma.inventoryItem.createMany({
    data: [
      { sku: 'SP-001', name: 'Air Filter 24x24', nameAr: 'فلتر هواء 24x24', quantity: 50, minStock: 20, unit: 'piece', warehouseId: warehouse.id, costPrice: 25.0 },
      { sku: 'SP-002', name: 'Refrigerant R-134a', nameAr: 'مبرد R-134a', quantity: 15, minStock: 5, unit: 'cylinder', warehouseId: warehouse.id, costPrice: 150.0 },
      { sku: 'SP-003', name: 'Blower Belt A-68', nameAr: 'حزام منفاخ A-68', quantity: 10, minStock: 5, unit: 'piece', warehouseId: warehouse.id, costPrice: 35.0 },
      { sku: 'SP-004', name: 'Contactor 40A', nameAr: 'ملامس 40 أمبير', quantity: 8, minStock: 3, unit: 'piece', warehouseId: warehouse.id, costPrice: 45.0 },
      { sku: 'SP-005', name: 'Thermal Insulation Tape', nameAr: 'شريط عزل حراري', quantity: 30, minStock: 10, unit: 'roll', warehouseId: warehouse.id, costPrice: 12.0 },
    ],
  });

  console.log('✅ Warehouse and inventory items created');

  // ============================================
  // 13. CREATE SYSTEM SETTINGS
  // ============================================
  await prisma.systemSetting.createMany({
    data: [
      { key: 'app.name', value: 'CMMS Platform', type: 'string', description: 'Application name', isPublic: true },
      { key: 'app.logo', value: '/logo.png', type: 'string', description: 'Application logo path', isPublic: true },
      { key: 'maintenance.work_hours_start', value: '08:00', type: 'string', description: 'Work hours start time', isPublic: false },
      { key: 'maintenance.work_hours_end', value: '17:00', type: 'string', description: 'Work hours end time', isPublic: false },
      { key: 'notifications.whatsapp_enabled', value: 'true', type: 'boolean', description: 'Enable WhatsApp notifications', isPublic: false },
      { key: 'notifications.email_enabled', value: 'true', type: 'boolean', description: 'Enable email notifications', isPublic: false },
    ],
  });

  console.log('✅ System settings created');

  // ============================================
  // SUMMARY
  // ============================================
  console.log('\n========================================');
  console.log('🎉 Database seeding completed!');
  console.log('========================================');
  console.log('📊 Summary:');
  console.log(`   • Users: 5 (1 Admin, 1 Engineer, 2 Technicians, 1 Viewer)`);
  console.log(`   • Departments: 4 (HVAC, Electrical, Mechanical, Civil)`);
  console.log(`   • Facility: 1 (Hospital Complex)`);
  console.log(`   • Buildings: 2`);
  console.log(`   • Equipment: 10 items across multiple categories`);
  console.log(`   • Checklist Templates: 3 (Chiller, AHU, Split AC)`);
  console.log(`   • PM Schedules: 4`);
  console.log(`   • Work Orders: 4 (1 In Progress, 2 Open, 1 Completed)`);
  console.log(`   • Inventory Items: 5`);
  console.log('========================================');
  console.log('🔐 Default Login Credentials:');
  console.log('   • Admin: admin@cmms.local / Admin123!');
  console.log('   • Engineer: engineer@cmms.local / Admin123!');
  console.log('   • Technician: tech1@cmms.local / Admin123!');
  console.log('   • Viewer: viewer@cmms.local / Admin123!');
  console.log('========================================\n');
}

main()
  .catch((e) => {
    console.error('❌ Seeding error:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
