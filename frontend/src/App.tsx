import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import WasteMinimization from './components/WasteMinimization';
import AIDecisionMaking from './components/AIDecisionMaking';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/waste" element={<WasteMinimization />} />
          <Route path="/ai-decisions" element={<AIDecisionMaking />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
