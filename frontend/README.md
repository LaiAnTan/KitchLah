# KitchLah - AI-Powered Kitchen Operations

A modern React.js web application designed to optimize kitchen operations through AI-powered insights and real-time monitoring.

## 🚀 Features

### 📊 Dashboard
- **Order Predictions**: ML-based daily order forecasting with confidence levels
- **Real-Time Alerts**: Live notifications for delays, surges, and critical issues
- **Interactive Charts**: Visual representation of predicted orders throughout the day
- **Surge Predictions**: Advanced warning system for peak hours

### ♻️ Smart Waste Minimization
- **Inventory Management**: Real-time stock tracking with expiry monitoring
- **Stock History**: Complete transaction history with waste cost tracking
- **AI Suggestions**: Intelligent recommendations to reduce food waste
- **Color-Coded Alerts**: Visual indicators for near-expiry items

### 🤖 AI Decision Making
- **Station Management**: Real-time monitoring of all kitchen stations
- **Order Queues**: Live order tracking with priority and status indicators
- **Load Balancing**: AI-powered recommendations for optimal station utilization
- **What-If Simulations**: Predictive modeling for different scenarios

## 🎨 Design System

### Color Palette
- **Primary Green** (#2E7D32): Main actions, key highlights
- **Secondary Green** (#66BB6A): Backgrounds, cards, secondary elements
- **Accent Yellow/Orange** (#F9A825): Warnings, near-expiry stock
- **Alert Red** (#D32F2F): Critical alerts, delays, urgent issues
- **Neutral Grey** (#9E9E9E): Secondary text, icons, dividers
- **Background White** (#FFFFFF): Primary background
- **Off White** (#F5F5F5): Secondary sections, subtle contrast

### Typography
- **Font Family**: Inter, Roboto, Poppins (sans-serif)
- **Style**: Clean, modern, flat design with soft shadows and rounded corners

## 🛠️ Technology Stack

- **Frontend**: React.js with TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Routing**: React Router DOM
- **State Management**: React Context (ready for Redux integration)
- **Icons**: Emoji-based for simplicity and universal compatibility

## 📱 Responsive Design

The application is fully responsive and optimized for:
- **Desktop**: Full-featured experience with split-screen layouts
- **Tablet**: Adaptive grid layouts with touch-friendly navigation
- **Mobile**: Stacked layouts with collapsible navigation

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd kitchlah
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Build for Production

```bash
npm run build
```

## 📊 Mock Data

The application includes comprehensive mock data for demonstration:
- **Order Predictions**: 16 time slots with confidence levels
- **Alerts**: Real-time notifications with different severity levels
- **Stock Items**: Inventory with expiry tracking and cost information
- **Station Data**: Kitchen stations with load and capacity information
- **AI Suggestions**: Intelligent recommendations for waste reduction and efficiency

## 🎯 Key Features

### Stress-Friendly UI
- **Clear Hierarchy**: Important information is prominently displayed
- **Minimal Cognitive Load**: Clean design with intuitive navigation
- **Color-Coded Status**: Quick visual identification of issues
- **Real-Time Updates**: Live data for immediate decision making

### AI Integration Ready
- **Modular Design**: Easy integration with backend AI services
- **Mock Data Structure**: Realistic data models for seamless API integration
- **Extensible Components**: Ready for additional AI features

## 🔧 Customization

### Adding New Stations
1. Update the `stations` array in `src/data/mockData.ts`
2. Add corresponding tab in `AIDecisionMaking.tsx`

### Modifying Color Scheme
1. Update color values in `tailwind.config.js`
2. Adjust component-specific colors as needed

### Adding New Alert Types
1. Extend the `Alert` interface in `mockData.ts`
2. Update alert rendering logic in components

## 📈 Future Enhancements

- **Real-time Data Integration**: Connect to live kitchen management systems
- **Advanced AI Models**: Implement machine learning for better predictions
- **Mobile App**: Native mobile application for kitchen staff
- **Analytics Dashboard**: Detailed performance metrics and reporting
- **Integration APIs**: Connect with POS systems and inventory management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please contact the development team or create an issue in the repository.

---

**KitchLah** - Transforming kitchen operations through intelligent automation and real-time insights.