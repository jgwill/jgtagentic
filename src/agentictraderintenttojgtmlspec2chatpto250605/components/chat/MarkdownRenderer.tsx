
import React from 'react';
// For a more robust solution, consider using a library like 'marked' or 'react-markdown'.
// This is a very basic implementation for demonstration.

interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  // Basic bold, italic, code block, and list support
  const renderMarkdown = (text: string) => {
    let html = text;

    // Code blocks (```text```)
    html = html.replace(/```([\s\S]*?)```/g, (_match, code) => {
      const safeCode = code.replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<pre class="bg-gray-800 text-white p-2 rounded-md my-2 text-sm overflow-x-auto"><code>${safeCode.trim()}</code></pre>`;
    });
    
    // Inline code (`text`)
    html = html.replace(/`([^`]+)`/g, (_match, code) => {
      const safeCode = code.replace(/</g, '&lt;').replace(/>/g, '&gt;');
      return `<code class="bg-gray-100 text-red-700 px-1 py-0.5 rounded text-sm">${safeCode}</code>`;
    });

    // Bold (**text** or __text__)
    html = html.replace(/\*\*(.*?)\*\*|__(.*?)__/g, '<strong>$1$2</strong>');
    // Italics (*text* or _text_)
    html = html.replace(/\*(.*?)\*|_(.*?)_/g, '<em>$1$2</em>');
    
    // Unordered lists (- item or * item)
    html = html.replace(/^[-*]\s+(.*)/gm, '<li class="ml-4">$1</li>');
    html = html.replace(/<\/li>\n<li/g, '</li><li'); // Fix consecutive list items
    html = html.replace(/<li class="ml-4">.*?<\/li>(?!\s*<li)/gs, (match) => `<ul class="list-disc list-inside my-1">${match}</ul>`);


    // Ordered lists (1. item)
    html = html.replace(/^\d+\.\s+(.*)/gm, '<li class="ml-4">$1</li>');
    // html = html.replace(/<\/li>\n<li/g, '</li><li'); // Already handled for UL, works for OL too
    html = html.replace(/<li class="ml-4">.*?<\/li>(?!\s*<li)/gs, (match) => `<ol class="list-decimal list-inside my-1">${match}</ol>`);

    // Links [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">$1</a>');

    // Paragraphs (basic: wrap lines that are not part of other structures)
    // This is tricky without a full parser. For now, just replace newlines with <br> for non-list/pre content.
    // A better approach would be to split by \n\n for paragraphs.
    // For simplicity in this basic renderer, we'll rely on CSS for line breaks or wrap the whole thing in a whitespace-preerving div.

    return html;
  };

  return (
    <div
      className="prose prose-sm max-w-none break-words" // Tailwind prose for basic styling
      dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
      style={{ whiteSpace: 'pre-wrap' }} // To respect newlines as line breaks
    />
  );
};

export default MarkdownRenderer;
