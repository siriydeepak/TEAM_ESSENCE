// ============================================================
//  AetherShelf Sentinel — Service Worker (sw.js)
//  Handles: Offline caching, Background Push Notifications,
//           Notification click routing
// ============================================================

const CACHE_NAME = "aethershelf-sentinel-v3";
const OFFLINE_URL = "/";

// Assets to pre-cache for offline-first operation
const PRECACHE_ASSETS = [
  "/",
  "/index.html",
  "/manifest.json",
  "/icon-192.png",
  "/icon-512.png",
  "/icon-96.png",
];

// ── Install: Pre-cache all shell assets ──────────────────────
self.addEventListener("install", (event) => {
  console.log("[Sentinel SW] Installing v3...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn("[Sentinel SW] Some assets failed to pre-cache:", err);
      });
    }).then(() => self.skipWaiting())
  );
});

// ── Activate: Clean up stale caches ──────────────────────────
self.addEventListener("activate", (event) => {
  console.log("[Sentinel SW] Activating...");
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE_NAME)
          .map((k) => {
            console.log("[Sentinel SW] Deleting stale cache:", k);
            return caches.delete(k);
          })
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: Network-first for API, Cache-first for shell ──────
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);

  // Always go network for API calls (real-time data)
  if (url.pathname.startsWith("/api/")) {
    event.respondWith(
      fetch(event.request).catch(() =>
        new Response(
          JSON.stringify({ error: "Offline", status: "cached_mode" }),
          { headers: { "Content-Type": "application/json" } }
        )
      )
    );
    return;
  }

  // Cache-first for all shell assets
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((response) => {
          if (response && response.status === 200 && response.type === "basic") {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => caches.match(OFFLINE_URL));
    })
  );
});

// ── Push: Handle background push events ──────────────────────
self.addEventListener("push", (event) => {
  console.log("[Sentinel SW] 🔔 Push received");

  let data = {
    title: "AetherShelf Sentinel",
    body: "Agent alert from your pantry intelligence system.",
    tag: "sentinel-alert",
    urgency: "high",
    icon: "/icon-192.png",
    badge: "/icon-96.png",
  };

  if (event.data) {
    try {
      const parsed = event.data.json();
      data = { ...data, ...parsed };
    } catch {
      data.body = event.data.text();
    }
  }

  // Urgency-based vibration pattern
  const vibratePattern =
    data.urgency === "high"
      ? [200, 100, 200, 100, 400]   // SOS-style for critical alerts
      : [200, 100, 200];             // Standard for advisory

  const notifOptions = {
    body: data.body,
    icon: data.icon,
    badge: data.badge,
    tag: data.tag,
    vibrate: vibratePattern,
    requireInteraction: data.urgency === "high",  // Keep critical alerts on screen
    actions: [
      { action: "open", title: "📊 View Dashboard" },
      { action: "dismiss", title: "Dismiss" },
    ],
    data: {
      url: "/",
      urgency: data.urgency,
      timestamp: Date.now(),
    },
  };

  event.waitUntil(
    self.registration.showNotification(data.title, notifOptions)
  );
});

// ── Notification Click: Open/focus the PWA ───────────────────
self.addEventListener("notificationclick", (event) => {
  const notification = event.notification;
  notification.close();

  if (event.action === "dismiss") return;

  const targetUrl = (notification.data && notification.data.url) || "/";

  event.waitUntil(
    clients
      .matchAll({ type: "window", includeUncontrolled: true })
      .then((windowClients) => {
        // Find an existing Sentinel tab and focus it
        for (const client of windowClients) {
          if (client.url.includes(self.location.origin) && "focus" in client) {
            return client.focus();
          }
        }
        // Otherwise open a new window
        if (clients.openWindow) {
          return clients.openWindow(targetUrl);
        }
      })
  );
});

// ── Push Subscription Change ──────────────────────────────────
self.addEventListener("pushsubscriptionchange", (event) => {
  console.log("[Sentinel SW] Subscription changed — re-registering...");
  event.waitUntil(
    self.registration.pushManager
      .subscribe({
        userVisibleOnly: true,
        applicationServerKey: self.__vapidPublicKey,
      })
      .then((subscription) => {
        return fetch("/api/push/subscribe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(subscription),
        });
      })
  );
});
