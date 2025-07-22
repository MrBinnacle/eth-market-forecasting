import React from 'react';
import '../DashboardStyles.css';

const ETHDashboard = () => (
  <div className="container">
    <div className="header">
      <div className="total-value">$1,009.78</div>
      <div className="status-indicator">🎓 Learning Portfolio Mode</div>
      <div className="total-return">+$536.10 Total Return (113.3%)</div>
      <div className="emergency-fund-status">
        <strong>Emergency Fund Threshold:</strong>
        <input type="number" className="threshold-input" value="5000" id="thresholdInput" />
        <span style={{ fontSize: '0.9rem', display: 'block', marginTop: '5px' }}>
          Current: 20% of threshold | Status: Play Money
        </span>
      </div>
    </div>
    <div className="update-time">Updated today • ETH Market Dashboard v1</div>
  </div>
);

export default ETHDashboard;
