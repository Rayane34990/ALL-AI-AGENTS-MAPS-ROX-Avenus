import React, { useEffect, useState } from 'react';

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
  const [agents, setAgents] = useState([]);
  const [query, setQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [tagFilter, setTagFilter] = useState('');
  const [licenseFilter, setLicenseFilter] = useState('');
  const [sourceFilter, setSourceFilter] = useState('');
  const [sortBy, setSortBy] = useState('');
  const [page, setPage] = useState(1);
  const [limit] = useState(20);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedAgent, setSelectedAgent] = useState(null);

  // Fetch agents with advanced search
  useEffect(() => {
    setLoading(true);
    setError('');
    const params = new URLSearchParams({
      q: query,
      type: typeFilter,
      tag: tagFilter,
      license: licenseFilter,
      source: sourceFilter,
      page,
      limit
    });
    fetch(`${API_BASE}/search/advanced?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        setAgents(data.results || []);
        setTotal(data.total || 0);
        setLoading(false);
      })
      .catch(e => {
        setError('Failed to load agents.');
        setLoading(false);
      });
  }, [query, typeFilter, tagFilter, licenseFilter, sourceFilter, page, limit]);

  // Extract unique filter values
  const types = unique(agents.map(a => a.type));
  const tags = unique(agents.flatMap(a => (a.tags || '').split(',').map(t => t.trim())));
  const licenses = unique(agents.map(a => a.license));
  const sources = unique(agents.map(a => a.source));

  // Add analytics
  const typeCounts = getCounts(agents, 'type');
  const sourceCounts = getCounts(agents, 'source');
  const tagCounts = getCounts(agents, 'tags');

  // Sorting logic
  const sortedAgents = [...agents];
  if (sortBy === 'stars') {
    sortedAgents.sort((a, b) => (parseInt(b.rating?.stars || 0) - parseInt(a.rating?.stars || 0)));
  } else if (sortBy === 'updated') {
    sortedAgents.sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated));
  } else if (sortBy === 'activity') {
    sortedAgents.sort((a, b) => (b.rating?.activity === 'high' ? 1 : -1));
  }

  const totalPages = Math.ceil(total / limit);

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>AI Agent Discovery</h1>
      <div style={{ display: 'flex', gap: 16, marginBottom: 24 }}>
        <input
          type="text"
          placeholder="Search agents..."
          value={query}
          onChange={e => { setQuery(e.target.value); setPage(1); }}
          style={{ width: 180, padding: 8 }}
        />
        <select value={typeFilter} onChange={e => { setTypeFilter(e.target.value); setPage(1); }}>
          <option value="">All Types</option>
          {types.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <select value={tagFilter} onChange={e => { setTagFilter(e.target.value); setPage(1); }}>
          <option value="">All Tags</option>
          {tags.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
        <select value={licenseFilter} onChange={e => { setLicenseFilter(e.target.value); setPage(1); }}>
          <option value="">All Licenses</option>
          {licenses.map(l => <option key={l} value={l}>{l}</option>)}
        </select>
        <select value={sourceFilter} onChange={e => { setSourceFilter(e.target.value); setPage(1); }}>
          <option value="">All Sources</option>
          {sources.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
          <option value="">Sort By</option>
          <option value="stars">Stars</option>
          <option value="activity">Activity</option>
          <option value="updated">Last Updated</option>
        </select>
        <button onClick={() => downloadCSV(agents, 'agents.csv')}>Export CSV</button>
        <button onClick={() => downloadJSON(agents, 'agents.json')}>Export JSON</button>
      </div>
      <div style={{ marginBottom: 24 }}>
        <b>Analytics:</b>
        <div>Types: {Object.entries(typeCounts).map(([k, v]) => `${k}: ${v}`).join(', ')}</div>
        <div>Sources: {Object.entries(sourceCounts).map(([k, v]) => `${k}: ${v}`).join(', ')}</div>
        <div>Top Tags: {Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([k, v]) => `${k}: ${v}`).join(', ')}</div>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        {sortedAgents.length === 0 && !loading && <p>No agents found.</p>}
        {sortedAgents.map(agent => (
          <div key={agent.id || agent.name} style={{ border: '1px solid #ccc', borderRadius: 8, padding: 16, marginBottom: 16, cursor: 'pointer' }}
            onClick={() => setSelectedAgent(agent)}>
            <h2>{agent.name}</h2>
            <p>{agent.description}</p>
            <p><b>Type:</b> {agent.type} | <b>Tags:</b> {agent.tags}</p>
            <p><b>Source:</b> {agent.source} | <b>License:</b> {agent.license}</p>
            <p><b>Last Updated:</b> {agent.last_updated}</p>
            <p><b>Stars:</b> {agent.rating?.stars || 0} | <b>Activity:</b> {agent.rating?.activity || 'unknown'}</p>
            <a href={agent.repo_link} target="_blank" rel="noopener noreferrer">Repo</a>
            {agent.demo_link && <span> | <a href={agent.demo_link} target="_blank" rel="noopener noreferrer">Demo</a></span>}
            {agent.paper_link && <span> | <a href={agent.paper_link} target="_blank" rel="noopener noreferrer">Paper</a></span>}
          </div>
        ))}
      </div>
      <div style={{ marginTop: 24 }}>
        {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
          <button
            key={p}
            onClick={() => setPage(p)}
            style={{ margin: 2, padding: 6, background: p === page ? '#007bff' : '#eee', color: p === page ? '#fff' : '#000', border: 'none', borderRadius: 4 }}
          >
            {p}
          </button>
        ))}
      </div>
      {selectedAgent && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.5)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          onClick={() => setSelectedAgent(null)}>
          <div style={{ background: '#fff', padding: 32, borderRadius: 12, minWidth: 320, maxWidth: 600 }} onClick={e => e.stopPropagation()}>
            <h2>{selectedAgent.name}</h2>
            <p>{selectedAgent.description}</p>
            <p><b>Type:</b> {selectedAgent.type}</p>
            <p><b>Tags:</b> {selectedAgent.tags}</p>
            <p><b>Source:</b> {selectedAgent.source}</p>
            <p><b>License:</b> {selectedAgent.license}</p>
            <p><b>Deployment:</b> {selectedAgent.deployment}</p>
            <p><b>Last Updated:</b> {selectedAgent.last_updated}</p>
            <p><b>Related:</b> {selectedAgent.related}</p>
            <p><b>Stars:</b> {selectedAgent.rating?.stars || 0}</p>
            <p><b>Activity:</b> {selectedAgent.rating?.activity || 'unknown'}</p>
            <p><b>Install:</b> {selectedAgent.install}</p>
            <a href={selectedAgent.repo_link} target="_blank" rel="noopener noreferrer">Repo</a>
            {selectedAgent.demo_link && <span> | <a href={selectedAgent.demo_link} target="_blank" rel="noopener noreferrer">Demo</a></span>}
            {selectedAgent.paper_link && <span> | <a href={selectedAgent.paper_link} target="_blank" rel="noopener noreferrer">Paper</a></span>}
            <div style={{ marginTop: 16 }}>
              <button onClick={() => setSelectedAgent(null)} style={{ padding: 8, borderRadius: 4, background: '#007bff', color: '#fff', border: 'none' }}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
