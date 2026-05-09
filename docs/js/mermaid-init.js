(function () {
  const mermaidLanguagePattern = /\blanguage-mermaid\b/;
  const mermaidContentPattern = /^(?:%%\{[\s\S]*?\}%%\s*)?(?:graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(?:-v2)?|erDiagram|journey|gantt|pie|mindmap|timeline|gitGraph|quadrantChart|requirementDiagram|C4Context|C4Container|C4Component|C4Dynamic|C4Deployment|xychart-beta|sankey-beta)\b/m;

  function isMermaidReady() {
    return typeof mermaid !== 'undefined';
  }

  function isMermaidDiagram(codeBlock, text) {
    const className = codeBlock.className || '';
    return mermaidLanguagePattern.test(className) || mermaidContentPattern.test(text.trimStart());
  }

  function convertMermaidCodeBlocks(root) {
    const selectors = ['.highlight code', 'pre > code'];

    const mermaidNodes = [];
    const codeBlocks = root.querySelectorAll(selectors.join(','));

    codeBlocks.forEach(function (codeBlock) {
      const diagramText = codeBlock.textContent.trim();
      if (!diagramText || !isMermaidDiagram(codeBlock, diagramText)) {
        return;
      }

      const wrapper = codeBlock.closest('.highlight') || codeBlock.closest('pre');
      if (!wrapper) {
        return;
      }

      const mermaidDiv = document.createElement('div');
      mermaidDiv.className = 'mermaid';
      mermaidDiv.textContent = diagramText;
      wrapper.replaceWith(mermaidDiv);
      mermaidNodes.push(mermaidDiv);
    });

    root.querySelectorAll('.mermaid').forEach(function (node) {
      if (node.getAttribute('data-processed') === 'true') {
        return;
      }
      if (!mermaidNodes.includes(node)) {
        mermaidNodes.push(node);
      }
    });

    return mermaidNodes;
  }

  function renderMermaid(root) {
    if (!isMermaidReady()) {
      return;
    }

    const nodes = convertMermaidCodeBlocks(root);
    if (!nodes.length) {
      return;
    }

    mermaid.initialize({ startOnLoad: false, theme: 'default' });

    if (typeof mermaid.run === 'function') {
      mermaid.run({ nodes: nodes });
    } else {
      mermaid.init(undefined, nodes);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderMermaid(document);
  });

  // MkDocs Material instant navigation lifecycle hook.
  if (typeof document$ !== 'undefined' && typeof document$.subscribe === 'function') {
    document$.subscribe(function (root) {
      renderMermaid(root);
    });
  }

  // Fallback for environments that emit Turbo navigation events.
  document.addEventListener('turbo:load', function () {
    renderMermaid(document);
  });
})();



