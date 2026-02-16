self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    const requestUrl = new URL(event.request.url);

    if (requestUrl.origin !== self.location.origin) {
        event.respondWith(async function() {
            try {
                const safeDomain = requestUrl.hostname; 
                const path = requestUrl.pathname;

                const localPath = `/archive_data/${safeDomain}${path}`;

                const response = await fetch(localPath);

                alert(response)
                if (response.status === 200) {
                    return response;
                } else {
                    console.warn(`not found: ${localPath}`);
                    return new Response('', { status: 404 });
                }
            } catch (err) {
                console.error('SW:', err);
                return new Response('', { status: 404 });
            }
        }());
    }
});
