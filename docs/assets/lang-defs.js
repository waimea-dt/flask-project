// Highlight.js language definition for "filetree" (project tree)
// - connector/line characters (├ └ │ ─)
// - folder names ending with '/'
// - files with extensions
// - line comments starting with '#'

(function() {
  if (typeof hljs === 'undefined') return;
  if (hljs.getLanguage && hljs.getLanguage('filetree')) return;

  hljs.registerLanguage('filetree', function(hljs) {
    return {
      name: 'filetree',
      aliases: ['tree','file-tree','structure'],
      case_insensitive: false,
      contains: [
        // comments beginning with #
        {
          className: 'comment',
          begin: /^\s*#.*$/,
          relevance: 0
        },

        // connector characters at start of line (├──, │, └──, etc.)
        {
          className: 'string',
          begin: /^[\s│├└╰┬]+[─]+/,
          relevance: 0
        },

        // folder names ending with a slash
        {
          className: 'title',
          begin: /[A-Za-z0-9_\-\.]+\/(?=\s|$)/,
          relevance: 10
        },

        // file names with extension or dotfiles (e.g. .env, .gitignore, file.txt)
        {
            className: 'keyword',
            begin: /(?:\.[A-Za-z0-9_\-]+|[A-Za-z0-9_\-\.]+\.[A-Za-z0-9]+)(?=\s|$)/,
            relevance: 10
        },

        // fallback punctuation (any remaining box-drawing chars)
        {
          className: 'punctuation',
          begin: /[│└├─]+/,
          relevance: 0
        }
      ]
    };
  });
})();

