// Convert mermaid code blocks to renderable divs
document.addEventListener('DOMContentLoaded', function() {
  // Find all code blocks that contain mermaid diagrams
  const codeBlocks = document.querySelectorAll('.highlight code');

  codeBlocks.forEach(function(codeBlock) {
    const text = codeBlock.textContent.trim();

    // Check if this is a mermaid diagram
    if (text.startsWith('graph ') || text.startsWith('flowchart') || text.includes('graph LR') || text.includes('graph TD')) {
      // Get the parent highlight div
      const highlightDiv = codeBlock.closest('.highlight');
      if (highlightDiv) {
        // Create a mermaid div with the code
        const mermaidDiv = document.createElement('div');
        mermaidDiv.className = 'mermaid';
        mermaidDiv.textContent = text;

        // Replace the highlight div with the mermaid div
        highlightDiv.replaceWith(mermaidDiv);
      }
    }
  });

  // Initialize Mermaid if it's loaded
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({ startOnLoad: true, theme: 'default' });
    mermaid.contentLoaded();
  }
});

// Re-initialize Mermaid after navigation (for Material theme instant loading)
document.addEventListener('turbo:load', function() {
  if (typeof mermaid !== 'undefined') {
    mermaid.contentLoaded();
  }
});



