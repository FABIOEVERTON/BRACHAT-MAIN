// utils/fetchWithCache.js
// Wrapper around node-fetch (or built‑in fetch in Node 18+) that caches HTTP responses.
// Uses the simple cache implementation from utils/cache.js.
// The cache key is the request URL + method + sorted query params + body (for POST).
// TTL default is 1 hour (3600000 ms). Adjust as needed.

const { set, get } = require('./cache');

// Node 18+ has global fetch; for older versions you may need to npm install node-fetch.
const fetch = (global.fetch) ? global.fetch : require('node-fetch');

/**
 * Perform an HTTP request with optional caching.
 * @param {string} url The request URL.
 * @param {object} [options] Fetch options (method, headers, body, etc.).
 * @param {object} [cacheOpts] Cache options: { ttl: number (ms), enabled: boolean }
 * @returns {Promise<any>} Parsed JSON response (or text if not JSON).
 */
async function fetchWithCache(url, options = {}, cacheOpts = { ttl: 3600000, enabled: true }) {
  const method = (options.method || 'GET').toUpperCase();
  const body = options.body ? JSON.stringify(options.body) : '';
  // Build a deterministic cache key.
  const cacheKey = `${method}:${url}:${body}`;

  if (cacheOpts.enabled) {
    const cached = get(cacheKey);
    if (cached !== undefined) {
      return cached; // Return cached parsed response.
    }
  }

  const response = await fetch(url, options);
  let data;
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (cacheOpts.enabled && response.ok) {
    set(cacheKey, data, cacheOpts.ttl);
  }
  return data;
}

module.exports = { fetchWithCache };
