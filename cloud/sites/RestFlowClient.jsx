import React, { useState, useEffect, useRef, useMemo } from 'react';
import { 
  Play, Save, Trash2, Plus, FolderPlus, Folder, FileText, 
  Settings, Database, History, Download, Upload, Copy, Check, 
  X, HelpCircle, Edit2, CheckCircle2, AlertTriangle, Info,
  Send, Code, Globe, Server, ListFilter, Search, RefreshCw, Key, Shield, HardDrive
} from 'lucide-react';

// --- Default Data for Pre-population ---
const DEFAULT_ENVIRONMENTS = [
  {
    id: 'env-1',
    name: 'Production (HttpBin)',
    variables: [
      { key: 'baseUrl', value: 'https://httpbin.org', enabled: true },
      { key: 'apiKey', value: 'prod_sec_key_998877', enabled: true },
      { key: 'userId', value: '1002', enabled: true }
    ]
  },
  {
    id: 'env-2',
    name: 'Development (JSONPlaceholder)',
    variables: [
      { key: 'baseUrl', value: 'https://jsonplaceholder.typicode.com', enabled: true },
      { key: 'apiKey', value: 'dev_key_12345', enabled: true },
      { key: 'userId', value: '1', enabled: true }
    ]
  },
  {
    id: 'env-3',
    name: 'Local Mock Server',
    variables: [
      { key: 'baseUrl', value: 'mock://api', enabled: true },
      { key: 'apiKey', value: 'local_mock_token', enabled: true }
    ]
  }
];

const DEFAULT_COLLECTIONS = [
  {
    id: 'coll-1',
    name: 'JSONPlaceholder API',
    description: 'Endpoints for testing JSONPlaceholder placeholder resources.',
    requests: [
      {
        id: 'req-1-1',
        name: 'Get Posts List',
        method: 'GET',
        url: '{{baseUrl}}/posts',
        params: [{ key: '_limit', value: '5', enabled: true, id: 'p1' }],
        headers: [{ key: 'Accept', value: 'application/json', enabled: true, id: 'h1' }],
        auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
        bodyType: 'none',
        bodyRaw: ''
      },
      {
        id: 'req-1-2',
        name: 'Create New Post',
        method: 'POST',
        url: '{{baseUrl}}/posts',
        params: [],
        headers: [
          { key: 'Content-Type', value: 'application/json', enabled: true, id: 'h2' },
          { key: 'Authorization', value: 'Bearer {{apiKey}}', enabled: true, id: 'h3' }
        ],
        auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
        bodyType: 'json',
        bodyRaw: '{\n  "title": "Novo post BRACHAT",\n  "body": "Este é um teste do RestFlow executado com sucesso.",\n  "userId": {{userId}}\n}'
      },
      {
        id: 'req-1-3',
        name: 'Get Post Comments',
        method: 'GET',
        url: '{{baseUrl}}/posts/{{userId}}/comments',
        params: [],
        headers: [],
        auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
        bodyType: 'none',
        bodyRaw: ''
      }
    ]
  },
  {
    id: 'coll-2',
    name: 'HttpBin Helpers',
    description: 'HttpBin testing HTTP request & response service.',
    requests: [
      {
        id: 'req-2-1',
        name: 'GET Echo Test',
        method: 'GET',
        url: '{{baseUrl}}/anything',
        params: [{ key: 'teste', value: 'restflow', enabled: true, id: 'p2' }],
        headers: [],
        auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
        bodyType: 'none',
        bodyRaw: ''
      },
      {
        id: 'req-2-2',
        name: 'POST JSON Echo',
        method: 'POST',
        url: '{{baseUrl}}/post',
        params: [],
        headers: [{ key: 'Content-Type', value: 'application/json', enabled: true, id: 'h4' }],
        auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
        bodyType: 'json',
        bodyRaw: '{\n  "app": "RestFlow",\n  "status": "Online",\n  "features": ["Mocks", "Env Vars", "Collections"]\n}'
      },
      {
        id: 'req-2-3',
        name: 'Simulate Delay',
        method: 'GET',
        url: '{{baseUrl}}/delay/2',
        params: [],
        headers: [],
        auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
        bodyType: 'none',
        bodyRaw: ''
      }
    ]
  }
];

const DEFAULT_MOCK_ROUTES = [
  {
    id: 'mock-1',
    path: '/users',
    method: 'GET',
    statusCode: 200,
    delay: 300,
    body: '[\n  { "id": 1, "name": "Fábio Igor", "role": "CEO & Architect" },\n  { "id": 2, "name": "Ezra", "role": "Central Core AI" },\n  { "id": 3, "name": "Nice", "role": "Home Governance" },\n  { "id": 4, "name": "Gilmario", "role": "Book Editor" }\n]'
  },
  {
    id: 'mock-2',
    path: '/users',
    method: 'POST',
    statusCode: 201,
    delay: 500,
    body: '{\n  "status": "success",\n  "message": "User created successfully inside mock database"\n}'
  },
  {
    id: 'mock-3',
    path: '/status/error',
    method: 'GET',
    statusCode: 500,
    delay: 100,
    body: '{\n  "error": "InternalServerError",\n  "message": "Simulated fail in local mock engine"\n}'
  }
];

export default function RestFlowClient() {
  // --- States ---
  const [collections, setCollections] = useState(() => {
    const saved = localStorage.getItem('restflow_collections');
    return saved ? JSON.parse(saved) : DEFAULT_COLLECTIONS;
  });
  const [environments, setEnvironments] = useState(() => {
    const saved = localStorage.getItem('restflow_environments');
    return saved ? JSON.parse(saved) : DEFAULT_ENVIRONMENTS;
  });
  const [activeEnvId, setActiveEnvId] = useState(() => {
    const saved = localStorage.getItem('restflow_active_env_id');
    return saved || DEFAULT_ENVIRONMENTS[0].id;
  });
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('restflow_history');
    return saved ? JSON.parse(saved) : [];
  });
  const [mockRoutes, setMockRoutes] = useState(() => {
    const saved = localStorage.getItem('restflow_mock_routes');
    return saved ? JSON.parse(saved) : DEFAULT_MOCK_ROUTES;
  });

  // Sidebar Tab
  const [sidebarTab, setSidebarTab] = useState('collections'); // 'collections' | 'history' | 'environments' | 'mocks'
  const [activeReqId, setActiveReqId] = useState('req-1-1'); // Currently selected request ID

  // Current Working Request State
  const [currentRequest, setCurrentRequest] = useState({
    name: 'Get Posts List',
    method: 'GET',
    url: '{{baseUrl}}/posts',
    params: [{ key: '_limit', value: '5', enabled: true, id: 'p1' }],
    headers: [{ key: 'Accept', value: 'application/json', enabled: true, id: 'h1' }],
    auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
    bodyType: 'none',
    bodyRaw: ''
  });

  // Response Viewer State
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [abortController, setAbortController] = useState(null);

  // Search & Filter States
  const [searchQuery, setSearchQuery] = useState('');
  const [respSearchQuery, setRespSearchQuery] = useState('');
  
  // Tab within Request builder
  const [requestTab, setRequestTab] = useState('params'); // 'params' | 'headers' | 'body' | 'auth' | 'codegen'
  // Tab within Response viewer
  const [responseTab, setResponseTab] = useState('body'); // 'body' | 'headers' | 'logs'
  // Code generation target
  const [codeTarget, setCodeTarget] = useState('curl'); // 'curl' | 'fetch' | 'axios' | 'python'
  
  // UI Modals / Toggles
  const [editEnvId, setEditEnvId] = useState(null);
  const [copiedNotification, setCopiedNotification] = useState(false);
  const [importExportOpen, setImportExportOpen] = useState(false);
  const [importJson, setImportJson] = useState('');
  const [importError, setImportError] = useState('');
  const [newCollName, setNewCollName] = useState('');
  const [isEditingReqName, setIsEditingReqName] = useState(false);
  const [editingReqNameValue, setEditingReqNameValue] = useState('');

  // Save to Local Storage on Change
  useEffect(() => {
    localStorage.setItem('restflow_collections', JSON.stringify(collections));
  }, [collections]);

  useEffect(() => {
    localStorage.setItem('restflow_environments', JSON.stringify(environments));
  }, [environments]);

  useEffect(() => {
    localStorage.setItem('restflow_active_env_id', activeEnvId);
  }, [activeEnvId]);

  useEffect(() => {
    localStorage.setItem('restflow_history', JSON.stringify(history));
  }, [history]);

  useEffect(() => {
    localStorage.setItem('restflow_mock_routes', JSON.stringify(mockRoutes));
  }, [mockRoutes]);

  // Load a request from a collection or history
  const loadRequest = (req) => {
    setCurrentRequest({
      name: req.name || 'Request',
      method: req.method || 'GET',
      url: req.url || '',
      params: req.params ? JSON.parse(JSON.stringify(req.params)) : [],
      headers: req.headers ? JSON.parse(JSON.stringify(req.headers)) : [],
      auth: req.auth ? { ...req.auth } : { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
      bodyType: req.bodyType || 'none',
      bodyRaw: req.bodyRaw || ''
    });
    setIsEditingReqName(false);
    setResponse(null);
  };

  // Sync back currentRequest updates to the main collection state
  const saveCurrentRequestToCollection = () => {
    setCollections(prev => {
      return prev.map(c => {
        const found = c.requests.some(r => r.id === activeReqId);
        if (!found) return c;
        return {
          ...c,
          requests: c.requests.map(r => {
            if (r.id !== activeReqId) return r;
            return {
              ...r,
              ...currentRequest
            };
          })
        };
      });
    });
    // Trigger simple alert/notification toast
    triggerToast();
  };

  const [toastMessage, setToastMessage] = useState('');
  const triggerToast = (msg = "Request salva!") => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 2500);
  };

  // Active Environment
  const activeEnvironment = useMemo(() => {
    return environments.find(e => e.id === activeEnvId) || null;
  }, [environments, activeEnvId]);

  // Resolve Environment variables in any given string
  const resolveEnvVars = (str) => {
    if (!str) return '';
    if (!activeEnvironment) return str;
    let resolved = str;
    activeEnvironment.variables.forEach(v => {
      if (v.enabled && v.key) {
        // Safe global regex replacement
        const regex = new RegExp(`{{\\s*${v.key}\\s*}}`, 'g');
        resolved = resolved.replace(regex, v.value);
      }
    });
    return resolved;
  };

  // Sync URL query params with the params table
  const handleUrlChange = (newUrl) => {
    setCurrentRequest(prev => {
      const updated = { ...prev, url: newUrl };
      
      // Attempt to extract query parameters
      try {
        const urlObj = new URL(resolveEnvVars(newUrl));
        const urlParams = [];
        urlObj.searchParams.forEach((value, key) => {
          urlParams.push({ key, value, enabled: true, id: Math.random().toString() });
        });

        // Merging logic: replace current enabled params with new ones from URL
        // while preserving existing headers/auth/etc.
        if (urlParams.length > 0) {
          // Keep existing params that are disabled, but override/add the ones from the URL
          const disabledParams = prev.params.filter(p => !p.enabled);
          updated.params = [...urlParams, ...disabledParams];
        }
      } catch (e) {
        // If URL is invalid or containing variables, we don't force parse
      }

      return updated;
    });
  };

  // Update URL string when params table is modified
  const updateUrlFromParams = (updatedParams) => {
    setCurrentRequest(prev => {
      let baseUrlPart = prev.url.split('?')[0];
      const queryParts = updatedParams
        .filter(p => p.enabled && p.key)
        .map(p => `${encodeURIComponent(p.key)}=${encodeURIComponent(p.value)}`);

      const newUrl = queryParts.length > 0 
        ? `${baseUrlPart}?${queryParts.join('&')}` 
        : baseUrlPart;

      return {
        ...prev,
        params: updatedParams,
        url: newUrl
      };
    });
  };

  // Execute Request (Supports real fetch & mock simulation)
  const sendRequest = async () => {
    if (isLoading) {
      if (abortController) abortController.abort();
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setResponse(null);

    const controller = new AbortController();
    setAbortController(controller);

    const startTime = performance.now();
    const resolvedUrl = resolveEnvVars(currentRequest.url);
    const resolvedMethod = currentRequest.method;
    
    // Check if the URL matches a mock route
    // Matches if URL starts with mock:// or matches the mock path in mock server mode
    const isMock = resolvedUrl.startsWith('mock://') || 
                   mockRoutes.some(r => resolvedUrl.endsWith(r.path) && r.method === resolvedMethod);

    if (isMock) {
      // Find the mock route
      const cleanPath = resolvedUrl.replace(/^mock:\/\/[^/]+/, '').split('?')[0];
      const route = mockRoutes.find(r => 
        (r.path === cleanPath || resolvedUrl.endsWith(r.path)) && r.method === resolvedMethod
      );

      // Simulate network latency
      const delay = route ? route.delay : 300;
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(resolve, delay);
        controller.signal.addEventListener('abort', () => {
          clearTimeout(timeout);
          reject(new DOMException('Aborted', 'AbortError'));
        });
      });

      const endTime = performance.now();
      const duration = Math.round(endTime - startTime);

      if (route) {
        let parsedBody = route.body;
        try {
          parsedBody = JSON.stringify(JSON.parse(route.body), null, 2);
        } catch(e) {}

        const mockResp = {
          status: route.statusCode,
          statusText: route.statusCode === 200 ? 'OK' : route.statusCode === 201 ? 'Created' : 'Mock Response',
          headers: {
            'content-type': 'application/json',
            'x-powered-by': 'RestFlow Mock Engine',
            'cache-control': 'no-cache'
          },
          body: parsedBody,
          time: duration,
          size: (new Blob([parsedBody]).size / 1024).toFixed(2) + ' KB',
          isMock: true
        };
        setResponse(mockResp);
        
        // Add to history
        addHistoryItem(resolvedMethod, currentRequest.url, route.statusCode, duration, mockResp.size);
      } else {
        const failResp = {
          status: 404,
          statusText: 'Not Found (Mock)',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ error: "Mock route not found", path: cleanPath, method: resolvedMethod }, null, 2),
          time: duration,
          size: '0.1 KB',
          isMock: true
        };
        setResponse(failResp);
        addHistoryItem(resolvedMethod, currentRequest.url, 404, duration, '0.1 KB');
      }
      setIsLoading(false);
      return;
    }

    // Real HTTP Fetch execution
    try {
      // Build Headers
      const headersObj = {};
      currentRequest.headers.forEach(h => {
        if (h.enabled && h.key) {
          headersObj[h.key] = resolveEnvVars(h.value);
        }
      });

      // Apply Auth Headers
      if (currentRequest.auth.type === 'bearer' && currentRequest.auth.token) {
        headersObj['Authorization'] = `Bearer ${resolveEnvVars(currentRequest.auth.token)}`;
      } else if (currentRequest.auth.type === 'basic' && (currentRequest.auth.username || currentRequest.auth.password)) {
        const creds = btoa(`${resolveEnvVars(currentRequest.auth.username)}:${resolveEnvVars(currentRequest.auth.password)}`);
        headersObj['Authorization'] = `Basic ${creds}`;
      } else if (currentRequest.auth.type === 'apikey' && currentRequest.auth.apiKey) {
        headersObj[resolveEnvVars(currentRequest.auth.apiKey)] = resolveEnvVars(currentRequest.auth.apiKeyVal);
      }

      // Build Fetch Request Options
      const options = {
        method: resolvedMethod,
        headers: headersObj,
        signal: controller.signal
      };

      // Set Body if applicable
      if (resolvedMethod !== 'GET' && resolvedMethod !== 'HEAD' && currentRequest.bodyType !== 'none') {
        if (currentRequest.bodyType === 'json') {
          options.body = resolveEnvVars(currentRequest.bodyRaw);
        } else if (currentRequest.bodyType === 'form-data' || currentRequest.bodyType === 'urlencoded') {
          // Just send raw text formatted for form-data
          options.body = resolveEnvVars(currentRequest.bodyRaw);
        }
      }

      // Perform Fetch
      const res = await fetch(resolvedUrl, options);
      const endTime = performance.now();
      const duration = Math.round(endTime - startTime);

      const responseHeaders = {};
      res.headers.forEach((val, key) => {
        responseHeaders[key] = val;
      });

      let responseText = '';
      try {
        responseText = await res.text();
        // Try pretty printing if JSON
        const parsed = JSON.parse(responseText);
        responseText = JSON.stringify(parsed, null, 2);
      } catch (e) {
        // Leave as raw text if not JSON
      }

      const sizeInKb = (new Blob([responseText]).size / 1024).toFixed(2);

      const successResp = {
        status: res.status,
        statusText: res.statusText || 'OK',
        headers: responseHeaders,
        body: responseText,
        time: duration,
        size: `${sizeInKb} KB`,
        isMock: false
      };

      setResponse(successResp);
      addHistoryItem(resolvedMethod, currentRequest.url, res.status, duration, `${sizeInKb} KB`);

    } catch (err) {
      const endTime = performance.now();
      const duration = Math.round(endTime - startTime);
      
      let errMsg = err.message || 'Erro de rede ou CORS.';
      
      // Render beautiful detailed CORS assistance block
      const errResp = {
        status: 0,
        statusText: 'Network / CORS Error',
        headers: {},
        body: `Error: ${errMsg}\n\n[Dica de Diagnóstico]:\n` +
              `1. A API destino pode não suportar requisições cross-origin (CORS) vindas do seu navegador.\n` + 
              `2. O endereço pode estar inacessível ou incorreto.\n\n` +
              `Dica de Teste Rápido:\n` +
              `Experimente usar o "Local Mock Server" selecionando ele no topo e alterando a URL para: \`mock://api/users\``,
        time: duration,
        size: '0 KB',
        error: true
      };
      setResponse(errResp);
      addHistoryItem(resolvedMethod, currentRequest.url, 'ERR', duration, '0 KB');
    } finally {
      setIsLoading(false);
    }
  };

  const addHistoryItem = (method, url, status, time, size) => {
    const item = {
      id: Math.random().toString(),
      name: currentRequest.name,
      method,
      url,
      status,
      time,
      size,
      timestamp: new Date().toLocaleTimeString()
    };
    setHistory(prev => [item, ...prev].slice(0, 50)); // Keep last 50 items
  };

  // Helper colors for HTTP Methods
  const getMethodColor = (m) => {
    switch (m?.toUpperCase()) {
      case 'GET': return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
      case 'POST': return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'PUT': return 'text-sky-400 bg-sky-500/10 border-sky-500/20';
      case 'DELETE': return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
      case 'PATCH': return 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20';
      default: return 'text-slate-400 bg-slate-500/10 border-slate-500/20';
    }
  };

  // Code Generation Snippet Builder
  const generatedCode = useMemo(() => {
    const resolvedUrl = resolveEnvVars(currentRequest.url);
    const method = currentRequest.method;
    const headers = currentRequest.headers.filter(h => h.enabled && h.key);
    
    // Add auth headers to code gen
    const allHeaders = [...headers];
    if (currentRequest.auth.type === 'bearer' && currentRequest.auth.token) {
      allHeaders.push({ key: 'Authorization', value: `Bearer ${currentRequest.auth.token}` });
    } else if (currentRequest.auth.type === 'basic' && (currentRequest.auth.username || currentRequest.auth.password)) {
      const creds = btoa(`${currentRequest.auth.username}:${currentRequest.auth.password}`);
      allHeaders.push({ key: 'Authorization', value: `Basic ${creds}` });
    } else if (currentRequest.auth.type === 'apikey' && currentRequest.auth.apiKey) {
      allHeaders.push({ key: currentRequest.auth.apiKey, value: currentRequest.auth.apiKeyVal });
    }

    if (codeTarget === 'curl') {
      let headersStr = allHeaders.map(h => `  -H "${h.key}: ${h.value}" \\\n`).join('');
      let dataStr = '';
      if (method !== 'GET' && currentRequest.bodyType !== 'none' && currentRequest.bodyRaw) {
        dataStr = `  -d '${currentRequest.bodyRaw.replace(/'/g, "'\\''")}' \\\n`;
      }
      return `curl -X ${method} "${resolvedUrl}" \\\n${headersStr}${dataStr}  -i`;
    }

    if (codeTarget === 'fetch') {
      const fetchHeaders = {};
      allHeaders.forEach(h => { fetchHeaders[h.key] = h.value; });
      const options = { method };
      if (Object.keys(fetchHeaders).length > 0) options.headers = fetchHeaders;
      if (method !== 'GET' && currentRequest.bodyType !== 'none' && currentRequest.bodyRaw) {
        options.body = currentRequest.bodyRaw;
      }
      return `fetch("${resolvedUrl}", ${JSON.stringify(options, null, 2)})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));`;
    }

    if (codeTarget === 'axios') {
      const axiosHeaders = {};
      allHeaders.forEach(h => { axiosHeaders[h.key] = h.value; });
      let dataBlock = '';
      if (method !== 'GET' && currentRequest.bodyType !== 'none' && currentRequest.bodyRaw) {
        try {
          dataBlock = `, \n  data: ${JSON.stringify(JSON.parse(currentRequest.bodyRaw), null, 2)}`;
        } catch(e) {
          dataBlock = `, \n  data: ${JSON.stringify(currentRequest.bodyRaw)}`;
        }
      }
      return `const axios = require('axios');

axios({
  method: '${method.toLowerCase()}',
  url: '${resolvedUrl}',
  headers: ${JSON.stringify(axiosHeaders, null, 4)}${dataBlock}
})
.then(response => {
  console.log(response.data);
})
.catch(error => {
  console.error(error);
});`;
    }

    if (codeTarget === 'python') {
      let headerLines = allHeaders.map(h => `    "${h.key}": "${h.value}"`).join(',\n');
      let dataLine = '';
      if (method !== 'GET' && currentRequest.bodyType !== 'none' && currentRequest.bodyRaw) {
        try {
          dataLine = `\ndata = ${JSON.stringify(JSON.parse(currentRequest.bodyRaw), null, 4)}`;
        } catch (e) {
          dataLine = `\ndata = """${currentRequest.bodyRaw}"""`;
        }
      }
      return `import requests

url = "${resolvedUrl}"
headers = {
${headerLines || '    "Accept": "application/json"'}
}
${dataLine ? dataLine + '\nresponse = requests.' + method.toLowerCase() + '(url, headers=headers, json=data)' : 'response = requests.' + method.toLowerCase() + '(url, headers=headers)'}

print(response.status_code)
print(response.json())`;
    }

    return '';
  }, [currentRequest, codeTarget, activeEnvId, environments]);

  // Utility to copy code to clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedNotification(true);
    setTimeout(() => setCopiedNotification(false), 2000);
  };

  // CRUD Collections
  const handleCreateCollection = () => {
    if (!newCollName.trim()) return;
    const newColl = {
      id: 'coll-' + Math.random().toString(),
      name: newCollName,
      description: 'Nova coleção de APIs',
      requests: []
    };
    setCollections(prev => [...prev, newColl]);
    setNewCollName('');
    triggerToast("Coleção criada!");
  };

  const handleCreateRequest = (collectionId) => {
    const newReqId = 'req-' + Math.random().toString();
    const newReq = {
      id: newReqId,
      name: 'Nova Requisição',
      method: 'GET',
      url: '{{baseUrl}}/users',
      params: [],
      headers: [],
      auth: { type: 'none', token: '', username: '', password: '', apiKey: '', apiKeyVal: '' },
      bodyType: 'none',
      bodyRaw: ''
    };

    setCollections(prev => prev.map(c => {
      if (c.id !== collectionId) return c;
      return {
        ...c,
        requests: [...c.requests, newReq]
      };
    }));
    setActiveReqId(newReqId);
    loadRequest(newReq);
    triggerToast("Requisição criada!");
  };

  const handleDeleteRequest = (collectionId, reqId) => {
    setCollections(prev => prev.map(c => {
      if (c.id !== collectionId) return c;
      return {
        ...c,
        requests: c.requests.filter(r => r.id !== reqId)
      };
    }));
    triggerToast("Requisição removida");
  };

  // CRUD Environments
  const handleAddEnv = () => {
    const newEnv = {
      id: 'env-' + Math.random().toString(),
      name: 'Novo Ambiente',
      variables: [
        { key: 'baseUrl', value: 'https://api.exemplo.com', enabled: true }
      ]
    };
    setEnvironments(prev => [...prev, newEnv]);
    setEditEnvId(newEnv.id);
  };

  const handleUpdateEnvVar = (envId, varIndex, field, value) => {
    setEnvironments(prev => prev.map(env => {
      if (env.id !== envId) return env;
      const updatedVars = [...env.variables];
      updatedVars[varIndex] = { ...updatedVars[varIndex], [field]: value };
      return { ...env, variables: updatedVars };
    }));
  };

  const handleAddEnvVar = (envId) => {
    setEnvironments(prev => prev.map(env => {
      if (env.id !== envId) return env;
      return {
        ...env,
        variables: [...env.variables, { key: '', value: '', enabled: true }]
      };
    }));
  };

  const handleRemoveEnvVar = (envId, varIndex) => {
    setEnvironments(prev => prev.map(env => {
      if (env.id !== envId) return env;
      return {
        ...env,
        variables: env.variables.filter((_, i) => i !== varIndex)
      };
    }));
  };

  // CRUD Mocks
  const handleAddMockRoute = () => {
    const newMock = {
      id: 'mock-' + Math.random().toString(),
      path: '/new-endpoint',
      method: 'GET',
      statusCode: 200,
      delay: 200,
      body: '{\n  "message": "Olá do seu servidor mock local!"\n}'
    };
    setMockRoutes(prev => [...prev, newMock]);
    triggerToast("Mock Route criado!");
  };

  const handleRemoveMockRoute = (id) => {
    setMockRoutes(prev => prev.filter(r => r.id !== id));
    triggerToast("Mock Route removido");
  };

  const handleUpdateMockRoute = (id, field, value) => {
    setMockRoutes(prev => prev.map(r => {
      if (r.id !== id) return r;
      return { ...r, [field]: value };
    }));
  };

  // JSON Import & Export
  const handleExportAll = () => {
    const allData = {
      version: "1.0.0",
      collections,
      environments,
      mockRoutes
    };
    const blob = new Blob([JSON.stringify(allData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `restflow_export_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const handleImport = () => {
    try {
      const parsed = JSON.parse(importJson);
      if (parsed.collections) setCollections(parsed.collections);
      if (parsed.environments) setEnvironments(parsed.environments);
      if (parsed.mockRoutes) setMockRoutes(parsed.mockRoutes);
      setImportExportOpen(false);
      setImportJson('');
      setImportError('');
      triggerToast("Importado com sucesso!");
    } catch (e) {
      setImportError('JSON inválido. Certifique-se de que o formato está correto.');
    }
  };

  // Search inside response body
  const filteredResponseBody = useMemo(() => {
    if (!response || !response.body) return '';
    if (!respSearchQuery.trim()) return response.body;

    const lines = response.body.split('\n');
    return lines
      .map((line, idx) => {
        if (line.toLowerCase().includes(respSearchQuery.toLowerCase())) {
          return `[Linha ${idx + 1}] >>> ${line}`;
        }
        return null;
      })
      .filter(Boolean)
      .join('\n') || '// Nenhuma correspondência encontrada';
  }, [response, respSearchQuery]);

  // Sync request name edit
  const saveReqName = () => {
    if (editingReqNameValue.trim()) {
      setCurrentRequest(p => ({ ...p, name: editingReqNameValue }));
      setCollections(prev => prev.map(c => ({
        ...c,
        requests: c.requests.map(r => r.id === activeReqId ? { ...r, name: editingReqNameValue } : r)
      })));
      setIsEditingReqName(false);
    }
  };

  return (
    <div className="flex flex-col h-screen w-full bg-slate-950 text-slate-100 font-sans overflow-hidden select-none">
      
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 bg-indigo-600 text-white py-3 px-5 rounded-lg shadow-xl border border-indigo-400/30 flex items-center gap-2 animate-bounce z-50">
          <CheckCircle2 size={18} />
          <span className="text-sm font-semibold">{toastMessage}</span>
        </div>
      )}

      {/* Top Header */}
      <header className="h-14 border-b border-slate-800 bg-slate-900/60 backdrop-blur-md px-4 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Globe size={18} className="text-white animate-pulse" />
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-wider text-slate-100 uppercase">RestFlow</h1>
            <span className="text-[10px] text-slate-400 font-medium block -mt-1">ECOSSISTEMA BRACHÁT API ENGINE</span>
          </div>
        </div>

        {/* Environment and Global Actions */}
        <div className="flex items-center gap-3">
          {/* Active Env Selector */}
          <div className="flex items-center gap-2 bg-slate-800/80 border border-slate-700/60 rounded-lg px-2.5 py-1.5">
            <Database size={14} className="text-indigo-400" />
            <select 
              value={activeEnvId}
              onChange={(e) => setActiveEnvId(e.target.value)}
              className="bg-transparent text-xs text-slate-200 outline-none border-none cursor-pointer font-medium max-w-[150px] truncate"
            >
              {environments.map(env => (
                <option key={env.id} value={env.id} className="bg-slate-900 text-slate-200">
                  {env.name}
                </option>
              ))}
            </select>
          </div>

          <button 
            onClick={() => setImportExportOpen(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs text-slate-300 rounded-lg transition-all"
          >
            <Upload size={13} />
            <span>Import / Export</span>
          </button>
        </div>
      </header>

      {/* Main Container */}
      <div className="flex flex-1 overflow-hidden">
        
        {/* Left Sidebar */}
        <aside className="w-80 border-r border-slate-800 bg-slate-900/40 flex flex-col shrink-0">
          {/* Tabs header */}
          <div className="grid grid-cols-4 border-b border-slate-800 text-center text-xs font-semibold text-slate-400 shrink-0">
            <button 
              onClick={() => setSidebarTab('collections')}
              className={`py-3 transition-colors border-b-2 ${sidebarTab === 'collections' ? 'border-indigo-500 text-indigo-400 bg-slate-800/20' : 'border-transparent hover:text-slate-200'}`}
            >
              Coleções
            </button>
            <button 
              onClick={() => setSidebarTab('history')}
              className={`py-3 transition-colors border-b-2 ${sidebarTab === 'history' ? 'border-indigo-500 text-indigo-400 bg-slate-800/20' : 'border-transparent hover:text-slate-200'}`}
            >
              Histórico
            </button>
            <button 
              onClick={() => setSidebarTab('environments')}
              className={`py-3 transition-colors border-b-2 ${sidebarTab === 'environments' ? 'border-indigo-500 text-indigo-400 bg-slate-800/20' : 'border-transparent hover:text-slate-200'}`}
            >
              Envs
            </button>
            <button 
              onClick={() => setSidebarTab('mocks')}
              className={`py-3 transition-colors border-b-2 ${sidebarTab === 'mocks' ? 'border-indigo-500 text-indigo-400 bg-slate-800/20' : 'border-transparent hover:text-slate-200'}`}
            >
              Mocks
            </button>
          </div>

          {/* Tab content */}
          <div className="flex-1 overflow-y-auto p-3.5 space-y-4">
            
            {/* COLLECTIONS TAB */}
            {sidebarTab === 'collections' && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Coleções</span>
                  <div className="flex items-center gap-1">
                    <input 
                      type="text" 
                      placeholder="Nova col..." 
                      value={newCollName}
                      onChange={(e) => setNewCollName(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleCreateCollection()}
                      className="bg-slate-800 border border-slate-700/60 rounded px-1.5 py-0.5 text-[11px] outline-none text-slate-200 w-24 focus:border-indigo-500"
                    />
                    <button 
                      onClick={handleCreateCollection}
                      className="p-1 hover:bg-slate-800 rounded text-slate-400 hover:text-white"
                      title="Criar Coleção"
                    >
                      <Plus size={14} />
                    </button>
                  </div>
                </div>

                <div className="space-y-2">
                  {collections.map(c => (
                    <div key={c.id} className="border border-slate-800/80 rounded-lg p-2 bg-slate-900/20">
                      <div className="flex items-center justify-between mb-1 pb-1 border-b border-slate-800/50">
                        <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300">
                          <Folder size={14} className="text-amber-500" />
                          <span className="truncate max-w-[120px]">{c.name}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <button 
                            onClick={() => handleCreateRequest(c.id)}
                            className="p-0.5 hover:bg-slate-800 rounded text-slate-400 hover:text-emerald-400"
                            title="Add Request"
                          >
                            <Plus size={13} />
                          </button>
                          <button 
                            onClick={() => {
                              setCollections(prev => prev.filter(item => item.id !== c.id));
                              triggerToast("Coleção deletada");
                            }}
                            className="p-0.5 hover:bg-slate-800 rounded text-slate-400 hover:text-rose-400"
                            title="Deletar Coleção"
                          >
                            <Trash2 size={13} />
                          </button>
                        </div>
                      </div>

                      {c.requests.length === 0 ? (
                        <div className="text-[10px] text-slate-500 italic p-1.5">Sem requisições</div>
                      ) : (
                        <div className="space-y-1 mt-1">
                          {c.requests.map(req => {
                            const isActive = req.id === activeReqId;
                            return (
                              <div 
                                key={req.id}
                                onClick={() => {
                                  setActiveReqId(req.id);
                                  loadRequest(req);
                                }}
                                className={`flex items-center justify-between p-1.5 rounded text-xs cursor-pointer transition-colors ${isActive ? 'bg-indigo-600/10 border border-indigo-500/20 text-white' : 'hover:bg-slate-800/40 text-slate-400'}`}
                              >
                                <div className="flex items-center gap-2 overflow-hidden">
                                  <span className={`text-[9px] font-extrabold px-1 py-0.5 rounded shrink-0 border ${getMethodColor(req.method)}`}>
                                    {req.method}
                                  </span>
                                  <span className="truncate">{req.name}</span>
                                </div>
                                <button 
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    handleDeleteRequest(c.id, req.id);
                                  }}
                                  className="opacity-0 group-hover:opacity-100 hover:text-rose-400 p-0.5"
                                  title="Deletar"
                                >
                                  <X size={11} />
                                </button>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* HISTORY TAB */}
            {sidebarTab === 'history' && (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Histórico Recente</span>
                  <button 
                    onClick={() => { setHistory([]); triggerToast("Histórico limpo!"); }}
                    className="text-[10px] text-rose-400 hover:underline flex items-center gap-1"
                  >
                    <Trash2 size={11} />
                    Limpar tudo
                  </button>
                </div>

                {history.length === 0 ? (
                  <div className="text-xs text-slate-500 italic text-center py-6">Nenhum histórico disponível</div>
                ) : (
                  <div className="space-y-1.5">
                    {history.map(item => (
                      <div 
                        key={item.id}
                        onClick={() => {
                          loadRequest(item);
                          triggerToast("Histórico carregado");
                        }}
                        className="p-2 bg-slate-900/40 hover:bg-slate-800/40 border border-slate-800 rounded-lg cursor-pointer transition-all flex items-center justify-between"
                      >
                        <div className="overflow-hidden space-y-0.5">
                          <div className="flex items-center gap-1.5">
                            <span className={`text-[9px] font-extrabold px-1 py-0.2 rounded border ${getMethodColor(item.method)}`}>
                              {item.method}
                            </span>
                            <span className="text-xs text-slate-300 font-medium truncate">{item.name}</span>
                          </div>
                          <div className="text-[10px] text-slate-500 truncate">{item.url}</div>
                        </div>
                        <div className="text-right shrink-0">
                          <span className={`text-[10px] font-bold ${
                            typeof item.status === 'number' && item.status >= 200 && item.status < 300 
                              ? 'text-emerald-400' 
                              : 'text-rose-400'
                          }`}>
                            {item.status}
                          </span>
                          <span className="text-[9px] text-slate-500 block">{item.time}ms</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* ENVIRONMENTS TAB */}
            {sidebarTab === 'environments' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Ambientes</span>
                  <button 
                    onClick={handleAddEnv}
                    className="flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
                  >
                    <Plus size={13} />
                    Criar Novo
                  </button>
                </div>

                <div className="space-y-2">
                  {environments.map(env => {
                    const isEditing = editEnvId === env.id;
                    const isActive = env.id === activeEnvId;

                    return (
                      <div key={env.id} className={`border rounded-lg p-2.5 transition-all ${
                        isActive ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-slate-800 bg-slate-900/20'
                      }`}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <input 
                              type="checkbox" 
                              checked={isActive}
                              onChange={() => setActiveEnvId(env.id)}
                              className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0 cursor-pointer"
                            />
                            {isEditing ? (
                              <input 
                                type="text"
                                value={env.name}
                                onChange={(e) => {
                                  setEnvironments(prev => prev.map(item => item.id === env.id ? { ...item, name: e.target.value } : item));
                                }}
                                className="bg-slate-800 border border-slate-700 rounded px-1.5 py-0.5 text-xs text-white outline-none w-32"
                              />
                            ) : (
                              <span className="text-xs font-bold text-slate-300">{env.name}</span>
                            )}
                          </div>
                          <div className="flex items-center gap-1.5">
                            <button 
                              onClick={() => setEditEnvId(isEditing ? null : env.id)}
                              className="text-slate-400 hover:text-white"
                              title="Editar"
                            >
                              <Edit2 size={12} />
                            </button>
                            <button 
                              onClick={() => {
                                setEnvironments(prev => prev.filter(item => item.id !== env.id));
                                if (activeEnvId === env.id && environments.length > 1) {
                                  setActiveEnvId(environments[0].id);
                                }
                                triggerToast("Ambiente deletado");
                              }}
                              className="text-slate-400 hover:text-rose-400"
                              title="Deletar"
                            >
                              <Trash2 size={12} />
                            </button>
                          </div>
                        </div>

                        {/* Variables list in environment */}
                        {isEditing && (
                          <div className="space-y-2 mt-2 pt-2 border-t border-slate-800/80">
                            {env.variables.map((v, varIndex) => (
                              <div key={varIndex} className="grid grid-cols-12 gap-1 items-center">
                                <input 
                                  type="text" 
                                  placeholder="Chave"
                                  value={v.key}
                                  onChange={(e) => handleUpdateEnvVar(env.id, varIndex, 'key', e.target.value)}
                                  className="col-span-5 bg-slate-900 border border-slate-800 rounded px-1.5 py-0.5 text-[10px] text-white outline-none"
                                />
                                <input 
                                  type="text" 
                                  placeholder="Valor"
                                  value={v.value}
                                  onChange={(e) => handleUpdateEnvVar(env.id, varIndex, 'value', e.target.value)}
                                  className="col-span-5 bg-slate-900 border border-slate-800 rounded px-1.5 py-0.5 text-[10px] text-white outline-none"
                                />
                                <button 
                                  onClick={() => handleRemoveEnvVar(env.id, varIndex)}
                                  className="col-span-2 text-rose-500 hover:text-rose-400 flex justify-center"
                                  title="Remover"
                                >
                                  <X size={12} />
                                </button>
                              </div>
                            ))}
                            <button 
                              onClick={() => handleAddEnvVar(env.id)}
                              className="text-[10px] text-indigo-400 hover:underline flex items-center gap-1 mt-1.5"
                            >
                              <Plus size={10} /> Add Variable
                            </button>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* MOCK SERVER ROUTES TAB */}
            {sidebarTab === 'mocks' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Mock Server</span>
                    <span className="text-[9px] text-slate-500">Substitui chamadas locais</span>
                  </div>
                  <button 
                    onClick={handleAddMockRoute}
                    className="flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 font-semibold"
                  >
                    <Plus size={13} />
                    Novo Route
                  </button>
                </div>

                <div className="space-y-2">
                  {mockRoutes.map(route => (
                    <div key={route.id} className="border border-slate-800 bg-slate-900/20 rounded-lg p-2.5 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className={`text-[9px] font-extrabold px-1.5 py-0.5 rounded border ${getMethodColor(route.method)}`}>
                          {route.method}
                        </span>
                        <button 
                          onClick={() => handleRemoveMockRoute(route.id)}
                          className="text-slate-500 hover:text-rose-400"
                        >
                          <Trash2 size={12} />
                        </button>
                      </div>

                      <div className="space-y-1">
                        <label className="text-[10px] text-slate-500 font-medium">Path</label>
                        <input 
                          type="text" 
                          value={route.path}
                          onChange={(e) => handleUpdateMockRoute(route.id, 'path', e.target.value)}
                          className="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs text-white outline-none"
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <label className="text-[10px] text-slate-500 font-medium">Status Code</label>
                          <input 
                            type="number" 
                            value={route.statusCode}
                            onChange={(e) => handleUpdateMockRoute(route.id, 'statusCode', parseInt(e.target.value))}
                            className="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs text-white outline-none"
                          />
                        </div>
                        <div>
                          <label className="text-[10px] text-slate-500 font-medium">Delay (ms)</label>
                          <input 
                            type="number" 
                            value={route.delay}
                            onChange={(e) => handleUpdateMockRoute(route.id, 'delay', parseInt(e.target.value))}
                            className="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs text-white outline-none"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="text-[10px] text-slate-500 font-medium">Corpo da Resposta (JSON/Texto)</label>
                        <textarea 
                          value={route.body}
                          onChange={(e) => handleUpdateMockRoute(route.id, 'body', e.target.value)}
                          rows={3}
                          className="w-full bg-slate-950 border border-slate-800 rounded p-1.5 text-[10px] text-slate-300 font-mono outline-none"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        </aside>

        {/* Central Workspace (Request + Response) */}
        <main className="flex-1 flex flex-col md:flex-row overflow-hidden bg-slate-950">
          
          {/* Left Panel: Request Builder */}
          <section className="flex-1 border-r border-slate-800 flex flex-col overflow-y-auto">
            {/* Request Name and Method Row */}
            <div className="p-4 border-b border-slate-800/80 bg-slate-900/20">
              <div className="flex items-center gap-2 mb-3">
                {isEditingReqName ? (
                  <div className="flex items-center gap-1.5 w-full">
                    <input 
                      type="text" 
                      value={editingReqNameValue}
                      onChange={(e) => setEditingReqNameValue(e.target.value)}
                      onBlur={saveReqName}
                      onKeyDown={(e) => e.key === 'Enter' && saveReqName()}
                      className="bg-slate-800 border border-slate-700 text-sm font-semibold rounded px-2.5 py-1 text-white outline-none w-full max-w-md"
                      autoFocus
                    />
                    <button 
                      onClick={saveReqName}
                      className="p-1.5 bg-indigo-600 hover:bg-indigo-500 rounded text-white"
                    >
                      <Check size={14} />
                    </button>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 group">
                    <h2 className="text-sm font-bold text-slate-200">{currentRequest.name}</h2>
                    <button 
                      onClick={() => {
                        setEditingReqNameValue(currentRequest.name);
                        setIsEditingReqName(true);
                      }}
                      className="text-slate-500 hover:text-slate-300 p-1 rounded transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <Edit2 size={13} />
                    </button>
                  </div>
                )}
              </div>

              {/* URL Bar */}
              <div className="flex gap-2">
                <select 
                  value={currentRequest.method}
                  onChange={(e) => setCurrentRequest(p => ({ ...p, method: e.target.value }))}
                  className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs font-extrabold text-slate-200 outline-none cursor-pointer"
                >
                  <option value="GET">GET</option>
                  <option value="POST">POST</option>
                  <option value="PUT">PUT</option>
                  <option value="DELETE">DELETE</option>
                  <option value="PATCH">PATCH</option>
                </select>

                <div className="flex-1 relative flex items-center">
                  <input 
                    type="text"
                    value={currentRequest.url}
                    onChange={(e) => handleUrlChange(e.target.value)}
                    placeholder="Insira a URL da API ou mock://..."
                    className="w-full bg-slate-900 border border-slate-700/80 rounded-lg pl-3 pr-10 py-2 text-xs text-slate-200 font-mono outline-none focus:border-indigo-500"
                  />
                  <div className="absolute right-3 text-[10px] font-bold text-indigo-400/80" title="Active Environment">
                    {activeEnvironment ? activeEnvironment.name.split(' ')[0] : 'None'}
                  </div>
                </div>

                <button 
                  onClick={sendRequest}
                  disabled={isLoading && !abortController}
                  className={`flex items-center gap-2 px-5 py-2 rounded-lg font-semibold text-xs tracking-wider transition-all shadow-lg ${
                    isLoading 
                      ? 'bg-rose-600 hover:bg-rose-700 text-white shadow-rose-600/10'
                      : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/20'
                  }`}
                >
                  {isLoading ? (
                    <>
                      <RefreshCw size={14} className="animate-spin" />
                      <span>ABORTAR</span>
                    </>
                  ) : (
                    <>
                      <Send size={14} />
                      <span>ENVIAR</span>
                    </>
                  )}
                </button>

                <button 
                  onClick={saveCurrentRequestToCollection}
                  className="p-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-slate-300"
                  title="Salvar na Coleção"
                >
                  <Save size={16} />
                </button>
              </div>
            </div>

            {/* Request Editor Tabs */}
            <div className="flex-1 flex flex-col min-h-0">
              <div className="flex border-b border-slate-800 text-xs text-slate-400 bg-slate-900/10 shrink-0">
                {['params', 'headers', 'body', 'auth', 'codegen'].map(tab => (
                  <button
                    key={tab}
                    onClick={() => setRequestTab(tab)}
                    className={`px-4 py-2.5 capitalize border-b-2 font-medium transition-colors ${
                      requestTab === tab 
                        ? 'border-indigo-500 text-indigo-400' 
                        : 'border-transparent hover:text-slate-200'
                    }`}
                  >
                    {tab === 'codegen' ? 'Código' : tab}
                  </button>
                ))}
              </div>

              <div className="flex-1 p-4 overflow-y-auto">
                
                {/* PARAMS TAB */}
                {requestTab === 'params' && (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-400">Query Parameters</span>
                      <span className="text-[10px] text-slate-500">Sincroniza automaticamente com a barra de URL</span>
                    </div>

                    <div className="space-y-2">
                      {currentRequest.params.map((param, index) => (
                        <div key={param.id || index} className="flex gap-2 items-center">
                          <input 
                            type="checkbox"
                            checked={param.enabled}
                            onChange={(e) => {
                              const updated = [...currentRequest.params];
                              updated[index].enabled = e.target.checked;
                              updateUrlFromParams(updated);
                            }}
                            className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
                          />
                          <input 
                            type="text" 
                            placeholder="Chave"
                            value={param.key}
                            onChange={(e) => {
                              const updated = [...currentRequest.params];
                              updated[index].key = e.target.value;
                              updateUrlFromParams(updated);
                            }}
                            className="w-1/2 bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none focus:border-slate-700"
                          />
                          <input 
                            type="text" 
                            placeholder="Valor"
                            value={param.value}
                            onChange={(e) => {
                              const updated = [...currentRequest.params];
                              updated[index].value = e.target.value;
                              updateUrlFromParams(updated);
                            }}
                            className="w-1/2 bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none focus:border-slate-700"
                          />
                          <button 
                            onClick={() => {
                              const updated = currentRequest.params.filter((_, i) => i !== index);
                              updateUrlFromParams(updated);
                            }}
                            className="text-rose-500 hover:text-rose-400 p-1"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      ))}

                      <button 
                        onClick={() => {
                          const updated = [...currentRequest.params, { key: '', value: '', enabled: true, id: Math.random().toString() }];
                          setCurrentRequest(p => ({ ...p, params: updated }));
                        }}
                        className="flex items-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 font-semibold mt-2"
                      >
                        <Plus size={14} /> Add Parameter
                      </button>
                    </div>
                  </div>
                )}

                {/* HEADERS TAB */}
                {requestTab === 'headers' && (
                  <div className="space-y-3">
                    <span className="text-xs font-bold text-slate-400 block">HTTP Request Headers</span>
                    
                    <div className="space-y-2">
                      {currentRequest.headers.map((h, index) => (
                        <div key={h.id || index} className="flex gap-2 items-center">
                          <input 
                            type="checkbox"
                            checked={h.enabled}
                            onChange={(e) => {
                              const updated = [...currentRequest.headers];
                              updated[index].enabled = e.target.checked;
                              setCurrentRequest(p => ({ ...p, headers: updated }));
                            }}
                            className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
                          />
                          <input 
                            type="text" 
                            placeholder="Header Key (ex: Content-Type)"
                            value={h.key}
                            onChange={(e) => {
                              const updated = [...currentRequest.headers];
                              updated[index].key = e.target.value;
                              setCurrentRequest(p => ({ ...p, headers: updated }));
                            }}
                            className="w-1/2 bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none focus:border-slate-700"
                          />
                          <input 
                            type="text" 
                            placeholder="Value"
                            value={h.value}
                            onChange={(e) => {
                              const updated = [...currentRequest.headers];
                              updated[index].value = e.target.value;
                              setCurrentRequest(p => ({ ...p, headers: updated }));
                            }}
                            className="w-1/2 bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none focus:border-slate-700"
                          />
                          <button 
                            onClick={() => {
                              const updated = currentRequest.headers.filter((_, i) => i !== index);
                              setCurrentRequest(p => ({ ...p, headers: updated }));
                            }}
                            className="text-rose-500 hover:text-rose-400 p-1"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      ))}

                      <button 
                        onClick={() => {
                          const updated = [...currentRequest.headers, { key: '', value: '', enabled: true, id: Math.random().toString() }];
                          setCurrentRequest(p => ({ ...p, headers: updated }));
                        }}
                        className="flex items-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 font-semibold mt-2"
                      >
                        <Plus size={14} /> Add Header
                      </button>
                    </div>
                  </div>
                )}

                {/* BODY TAB */}
                {requestTab === 'body' && (
                  <div className="space-y-4">
                    <div className="flex gap-4 border-b border-slate-800 pb-2 text-xs">
                      {['none', 'json', 'form-data'].map(type => (
                        <label key={type} className="flex items-center gap-1.5 cursor-pointer text-slate-300 hover:text-white capitalize">
                          <input 
                            type="radio" 
                            name="bodyType"
                            checked={currentRequest.bodyType === type}
                            onChange={() => setCurrentRequest(p => ({ ...p, bodyType: type }))}
                            className="text-indigo-600 bg-slate-900 border-slate-700 focus:ring-0"
                          />
                          {type}
                        </label>
                      ))}
                    </div>

                    {currentRequest.bodyType === 'none' && (
                      <div className="text-xs text-slate-500 italic py-6 text-center">Nenhum corpo de requisição será enviado.</div>
                    )}

                    {currentRequest.bodyType !== 'none' && (
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-slate-400 font-semibold font-mono">Payload Editor</span>
                          <span className="text-[10px] text-slate-500">Suporta variáveis {"{{key}}"}</span>
                        </div>
                        <textarea
                          value={currentRequest.bodyRaw}
                          onChange={(e) => setCurrentRequest(p => ({ ...p, bodyRaw: e.target.value }))}
                          placeholder={currentRequest.bodyType === 'json' ? '{\n  "name": "Fábio",\n  "city": "Brasilia"\n}' : 'chave1=valor1\nchave2=valor2'}
                          rows={12}
                          className="w-full bg-slate-900 border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-mono outline-none focus:border-slate-700"
                        />
                      </div>
                    )}
                  </div>
                )}

                {/* AUTH TAB */}
                {requestTab === 'auth' && (
                  <div className="space-y-4">
                    <div>
                      <label className="text-xs font-bold text-slate-400 block mb-1.5">Autenticação</label>
                      <select 
                        value={currentRequest.auth.type}
                        onChange={(e) => {
                          const updatedAuth = { ...currentRequest.auth, type: e.target.value };
                          setCurrentRequest(p => ({ ...p, auth: updatedAuth }));
                        }}
                        className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 outline-none w-full max-w-xs cursor-pointer"
                      >
                        <option value="none">Nenhuma</option>
                        <option value="bearer">Bearer Token</option>
                        <option value="basic">Basic Auth (User/Pass)</option>
                        <option value="apikey">API Key Header</option>
                      </select>
                    </div>

                    {currentRequest.auth.type === 'bearer' && (
                      <div className="space-y-1">
                        <label className="text-[11px] text-slate-500 font-semibold">Token</label>
                        <input 
                          type="password"
                          placeholder="Bearer token ou {{apiKey}}"
                          value={currentRequest.auth.token}
                          onChange={(e) => {
                            const updatedAuth = { ...currentRequest.auth, token: e.target.value };
                            setCurrentRequest(p => ({ ...p, auth: updatedAuth }));
                          }}
                          className="w-full max-w-md bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none"
                        />
                      </div>
                    )}

                    {currentRequest.auth.type === 'basic' && (
                      <div className="grid grid-cols-2 gap-3 max-w-md">
                        <div className="space-y-1">
                          <label className="text-[11px] text-slate-500 font-semibold">Username</label>
                          <input 
                            type="text"
                            placeholder="Usuario"
                            value={currentRequest.auth.username}
                            onChange={(e) => {
                              const updatedAuth = { ...currentRequest.auth, username: e.target.value };
                              setCurrentRequest(p => ({ ...p, auth: updatedAuth }));
                            }}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none"
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="text-[11px] text-slate-500 font-semibold">Password</label>
                          <input 
                            type="password"
                            placeholder="Senha"
                            value={currentRequest.auth.password}
                            onChange={(e) => {
                              const updatedAuth = { ...currentRequest.auth, password: e.target.value };
                              setCurrentRequest(p => ({ ...p, auth: updatedAuth }));
                            }}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none"
                          />
                        </div>
                      </div>
                    )}

                    {currentRequest.auth.type === 'apikey' && (
                      <div className="grid grid-cols-2 gap-3 max-w-md">
                        <div className="space-y-1">
                          <label className="text-[11px] text-slate-500 font-semibold">Header Name</label>
                          <input 
                            type="text"
                            placeholder="X-API-Key"
                            value={currentRequest.auth.apiKey}
                            onChange={(e) => {
                              const updatedAuth = { ...currentRequest.auth, apiKey: e.target.value };
                              setCurrentRequest(p => ({ ...p, auth: updatedAuth }));
                            }}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none"
                          />
                        </div>
                        <div className="space-y-1">
                          <label className="text-[11px] text-slate-500 font-semibold">Value</label>
                          <input 
                            type="text"
                            placeholder="Chave/Token"
                            value={currentRequest.auth.apiKeyVal}
                            onChange={(e) => {
                              const updatedAuth = { ...currentRequest.auth, apiKeyVal: e.target.value };
                              setCurrentRequest(p => ({ ...p, auth: updatedAuth }));
                            }}
                            className="w-full bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-200 font-mono outline-none"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* CODE GENERATOR TAB */}
                {requestTab === 'codegen' && (
                  <div className="space-y-4">
                    <div className="flex gap-2 bg-slate-900 p-1.5 rounded-lg border border-slate-800/80">
                      {[
                        { id: 'curl', label: 'cURL' },
                        { id: 'fetch', label: 'Fetch JS' },
                        { id: 'axios', label: 'Axios' },
                        { id: 'python', label: 'Python' }
                      ].map(t => (
                        <button
                          key={t.id}
                          onClick={() => setCodeTarget(t.id)}
                          className={`flex-1 py-1 rounded text-xs font-semibold transition-colors ${
                            codeTarget === t.id ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-slate-200'
                          }`}
                        >
                          {t.label}
                        </button>
                      ))}
                    </div>

                    <div className="relative">
                      <pre className="bg-slate-900/80 border border-slate-800 rounded-lg p-4 text-[11px] text-indigo-300 font-mono overflow-x-auto whitespace-pre-wrap max-h-96">
                        {generatedCode}
                      </pre>
                      <button 
                        onClick={() => copyToClipboard(generatedCode)}
                        className="absolute top-3 right-3 p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700/60"
                        title="Copiar código"
                      >
                        {copiedNotification ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
                      </button>
                    </div>
                  </div>
                )}

              </div>
            </div>
          </section>

          {/* Right Panel: Response Viewer */}
          <section className="flex-1 flex flex-col min-h-0 bg-slate-950/40">
            {/* Header info */}
            <div className="p-4 border-b border-slate-800 bg-slate-900/10 flex items-center justify-between min-h-[69px] shrink-0">
              <span className="text-xs font-bold text-slate-400">Response</span>

              {response ? (
                <div className="flex items-center gap-3">
                  {/* Status Code */}
                  <span className={`text-xs font-bold px-2 py-1 rounded border ${
                    response.status >= 200 && response.status < 300 
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                      : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                  }`}>
                    {response.status} {response.statusText}
                  </span>

                  {/* Latency */}
                  <span className="text-xs text-slate-400 font-medium">
                    {response.time} ms
                  </span>

                  {/* Data Size */}
                  <span className="text-xs text-slate-400 font-medium">
                    {response.size}
                  </span>

                  {response.isMock && (
                    <span className="text-[10px] font-semibold bg-violet-600/20 text-violet-400 px-2 py-0.5 rounded border border-violet-500/20">
                      Mocked
                    </span>
                  )}
                </div>
              ) : (
                <span className="text-xs text-slate-600 italic">Pronto para envio</span>
              )}
            </div>

            {/* Inner Content */}
            <div className="flex-1 flex flex-col min-h-0">
              
              {/* Response Tabs selector */}
              <div className="flex border-b border-slate-800 text-xs text-slate-400 bg-slate-900/10 shrink-0">
                <button
                  onClick={() => setResponseTab('body')}
                  className={`px-4 py-2.5 border-b-2 font-medium transition-colors ${
                    responseTab === 'body' ? 'border-indigo-500 text-indigo-400' : 'border-transparent hover:text-slate-200'
                  }`}
                >
                  Body
                </button>
                <button
                  onClick={() => setResponseTab('headers')}
                  className={`px-4 py-2.5 border-b-2 font-medium transition-colors ${
                    responseTab === 'headers' ? 'border-indigo-500 text-indigo-400' : 'border-transparent hover:text-slate-200'
                  }`}
                >
                  Headers
                </button>
                <button
                  onClick={() => setResponseTab('logs')}
                  className={`px-4 py-2.5 border-b-2 font-medium transition-colors ${
                    responseTab === 'logs' ? 'border-indigo-500 text-indigo-400' : 'border-transparent hover:text-slate-200'
                  }`}
                >
                  Logs de Rede
                </button>
              </div>

              {/* Tab Display Area */}
              <div className="flex-1 p-4 overflow-y-auto flex flex-col min-h-0">
                
                {isLoading && (
                  <div className="flex-1 flex flex-col items-center justify-center space-y-3">
                    <RefreshCw size={28} className="text-indigo-500 animate-spin" />
                    <span className="text-xs font-semibold text-slate-400">Aguardando resposta do servidor...</span>
                  </div>
                )}

                {!isLoading && !response && (
                  <div className="flex-1 flex flex-col items-center justify-center text-center space-y-2 p-8">
                    <HelpCircle size={36} className="text-slate-700" />
                    <span className="text-xs text-slate-500 font-semibold">Envie uma requisição para inspecionar os detalhes da resposta aqui.</span>
                  </div>
                )}

                {!isLoading && response && (
                  <div className="flex-1 flex flex-col min-h-0 space-y-4">
                    
                    {/* BODY TAB */}
                    {responseTab === 'body' && (
                      <div className="flex-1 flex flex-col min-h-0 space-y-3">
                        <div className="flex items-center justify-between shrink-0">
                          {/* Search bar inside response */}
                          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 rounded px-2 py-1 w-64">
                            <Search size={12} className="text-slate-500" />
                            <input 
                              type="text" 
                              placeholder="Filtrar resultado..." 
                              value={respSearchQuery}
                              onChange={(e) => setRespSearchQuery(e.target.value)}
                              className="bg-transparent text-[11px] text-slate-200 outline-none w-full"
                            />
                          </div>

                          <button 
                            onClick={() => copyToClipboard(response.body)}
                            className="flex items-center gap-1.5 px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 rounded border border-slate-700/60 transition-all"
                          >
                            <Copy size={12} />
                            <span>Copy Body</span>
                          </button>
                        </div>

                        <div className="flex-1 min-h-0 bg-slate-900/60 border border-slate-800 rounded-lg p-3 overflow-y-auto font-mono text-[11px] text-slate-300 whitespace-pre">
                          {filteredResponseBody}
                        </div>
                      </div>
                    )}

                    {/* HEADERS TAB */}
                    {responseTab === 'headers' && (
                      <div className="border border-slate-800 rounded-lg overflow-hidden">
                        <table className="min-w-full text-xs text-left text-slate-400">
                          <thead className="bg-slate-900/60 text-slate-300 border-b border-slate-800">
                            <tr>
                              <th className="px-4 py-2 font-bold">Header</th>
                              <th className="px-4 py-2 font-bold">Value</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-800/60">
                            {Object.entries(response.headers).length === 0 ? (
                              <tr>
                                <td colSpan="2" className="px-4 py-3 text-center text-slate-500 italic">Sem cabeçalhos na resposta</td>
                              </tr>
                            ) : (
                              Object.entries(response.headers).map(([k, v]) => (
                                <tr key={k} className="hover:bg-slate-900/20">
                                  <td className="px-4 py-2 font-semibold text-slate-300 font-mono select-text">{k}</td>
                                  <td className="px-4 py-2 text-slate-400 font-mono select-text break-all">{v}</td>
                                </tr>
                              ))
                            )}
                          </tbody>
                        </table>
                      </div>
                    )}

                    {/* NET LOGS TAB */}
                    {responseTab === 'logs' && (
                      <div className="space-y-3 font-mono text-[11px]">
                        <div className="p-3 bg-slate-900/60 border border-slate-800 rounded-lg space-y-2">
                          <div className="flex items-center gap-1 text-emerald-400">
                            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                            <span>[SYSTEM LOG] Conexão estabelecida com {currentRequest.url.includes('mock://') ? 'Mock Engine Local' : 'Servidor Remoto'}</span>
                          </div>
                          <div className="text-slate-400">
                            &gt; {currentRequest.method} {resolveEnvVars(currentRequest.url)} HTTP/1.1
                          </div>
                          {currentRequest.headers.map((h, i) => h.enabled && h.key && (
                            <div key={i} className="text-slate-500">&gt; {h.key}: {resolveEnvVars(h.value)}</div>
                          ))}
                          <div className="text-slate-500">&gt; Host: {new URL(resolveEnvVars(currentRequest.url).replace('mock://', 'http://')).host}</div>
                          <hr className="border-slate-800 my-1" />
                          <div className="text-slate-400">&lt; HTTP/1.1 {response.status} {response.statusText}</div>
                          <div className="text-slate-500">&lt; Time Elapsed: {response.time} ms</div>
                          <div className="text-slate-500">&lt; Content Length: {response.size}</div>
                        </div>
                      </div>
                    )}

                  </div>
                )}
              </div>
            </div>
          </section>

        </main>
      </div>

      {/* IMPORT / EXPORT MODAL */}
      {importExportOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 w-full max-w-xl space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
              <span className="text-sm font-bold text-slate-200">Importar / Exportar Dados</span>
              <button 
                onClick={() => setImportExportOpen(false)}
                className="text-slate-400 hover:text-white"
              >
                <X size={18} />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <span className="text-xs font-bold text-slate-400 block mb-1">Exportar</span>
                <p className="text-[11px] text-slate-500 mb-2">Gere e baixe um arquivo JSON contendo todas as suas Coleções, Variáveis de Ambiente e Mock Server.</p>
                <button 
                  onClick={handleExportAll}
                  className="flex items-center gap-1.5 px-3 py-2 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white rounded-lg transition-all"
                >
                  <Download size={14} />
                  Exportar JSON Completo
                </button>
              </div>

              <hr className="border-slate-800" />

              <div className="space-y-2">
                <span className="text-xs font-bold text-slate-400 block">Importar</span>
                <p className="text-[11px] text-slate-500">Cole o JSON exportado abaixo para restaurar configurações.</p>
                <textarea 
                  value={importJson}
                  onChange={(e) => setImportJson(e.target.value)}
                  placeholder='{ "collections": [...], "environments": [...] }'
                  rows={6}
                  className="w-full bg-slate-950 border border-slate-800 rounded p-2.5 text-xs text-slate-300 font-mono outline-none"
                />
                {importError && (
                  <span className="text-xs text-rose-500 block font-semibold">{importError}</span>
                )}
                <button 
                  onClick={handleImport}
                  className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700"
                >
                  Confirmar Importação
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer bar */}
      <footer className="h-8 border-t border-slate-800 bg-slate-900/60 px-4 flex items-center justify-between text-[11px] text-slate-500 shrink-0">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1 text-slate-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            Oracle VM: Active (147.15.18.252)
          </span>
          <span className="text-slate-600">|</span>
          <span className="flex items-center gap-1 text-rose-500 font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500"></span>
            Hetzner VPS: Inativo (Stopped)
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span>Atalho rápido: Ctrl + Enter para enviar</span>
        </div>
      </footer>
    </div>
  );
}
