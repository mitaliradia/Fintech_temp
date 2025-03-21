import React from 'react';
import { Line, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import '../index.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend);

const Dashboard = () => {
  // Data for Line Graph (Transaction Trends)
  const lineData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Spending ($)',
        data: [1200, 1900, 1500, 2200, 1800, 2100],
        borderColor: '#4a90e2',
        backgroundColor: 'rgba(74, 144, 226, 0.2)',
        fill: true,
        tension: 0.3,
      },
    ],
  };

  // Data for Pie Chart (Investment Portfolio)
  const pieData = {
    labels: ['Stocks', 'Crypto', 'Other Assets'],
    datasets: [
      {
        data: [5200, 3150, 1200],
        backgroundColor: ['#4a90e2', '#50e3c2', '#f5a623'],
        hoverOffset: 20,
      },
    ],
  };

  // Options for charts
  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } },
    scales: { y: { beginAtZero: true } },
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'top' } },
  };

  return (
    <div className="dashboard-container">
      {/* Account Overview */}
      <section className="card account-overview">
        <h2>Account Overview</h2>
        <div className="overview-details">
          <div className="balance">
            <h3>Current Balance</h3>
            <p>$12,345.67</p>
          </div>
          <div className="transactions">
            <h3>Transactions</h3>
            <p>32 this month</p>
          </div>
          <div className="insights">
            <h3>Insights</h3>
            <p>Spending up 5%</p>
          </div>
        </div>
      </section>

      {/* Recent Transactions with Line Graph */}
      <section className="card recent-transactions">
        <h2>Recent Transactions</h2>
        <div className="transaction-graph">
          <h3>Transaction Trends</h3>
          <div className="graph-container">
            <Line data={lineData} options={lineOptions} />
          </div>
        </div>
        <ul>
          <li>Starbucks - $5.20 <span>Mar 19, 2025</span></li>
          <li>Amazon - $45.99 <span>Mar 18, 2025</span></li>
          <li>Grocery Store - $72.30 <span>Mar 17, 2025</span></li>
        </ul>
      </section>

      {/* Investment Portfolio with Pie Chart */}
      <section className="card investment-portfolio">
        <h2>Investment Portfolio</h2>
        <div className="portfolio-graph">
          <div className="graph-container">
            <Pie data={pieData} options={pieOptions} />
          </div>
        </div>
        <div className="portfolio-details">
          <div>
            <h3>Stocks</h3>
            <p>$5,200</p>
          </div>
          <div>
            <h3>Crypto</h3>
            <p>$3,150</p>
          </div>
          <div>
            <h3>Other Assets</h3>
            <p>$1,200</p>
          </div>
        </div>
      </section>

      {/* Budget & Savings */}
      <section className="card budget-savings">
        <h2>Budget & Savings</h2>
        <div className="budget-details">
          <div>
            <h3>Monthly Budget</h3>
            <p>$2,500 / $3,000</p>
          </div>
          <div>
            <h3>Savings Goal</h3>
            <p>$10,000 / $15,000</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;