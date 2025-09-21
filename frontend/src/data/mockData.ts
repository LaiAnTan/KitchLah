// Mock data for KitchLah application

export interface OrderPrediction {
  timeSlot: string;
  predictedOrders: number;
  confidence: number;
}

export interface MenuPrediction {
  menu: string;
  quantity: number;
  hourlyBreakdown?: HourlyBreakdown[];
}

export interface HourlyBreakdown {
  hour: string;
  quantity: number;
}

export interface Alert {
  id: string;
  type: 'delay' | 'surge' | 'critical';
  message: string;
  timestamp: string;
  severity: 'low' | 'medium' | 'high';
}

export interface StockItem {
  id: string;
  name: string;
  quantity: number;
  unit: string;
  expiryDate: string;
  status: 'fresh' | 'near-expiry' | 'expired';
  cost: number;
}

export interface RecipeIngredient {
  id: string;
  name: string;
  quantity: number;
  unit: string;
  notes: string;
}

export interface Recipe {
  cook_time_minutes: number;
  cuisine_type: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  estimated_cost: number;
  ingredients: RecipeIngredient[];
  instructions: string[];
  name: string;
  primary_ingredient: string;
  profit_margin_percent: number;
  servings: number;
  suggested_selling_price: number;
}

export interface StockHistory {
  id: string;
  date: string;
  item: string;
  addedQuantity: number;
  totalQuantity: number;
  action: 'added' | 'used' | 'wasted';
  cost: number;
}

export interface Station {
  id: string;
  name: string;
  currentLoad: number;
  maxCapacity: number;
  ordersInQueue: number;
  avgProcessingTime: number;
}

export interface Order {
  id: string;
  customerName: string;
  items: string[];
  station: string;
  status: 'pending' | 'preparing' | 'ready' | 'completed';
  estimatedTime: number;
  priority: 'low' | 'medium' | 'high';
}

export interface AISuggestion {
  id: string;
  type: 'waste' | 'efficiency' | 'inventory';
  title: string;
  description: string;
  impact: 'low' | 'medium' | 'high';
  action: string;
}

// Mock data
export const orderPredictions: OrderPrediction[] = [
  { timeSlot: '6:00 AM', predictedOrders: 12, confidence: 85 },
  { timeSlot: '7:00 AM', predictedOrders: 28, confidence: 92 },
  { timeSlot: '8:00 AM', predictedOrders: 45, confidence: 88 },
  { timeSlot: '9:00 AM', predictedOrders: 38, confidence: 90 },
  { timeSlot: '10:00 AM', predictedOrders: 25, confidence: 87 },
  { timeSlot: '11:00 AM', predictedOrders: 32, confidence: 89 },
  { timeSlot: '12:00 PM', predictedOrders: 68, confidence: 95 },
  { timeSlot: '1:00 PM', predictedOrders: 72, confidence: 93 },
  { timeSlot: '2:00 PM', predictedOrders: 35, confidence: 86 },
  { timeSlot: '3:00 PM', predictedOrders: 28, confidence: 88 },
  { timeSlot: '4:00 PM', predictedOrders: 22, confidence: 85 },
  { timeSlot: '5:00 PM', predictedOrders: 38, confidence: 90 },
  { timeSlot: '6:00 PM', predictedOrders: 55, confidence: 92 },
  { timeSlot: '7:00 PM', predictedOrders: 62, confidence: 94 },
  { timeSlot: '8:00 PM', predictedOrders: 48, confidence: 89 },
  { timeSlot: '9:00 PM', predictedOrders: 25, confidence: 87 },
];

export const alerts: Alert[] = [
  {
    id: '1',
    type: 'delay',
    message: 'Order #24 delayed by 10 mins',
    timestamp: '2024-01-20 14:30:00',
    severity: 'medium'
  },
  {
    id: '2',
    type: 'surge',
    message: '+30% surge expected at 7PM',
    timestamp: '2024-01-20 14:25:00',
    severity: 'high'
  },
  {
    id: '3',
    type: 'critical',
    message: 'Fryer Station overloaded - 15 orders queued',
    timestamp: '2024-01-20 14:20:00',
    severity: 'high'
  }
];

export const stockItems: StockItem[] = [
  {
    id: '1',
    name: 'Chicken Breast',
    quantity: 25,
    unit: 'kg',
    expiryDate: '2024-01-22',
    status: 'fresh',
    cost: 12.50
  },
  {
    id: '2',
    name: 'Tomatoes',
    quantity: 15,
    unit: 'kg',
    expiryDate: '2024-01-21',
    status: 'near-expiry',
    cost: 3.20
  },
  {
    id: '3',
    name: 'Lettuce',
    quantity: 8,
    unit: 'heads',
    expiryDate: '2024-01-20',
    status: 'near-expiry',
    cost: 2.10
  },
  {
    id: '4',
    name: 'Ground Beef',
    quantity: 18,
    unit: 'kg',
    expiryDate: '2024-01-25',
    status: 'fresh',
    cost: 15.80
  },
  {
    id: '5',
    name: 'Milk',
    quantity: 12,
    unit: 'liters',
    expiryDate: '2024-01-19',
    status: 'expired',
    cost: 4.50
  }
];

export const menuPredictions: MenuPrediction[] = [
  {
    menu: 'Chicken Burger',
    quantity: 180,
    hourlyBreakdown: [
      { hour: '6:00 AM', quantity: 8 },
      { hour: '7:00 AM', quantity: 15 },
      { hour: '8:00 AM', quantity: 22 },
      { hour: '9:00 AM', quantity: 18 },
      { hour: '10:00 AM', quantity: 12 },
      { hour: '11:00 AM', quantity: 16 },
      { hour: '12:00 PM', quantity: 28 },
      { hour: '1:00 PM', quantity: 32 },
      { hour: '2:00 PM', quantity: 15 },
      { hour: '3:00 PM', quantity: 12 },
      { hour: '4:00 PM', quantity: 8 },
      { hour: '5:00 PM', quantity: 18 },
      { hour: '6:00 PM', quantity: 25 },
      { hour: '7:00 PM', quantity: 28 },
      { hour: '8:00 PM', quantity: 20 },
      { hour: '9:00 PM', quantity: 10 }
    ]
  },
  {
    menu: 'Fish & Chips',
    quantity: 145,
    hourlyBreakdown: [
      { hour: '6:00 AM', quantity: 5 },
      { hour: '7:00 AM', quantity: 12 },
      { hour: '8:00 AM', quantity: 18 },
      { hour: '9:00 AM', quantity: 15 },
      { hour: '10:00 AM', quantity: 10 },
      { hour: '11:00 AM', quantity: 14 },
      { hour: '12:00 PM', quantity: 25 },
      { hour: '1:00 PM', quantity: 28 },
      { hour: '2:00 PM', quantity: 12 },
      { hour: '3:00 PM', quantity: 9 },
      { hour: '4:00 PM', quantity: 6 },
      { hour: '5:00 PM', quantity: 15 },
      { hour: '6:00 PM', quantity: 22 },
      { hour: '7:00 PM', quantity: 25 },
      { hour: '8:00 PM', quantity: 18 },
      { hour: '9:00 PM', quantity: 8 }
    ]
  },
  {
    menu: 'Grilled Chicken',
    quantity: 120,
    hourlyBreakdown: [
      { hour: '6:00 AM', quantity: 3 },
      { hour: '7:00 AM', quantity: 8 },
      { hour: '8:00 AM', quantity: 12 },
      { hour: '9:00 AM', quantity: 10 },
      { hour: '10:00 AM', quantity: 7 },
      { hour: '11:00 AM', quantity: 9 },
      { hour: '12:00 PM', quantity: 18 },
      { hour: '1:00 PM', quantity: 22 },
      { hour: '2:00 PM', quantity: 8 },
      { hour: '3:00 PM', quantity: 6 },
      { hour: '4:00 PM', quantity: 4 },
      { hour: '5:00 PM', quantity: 10 },
      { hour: '6:00 PM', quantity: 15 },
      { hour: '7:00 PM', quantity: 18 },
      { hour: '8:00 PM', quantity: 12 },
      { hour: '9:00 PM', quantity: 5 }
    ]
  },
  {
    menu: 'Pasta Special',
    quantity: 95,
    hourlyBreakdown: [
      { hour: '6:00 AM', quantity: 2 },
      { hour: '7:00 AM', quantity: 5 },
      { hour: '8:00 AM', quantity: 8 },
      { hour: '9:00 AM', quantity: 6 },
      { hour: '10:00 AM', quantity: 4 },
      { hour: '11:00 AM', quantity: 6 },
      { hour: '12:00 PM', quantity: 12 },
      { hour: '1:00 PM', quantity: 15 },
      { hour: '2:00 PM', quantity: 6 },
      { hour: '3:00 PM', quantity: 4 },
      { hour: '4:00 PM', quantity: 3 },
      { hour: '5:00 PM', quantity: 7 },
      { hour: '6:00 PM', quantity: 10 },
      { hour: '7:00 PM', quantity: 12 },
      { hour: '8:00 PM', quantity: 8 },
      { hour: '9:00 PM', quantity: 3 }
    ]
  },
  {
    menu: 'Soup of the Day',
    quantity: 75,
    hourlyBreakdown: [
      { hour: '6:00 AM', quantity: 4 },
      { hour: '7:00 AM', quantity: 8 },
      { hour: '8:00 AM', quantity: 6 },
      { hour: '9:00 AM', quantity: 5 },
      { hour: '10:00 AM', quantity: 3 },
      { hour: '11:00 AM', quantity: 4 },
      { hour: '12:00 PM', quantity: 8 },
      { hour: '1:00 PM', quantity: 10 },
      { hour: '2:00 PM', quantity: 4 },
      { hour: '3:00 PM', quantity: 3 },
      { hour: '4:00 PM', quantity: 2 },
      { hour: '5:00 PM', quantity: 5 },
      { hour: '6:00 PM', quantity: 7 },
      { hour: '7:00 PM', quantity: 8 },
      { hour: '8:00 PM', quantity: 6 },
      { hour: '9:00 PM', quantity: 2 }
    ]
  }
];

export const stockHistory: StockHistory[] = [
  {
    id: '1',
    date: '2024-01-20',
    item: 'Chicken Breast',
    addedQuantity: 30,
    totalQuantity: 30,
    action: 'added',
    cost: 375.00
  },
  {
    id: '2',
    date: '2024-01-20',
    item: 'Chicken Breast',
    addedQuantity: -5,
    totalQuantity: 25,
    action: 'used',
    cost: 62.50
  },
  {
    id: '3',
    date: '2024-01-19',
    item: 'Milk',
    addedQuantity: -12,
    totalQuantity: 0,
    action: 'wasted',
    cost: 54.00
  },
  {
    id: '4',
    date: '2024-01-19',
    item: 'Tomatoes',
    addedQuantity: 20,
    totalQuantity: 20,
    action: 'added',
    cost: 64.00
  },
  {
    id: '5',
    date: '2024-01-19',
    item: 'Tomatoes',
    addedQuantity: -5,
    totalQuantity: 15,
    action: 'used',
    cost: 16.00
  },
  {
    id: '6',
    date: '2024-01-18',
    item: 'Lettuce',
    addedQuantity: 15,
    totalQuantity: 15,
    action: 'added',
    cost: 31.50
  },
  {
    id: '7',
    date: '2024-01-18',
    item: 'Lettuce',
    addedQuantity: -7,
    totalQuantity: 8,
    action: 'used',
    cost: 14.70
  },
  {
    id: '8',
    date: '2024-01-17',
    item: 'Ground Beef',
    addedQuantity: 25,
    totalQuantity: 25,
    action: 'added',
    cost: 395.00
  },
  {
    id: '9',
    date: '2024-01-17',
    item: 'Ground Beef',
    addedQuantity: -7,
    totalQuantity: 18,
    action: 'used',
    cost: 110.60
  },
  {
    id: '10',
    date: '2024-01-16',
    item: 'Fish Fillet',
    addedQuantity: 18,
    totalQuantity: 18,
    action: 'added',
    cost: 270.00
  },
  {
    id: '11',
    date: '2024-01-16',
    item: 'Fish Fillet',
    addedQuantity: -4,
    totalQuantity: 14,
    action: 'used',
    cost: 60.00
  },
  {
    id: '12',
    date: '2024-01-15',
    item: 'Pasta',
    addedQuantity: 12,
    totalQuantity: 12,
    action: 'added',
    cost: 36.00
  },
  {
    id: '13',
    date: '2024-01-15',
    item: 'Pasta',
    addedQuantity: -3,
    totalQuantity: 9,
    action: 'used',
    cost: 9.00
  }
];

export const stations: Station[] = [
  {
    id: 'prep',
    name: 'Prep Station',
    currentLoad: 65,
    maxCapacity: 100,
    ordersInQueue: 8,
    avgProcessingTime: 12
  },
  {
    id: 'fryer',
    name: 'Fryer Station',
    currentLoad: 90,
    maxCapacity: 100,
    ordersInQueue: 15,
    avgProcessingTime: 8
  },
  {
    id: 'grill',
    name: 'Grill Station',
    currentLoad: 45,
    maxCapacity: 100,
    ordersInQueue: 5,
    avgProcessingTime: 15
  },
  {
    id: 'stove',
    name: 'Stove Station',
    currentLoad: 70,
    maxCapacity: 100,
    ordersInQueue: 10,
    avgProcessingTime: 10
  },
  {
    id: 'assembly',
    name: 'Assembly Station',
    currentLoad: 55,
    maxCapacity: 100,
    ordersInQueue: 7,
    avgProcessingTime: 5
  }
];

export const orders: Order[] = [
  {
    id: '1',
    customerName: 'John Doe',
    items: ['Chicken Burger', 'Fries'],
    station: 'fryer',
    status: 'preparing',
    estimatedTime: 8,
    priority: 'medium'
  },
  {
    id: '2',
    customerName: 'Jane Smith',
    items: ['Grilled Chicken', 'Salad'],
    station: 'grill',
    status: 'pending',
    estimatedTime: 15,
    priority: 'high'
  },
  {
    id: '3',
    customerName: 'Mike Johnson',
    items: ['Pasta Special', 'Soup'],
    station: 'stove',
    status: 'preparing',
    estimatedTime: 10,
    priority: 'low'
  },
  {
    id: '4',
    customerName: 'Sarah Wilson',
    items: ['Fish & Chips', 'Coleslaw'],
    station: 'fryer',
    status: 'pending',
    estimatedTime: 12,
    priority: 'high'
  },
  {
    id: '5',
    customerName: 'David Brown',
    items: ['Chicken Burger', 'Onion Rings'],
    station: 'fryer',
    status: 'ready',
    estimatedTime: 0,
    priority: 'medium'
  },
  {
    id: '6',
    customerName: 'Lisa Garcia',
    items: ['Grilled Chicken', 'Rice'],
    station: 'grill',
    status: 'preparing',
    estimatedTime: 18,
    priority: 'low'
  },
  {
    id: '7',
    customerName: 'Tom Anderson',
    items: ['Pasta Special', 'Garlic Bread'],
    station: 'stove',
    status: 'pending',
    estimatedTime: 14,
    priority: 'medium'
  },
  {
    id: '8',
    customerName: 'Emma Davis',
    items: ['Fish & Chips', 'Mushy Peas'],
    station: 'fryer',
    status: 'preparing',
    estimatedTime: 10,
    priority: 'high'
  },
  {
    id: '9',
    customerName: 'Chris Taylor',
    items: ['Chicken Burger', 'Fries', 'Drink'],
    station: 'assembly',
    status: 'pending',
    estimatedTime: 5,
    priority: 'medium'
  },
  {
    id: '10',
    customerName: 'Maria Rodriguez',
    items: ['Grilled Chicken', 'Vegetables'],
    station: 'grill',
    status: 'ready',
    estimatedTime: 0,
    priority: 'low'
  },
  {
    id: '11',
    customerName: 'James Wilson',
    items: ['Pasta Special', 'Caesar Salad'],
    station: 'stove',
    status: 'preparing',
    estimatedTime: 12,
    priority: 'high'
  },
  {
    id: '12',
    customerName: 'Anna Thompson',
    items: ['Fish & Chips', 'Tartar Sauce'],
    station: 'fryer',
    status: 'pending',
    estimatedTime: 15,
    priority: 'medium'
  },
  {
    id: '13',
    customerName: 'Robert Lee',
    items: ['Chicken Burger', 'Sweet Potato Fries'],
    station: 'fryer',
    status: 'preparing',
    estimatedTime: 9,
    priority: 'low'
  },
  {
    id: '14',
    customerName: 'Jennifer White',
    items: ['Grilled Chicken', 'Quinoa'],
    station: 'grill',
    status: 'pending',
    estimatedTime: 20,
    priority: 'high'
  },
  {
    id: '15',
    customerName: 'Michael Clark',
    items: ['Pasta Special', 'Breadsticks'],
    station: 'stove',
    status: 'ready',
    estimatedTime: 0,
    priority: 'medium'
  }
];

export const aiSuggestions: AISuggestion[] = [
  {
    id: '1',
    type: 'waste',
    title: 'Use Chicken Stock for Soup Special',
    description: 'Chicken breast expires in 2 days. Recommend creating a soup special to utilize the stock efficiently.',
    impact: 'medium',
    action: 'Create soup special menu item'
  },
  {
    id: '2',
    type: 'inventory',
    title: 'Offer 20% Discount on Tomato Dishes',
    description: 'Tomatoes are near expiry. Offer discount to increase sales and reduce waste.',
    impact: 'high',
    action: 'Apply discount to tomato-based dishes'
  },
  {
    id: '3',
    type: 'efficiency',
    title: 'Redistribute Fryer Station Load',
    description: 'Fryer station is overloaded. Move some orders to grill station to balance workload.',
    impact: 'high',
    action: 'Transfer 5 orders to grill station'
  }
];
