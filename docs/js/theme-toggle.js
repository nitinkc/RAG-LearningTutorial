// Persist and restore the user's dark/light preference
(function () {
  const STORAGE_KEY = 'md-color-scheme';
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    // Apply before paint to avoid flash
    document.documentElement.setAttribute('data-md-color-scheme', saved);
  }
})();

document.addEventListener('DOMContentLoaded', function () {
  // Sync preference whenever the Material toggle changes the scheme
  const observer = new MutationObserver(function () {
    const scheme = document.body.getAttribute('data-md-color-scheme');
    if (scheme) {
      localStorage.setItem('md-color-scheme', scheme);
    }

    // Re-render mermaid diagrams after theme switch so colours update
    if (typeof mermaid !== 'undefined') {
      const theme = scheme === 'slate' ? 'dark' : 'default';
      mermaid.initialize({ startOnLoad: false, theme: theme });
      document.querySelectorAll('.mermaid[data-processed]').forEach(function (el) {
        el.removeAttribute('data-processed');
        el.innerHTML = el.getAttribute('data-source') || el.innerHTML;
      });
      mermaid.init(undefined, document.querySelectorAll('.mermaid'));
    }
  });

  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ['data-md-color-scheme'],
  });
});
