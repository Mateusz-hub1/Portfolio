const CACHE='quiz-v1';
self.addEventListener('install',e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll([
    './','./index.html','./results.html','./style.css','./app.js','./og.js',
    './data/prawo_jazdy.json','./data/egzamin_it.json','./data/historia_pl.json'
    // dorzuć własne pliki z /media
  ])));
});
self.addEventListener('fetch',e=>{
  e.respondWith(
    caches.match(e.request).then(r=>r||fetch(e.request))
  );
});
