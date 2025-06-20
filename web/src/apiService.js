// API configuration for cloud deployment
const API_CONFIG = {
  // Production API URL (will be set via environment variable)
  PRODUCTION_URL: process.env.REACT_APP_API_URL || 'https://your-railway-app.railway.app',
  
  // Development API URL
  DEVELOPMENT_URL: 'http://localhost:8000',
  
  // Determine which URL to use
  getBaseURL: () => {
    // If we're in production (deployed), use the production URL
    if (process.env.NODE_ENV === 'production') {
      return API_CONFIG.PRODUCTION_URL;
    }
    // Otherwise use development URL
    return API_CONFIG.DEVELOPMENT_URL;
  }
};

// API service functions
export const apiService = {
  // Get base URL with /api prefix
  getBaseURL: () => `${API_CONFIG.getBaseURL()}/api`,

  // Fetch all agents with pagination
  async fetchAgents(page = 1, limit = 20) {
    try {
      const response = await fetch(`${this.getBaseURL()}/agents?page=${page}&limit=${limit}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching agents:', error);
      throw error;
    }
  },

  // Search agents
  async searchAgents(query) {
    try {
      const response = await fetch(`${this.getBaseURL()}/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Error searching agents:', error);
      throw error;
    }
  },

  // Advanced search
  async advancedSearch(params) {
    try {
      const queryString = new URLSearchParams(params).toString();
      const response = await fetch(`${this.getBaseURL()}/search/advanced?${queryString}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Error in advanced search:', error);
      throw error;
    }
  },

  // Get single agent
  async getAgent(id) {
    try {
      const response = await fetch(`${this.getBaseURL()}/agents/${id}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Error fetching agent:', error);
      throw error;
    }
  },

  // Export all agents
  async exportAgents() {
    try {
      const response = await fetch(`${this.getBaseURL()}/export`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Error exporting agents:', error);
      throw error;
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await fetch(`${API_CONFIG.getBaseURL()}/health`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
};

export default apiService;
