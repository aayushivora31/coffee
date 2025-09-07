// Coffee Shop Service Worker
const CACHE_NAME = 'coffeeshop-v1.0.0';
const STATIC_CACHE = 'coffeeshop-static-v1';
const DYNAMIC_CACHE = 'coffeeshop-dynamic-v1';

// Files to cache immediately
const STATIC_FILES = [
  '/',
  '/menu/',
  '/about/',
  '/contact/',
  '/static/css/style.css',
  '/static/js/bootstrap.bundle.min.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css',
  'https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css',
  'https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js'
];

// Dynamic cache strategies
const CACHE_STRATEGIES = {
  api: 'networkFirst',
  images: 'cacheFirst',
  static: 'cacheFirst',
  pages: 'staleWhileRevalidate'
};


// Install event - cache static files
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('Service Worker: Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Static files cached successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('Service Worker: Error caching static files', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('Service Worker: Deleting old cache', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activated successfully');
        return self.clients.claim();
      })
  );
});

// Fetch event - handle requests with caching strategies
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip requests with specific parameters that shouldn't be cached
  if (url.searchParams.has('no-cache') || url.pathname.includes('/admin/')) {
    return fetch(request);
  }
  
  event.respondWith(handleRequest(request));
});

// Handle different types of requests
async function handleRequest(request) {
  const url = new URL(request.url);
  
  try {
    // API requests - Network First strategy
    if (url.pathname.startsWith('/api/')) {
      return await networkFirst(request);
    }
    
    // Images - Cache First strategy  
    if (request.destination === 'image' || url.pathname.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)) {
      return await cacheFirst(request);
    }
    
    // Static assets - Cache First strategy
    if (url.pathname.match(/\.(css|js|woff2?|ttf|eot)$/i)) {
      return await cacheFirst(request);
    }
    
    // External CDN resources - Cache First strategy
    if (url.origin !== location.origin) {
      return await cacheFirst(request);
    }
    
    // HTML pages - Stale While Revalidate strategy
    if (request.headers.get('accept')?.includes('text/html')) {
      return await staleWhileRevalidate(request);
    }
    
    // Default to network first
    return await networkFirst(request);
    
  } catch (error) {
    console.error('Service Worker: Fetch error', error);
    
    // Return offline page for navigation requests
    if (request.headers.get('accept')?.includes('text/html')) {
      return await getOfflinePage();
    }
    
    // Return offline image for image requests
    if (request.destination === 'image') {
      return await getOfflineImage();
    }
    
    throw error;
  }
}

// Network First strategy
async function networkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    throw error;
  }
}

// Cache First strategy
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    // Update cache in background
    fetch(request)
      .then((response) => {
        if (response.ok) {
          const cache = caches.open(DYNAMIC_CACHE);
          cache.then(c => c.put(request, response));
        }
      })
      .catch(() => {}); // Ignore errors for background updates
    
    return cachedResponse;
  }
  
  const networkResponse = await fetch(request);
  
  if (networkResponse.ok) {
    const cache = await caches.open(DYNAMIC_CACHE);
    cache.put(request, networkResponse.clone());
  }
  
  return networkResponse;
}

// Stale While Revalidate strategy
async function staleWhileRevalidate(request) {
  const cachedResponse = await caches.match(request);
  
  const networkPromise = fetch(request)
    .then((response) => {
      if (response.ok) {
        const cache = caches.open(DYNAMIC_CACHE);
        cache.then(c => c.put(request, response.clone()));
      }
      return response;
    })
    .catch(() => null);
  
  return cachedResponse || await networkPromise;
}

// Get offline page
async function getOfflinePage() {
  const cache = await caches.open(STATIC_CACHE);
  const offlineResponse = await cache.match('/');
  
  if (offlineResponse) {
    return offlineResponse;
  }
  
  // Return a basic offline page
  return new Response(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Offline - Coffee Shop</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body { 
          font-family: Arial, sans-serif; 
          text-align: center; 
          padding: 50px;
          background: linear-gradient(135deg, #8B4513, #D2691E);
          color: white;
          min-height: 100vh;
          margin: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-direction: column;
        }
        .offline-icon { font-size: 4rem; margin-bottom: 1rem; }
        h1 { margin-bottom: 1rem; }
        p { margin-bottom: 2rem; }
        .retry-btn {
          background: white;
          color: #8B4513;
          border: none;
          padding: 12px 24px;
          border-radius: 25px;
          font-weight: bold;
          cursor: pointer;
          transition: transform 0.3s ease;
        }
        .retry-btn:hover {
          transform: translateY(-2px);
        }
      </style>
    </head>
    <body>
      <div class="offline-icon">☕</div>
      <h1>You're Offline</h1>
      <p>It looks like you're not connected to the internet.<br>Please check your connection and try again.</p>
      <button class="retry-btn" onclick="window.location.reload()">Try Again</button>
    </body>
    </html>
  `, {
    headers: { 'Content-Type': 'text/html' }
  });
}

// Get offline image placeholder
async function getOfflineImage() {
  // Return a simple SVG placeholder
  const svg = `
    <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#f8f9fa"/>
      <text x="50%" y="50%" text-anchor="middle" dy=".3em" font-family="Arial" font-size="16" fill="#6c757d">
        Image unavailable offline
      </text>
    </svg>
  `;
  
  return new Response(svg, {
    headers: { 'Content-Type': 'image/svg+xml' }
  });
}

// Background sync for orders
self.addEventListener('sync', (event) => {
  if (event.tag === 'order-sync') {
    event.waitUntil(syncOrders());
  }
});

// Sync pending orders when back online
async function syncOrders() {
  try {
    // Get pending orders from IndexedDB (you would implement this)
    // and send them to the server
    console.log('Service Worker: Syncing pending orders...');
    
    // This would be implemented based on your order queuing strategy
    // For now, just log that we're ready to sync
    
  } catch (error) {
    console.error('Service Worker: Error syncing orders', error);
  }
}

// Push notifications
self.addEventListener('push', (event) => {
  if (!event.data) return;
  
  const data = event.data.json();
  const options = {
    body: data.body || 'You have a new notification from Coffee Shop',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-72x72.png',
    image: data.image,
    vibrate: [200, 100, 200],
    tag: data.tag || 'general',
    data: data.url ? { url: data.url } : undefined,
    actions: [
      {
        action: 'view',
        title: 'View',
        icon: '/static/icons/view-24x24.png'
      },
      {
        action: 'dismiss',
        title: 'Dismiss',
        icon: '/static/icons/dismiss-24x24.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'Coffee Shop', options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'view' && event.notification.data?.url) {
    event.waitUntil(
      clients.openWindow(event.notification.data.url)
    );
  } else if (event.action !== 'dismiss') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message handling from main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(DYNAMIC_CACHE)
        .then(cache => cache.addAll(event.data.urls))
    );
  }
});

console.log('Service Worker: Loaded successfully');