// Defines a tiny language "simple" for highlight.js
(function() {
  // register once (safe if script may be loaded multiple times)
  if (typeof hljs === 'undefined' || hljs.getLanguage && hljs.getLanguage('simple')) return;

  hljs.registerLanguage('simple', function(hljs) {
    return {
      name: 'simple',
      aliases: ['simplelang'],
      keywords: {
        keyword: 'do end if else while return'
      },
      contains: [
        hljs.COMMENT('#', '$'),            // line comments start with #
        hljs.QUOTE_STRING_MODE,           // "string" support
        {                                // numbers
          className: 'number',
          begin: /\b\d+(\.\d+)?\b/
        }
      ]
    };
  });
})();

