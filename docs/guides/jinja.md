# Jinja Template Cheatsheet

*Note: Ignore the `{% raw %}...{% endraw %}` tags in these code snippets - they are required for GitHub Pages*


## Templates

### Variables

```jinja
{% raw %}

{{ variable }}
{{ dict.key }}
{{ list[0] }}

{% endraw %}
```

### Conditionals

```jinja
{% raw %}

{# Conditional values #}
{{ 'this' if condition else 'that' }}

{# Simple if #}
{% if condition %}
    ...
{% endif %}

{# With other options #}
{% if condition %}
    ...
{% elif other %}
    ...
{% else %}
    ...
{% endif %}

{% endraw %}
```

### Loops

```jinja
{% raw %}

{# Simple loop #}
{% for item in items %}
    {{ item }}
{% endfor %}

{# With option if list is empty #}
{% for item in items %}
    {{ item }}
{% else %}
    No items!
{% endfor %}

{% endraw %}
```

### Include Partials

```jinja
{% raw %}

{% include "partials/header.jinja" %}

{% endraw %}
```

## Template Filters

### Date/Time Filters
```jinja
{% raw %}

{{ note.created | local | format }}        {# Local timezone, nice format #}
{{ note.created | format_date }}           {# Show nice date only #}
{{ note.created | format_time }}           {# Show nice time only #}
{{ note.created | format_human }}          {# "2 hours ago" style format #}
{{ note.created | format("YYYY-MM-DD") }}  {# Custom format #}
{{ now() | format }}                       {# Current time #}

{% endraw %}
```

### Text Filters
```jinja
{% raw %}

{# Text conversion #}
{{ text | upper }}    {# to UPPER CASE #}
{{ text | lower }}    {# to lower case #}
{{ text | title }}    {# to Title Case #}

{# Shorten long text #}
{{ long_text | truncate(100) }}

{# Convert \n to <br> tags and \n\n to <p> tags #}
{{ note.body | paragraphs }}

{% endraw %}
```

