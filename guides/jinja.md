# Jinja Template Cheatsheet

## Templates

```jinja
{# Variables #}
{{ variable }}
{{ dict.key }}
{{ list[0] }}

{# Conditional values #}
{{ 'this' if variable else 'that' }}

{# Conditionals #}
{% if condition %}
    ...
{% elif other %}
    ...
{% else %}
    ...
{% endif %}

{# Loops #}
{% for item in items %}
    {{ item }}
{% else %}
    No items!
{% endfor %}

{# Include #}
{% include "partials/header.jinja" %}
```

## Jinja Template Filters

### Date/Time Filters
```jinja
{{ note.created | local | format }}        {# Local timezone, nice format #}
{{ note.created | format_date }}           {# Show nice date only #}
{{ note.created | format_time }}           {# Show nice time only #}
{{ note.created | format_human }}          {# "2 hours ago" style format #}
{{ note.created | format("YYYY-MM-DD") }}  {# Custom format #}
{{ now() | format }}                       {# Current time #}
```

### Text Filters
```jinja
{# Text conversion #}
{{ text | upper }}                {# to UPPER CASE #}
{{ text | lower }}                {# to lower case #}
{{ text | title }}                {# to Title Case #}

{# Shorten long text #}
{{ long_text | truncate(100) }}

{# Convert \n to <br> tags and \n\n to <p> tags #}
{{ note.body | paragraphs }}
```

