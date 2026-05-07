function renderMath() {
  if (!window.MathJax || typeof window.MathJax.typesetPromise !== 'function') {
    return;
  }

  // Clear prior state before re-typesetting after client-side navigation.
  if (typeof window.MathJax.typesetClear === 'function') {
    window.MathJax.typesetClear();
  }

  window.MathJax.typesetPromise().catch(err => console.log(err));
}

window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true
  },
  svg: {
    fontCache: 'global'
  },
  startup: {
    pageReady: function () {
      return window.MathJax.startup.defaultPageReady().then(() => {
        renderMath();
      });
    }
  }
};

// Re-render math after instant navigation in MkDocs Material.
if (window.document$ && typeof window.document$.subscribe === 'function') {
  window.document$.subscribe(function () {
    renderMath();
  });
} else {
  // Fallback for non-instant navigation.
  document.addEventListener('DOMContentLoaded', function () {
    renderMath();
  });
}
