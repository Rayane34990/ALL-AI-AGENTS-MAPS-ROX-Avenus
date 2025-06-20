import React, { useEffect, useState } from 'react';
import LandingPage from './LandingPage';

const API_BASE = process.env.REACT_APP_API_BASE_URL || '';

function unique(arr) {
  return Array.from(new Set(arr.filter(Boolean)));
}

function downloadCSV(data, filename) {
  const replacer = (key, value) => value === null ? '' : value;
  const header = Object.keys(data[0] || {});
  const csv = [header.join(',')].concat(
    data.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
  ).join('\r\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  window.URL.revokeObjectURL(url);
}

function downloadJSON(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  window.URL.revokeObjectURL(url);
}

function getCounts(arr, key) {
  return arr.reduce((acc, item) => {
    const val = (item[key] || '').split(',').map(v => v.trim()).filter(Boolean);
    val.forEach(v => { if (v) acc[v] = (acc[v] || 0) + 1; });
    return acc;
  }, {});
}

function App() {
  // You can add routing logic here if you want to show the landing page only at '/'
  return <LandingPage />;
}

export default App;
