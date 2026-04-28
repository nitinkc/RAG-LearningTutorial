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
      return MathJax.typesetPromise().catch(err => console.log(err));
    }
  }
};

// Re-render math after DOM changes (for navigation)
if (window.MathJax && typeof MathJax.typesetPromise === 'function') {
  document.addEventListener('turbo:load', function() {
    MathJax.typesetPromise().catch(err => console.log(err));
  });
}

