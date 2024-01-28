// // This file is the service worker file. It "installs" the PWA on the user's device.
const addResourcesToCache = async (resources) => {
  const cache = await caches.open("v1");
  await cache.addAll(resources);
};

self.addEventListener("install", (event) => {
    event.waitUntil(
        addResourcesToCache([
            "/",
            'static/js/jquery-3.7.1.min.js',
            'static/js/base.js',
            'static/js/bootstrap.bundle.min.js',

            'static/css/bootstrap.min.css',
            'static/css/font-awesome.min.css',
            'static/css/style.css',
            'static/manifest.json'
    ]),
  );
});