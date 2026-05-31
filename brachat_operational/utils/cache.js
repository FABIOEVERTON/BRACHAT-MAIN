// utils/cache.js
// Simple file-based cache with TTL (time-to-live) support.
// Stores cached entries in JSON format under .cache/cache.json.
// Usage:
//   const cache = require('./cache');
//   cache.set('key', value, ttlMs);
//   const val = cache.get('key'); // returns undefined if missing or expired.

const fs = require('fs');
const path = require('path');

const CACHE_DIR = path.resolve(__dirname);
const CACHE_FILE = path.join(CACHE_DIR, 'cache.json');

// Ensure cache file exists
function _init() {
  try {
    if (!fs.existsSync(CACHE_FILE)) {
      fs.writeFileSync(CACHE_FILE, JSON.stringify({}), 'utf8');
    }
  } catch (e) {
    // Silently ignore filesystem errors – cache is optional.
  }
}

function _readCache() {
  try {
    const data = fs.readFileSync(CACHE_FILE, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    return {};
  }
}

function _writeCache(cache) {
  try {
    fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf8');
  } catch (e) {
    // ignore
  }
}

/** Set a value in cache.
 * @param {string} key Cache key.
 * @param {*} value Value to store (JSON-serializable).
 * @param {number} ttlMs Time-to-live in milliseconds. Use 0 for no expiration.
 */
function set(key, value, ttlMs = 0) {
  const cache = _readCache();
  const expiresAt = ttlMs > 0 ? Date.now() + ttlMs : null;
  cache[key] = { value, expiresAt };
  _writeCache(cache);
}

/** Get a value from cache.
 * @param {string} key Cache key.
 * @returns {*} Value or undefined if missing/expired.
 */
function get(key) {
  const cache = _readCache();
  const entry = cache[key];
  if (!entry) return undefined;
  if (entry.expiresAt && Date.now() > entry.expiresAt) {
    // expired – delete
    delete cache[key];
    _writeCache(cache);
    return undefined;
  }
  return entry.value;
}

/** Delete a key from cache */
function del(key) {
  const cache = _readCache();
  if (key in cache) {
    delete cache[key];
    _writeCache(cache);
  }
}

/** Clear entire cache */
function clear() {
  _writeCache({});
}

_init();

module.exports = { set, get, del, clear };
