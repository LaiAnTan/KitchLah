# KitchLah Demo Guide

## 🚀 Quick Start

1. **Navigate to the project directory:**
   ```bash
   cd kitchlah
   ```

2. **Install dependencies (if not already done):**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser to:** `http://localhost:3000`

## 📱 Demo Features to Explore

### 🏠 Dashboard (Landing Page)
- **Current Date & Time**: Live display of current date and time in the header
- **Menu-Based Predictions**: Click on any menu item to see expandable hourly breakdown
- **Loading Animation**: Watch the loading spinner while hourly data is being generated
- **Real-Time Alerts**: See delay notifications, surge predictions, and critical alerts
- **Interactive Chart**: Hover over the line chart to see detailed order predictions
- **Surge Predictions**: Check the right panel for peak hour warnings

### ♻️ Smart Waste Minimization
- **Inventory Tab**: 
  - View current stock with color-coded expiry status
  - **NEW**: Stock percentage column with visual progress bars
  - Green = Fresh, Yellow = Near-expiry, Red = Expired
- **Stock History Tab**:
  - See enhanced transaction history with more detailed entries
  - Track waste costs and money lost
- **AI Suggestions Panel**:
  - **NEW**: "Generate Recipes/Ideas" button with loading animation
  - Get AI-generated recipe suggestions for near-expiry items
  - See waste reduction strategies
- **Updated Header**: Shows waste cost reduction with percentage improvement

### 🤖 AI Decision Making
- **Station Tabs**: Click through different kitchen stations
  - All Stations, Prep, Fryer, Grill, Stove, Assembly
- **Enhanced Order Queues**: View 15+ orders with detailed customer information
- **Station Overload**: See which stations are overloaded (red indicators)
- **AI Recommendations**: Get efficiency suggestions
- **What-If Simulation**: Try entering scenarios like "What if 20 orders arrive at 8PM?"

## 🎨 Design Highlights

- **Color-Coded System**: 
  - Green = Good/Normal
  - Yellow = Warning/Attention
  - Red = Critical/Urgent
- **Responsive Design**: Resize your browser to see mobile/tablet layouts
- **Clean Typography**: Inter font for modern, readable interface
- **Intuitive Navigation**: Clear icons and labels for easy navigation

## 📊 Mock Data Features

- **16 Time Slots**: Full day order predictions
- **3 Alert Types**: Delays, surges, and critical issues
- **5 Stock Items**: Various expiry statuses for testing
- **5 Kitchen Stations**: Different load levels and capacities
- **AI Suggestions**: Realistic recommendations for waste reduction and efficiency

## 🔧 Customization Ideas

1. **Add More Stations**: Edit `src/data/mockData.ts` to add new kitchen stations
2. **Modify Colors**: Update `tailwind.config.js` for different color schemes
3. **Add New Alert Types**: Extend the Alert interface for more notification types
4. **Enhance Charts**: Add more chart types using Recharts library

## 🚀 Production Deployment

1. **Build the project:**
   ```bash
   npm run build
   ```

2. **Deploy the `build` folder** to your hosting service (Netlify, Vercel, etc.)

## 🆘 Troubleshooting

- **Port 3000 in use?** The app will automatically use the next available port
- **Styling issues?** Make sure Tailwind CSS is properly configured
- **Routing problems?** Check that React Router is correctly set up

---

**Enjoy exploring KitchLah!** 🍳✨
