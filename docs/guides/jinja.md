# Jinja Template Cheatsheet

## Templates

### Variables

````jinja
{{ variable }}
{{ dict.key }}
{{ list[0] }}
````

### Conditionals

````jinja
{{ 'this' if condition else 'that' }}
````

````jinja
{% if condition %}
    ...
{% endif %}
````

````jinja
{% if condition %}
    ...
{% elif other %}
    ...
{% else %}
    ...
{% endif %}
````

### Loops

````jinja
{% for item in items %}
    {{ item }}
{% endfor %}
````

````jinja
{% for item in items %}
    {{ item }}
{% else %}
    No items!
{% endfor %}
````

### Include Partials

````jinja
{% include "partials/header.jinja" %}
````

## Template Filters

### Date/Time Filters
````jinja
{{ note.created | local | format }}        {# Local timezone, nice format #}
{{ note.created | format_date }}           {# Show nice date only #}
{{ note.created | format_time }}           {# Show nice time only #}
{{ note.created | format_human }}          {# "2 hours ago" style format #}
{{ note.created | format("YYYY-MM-DD") }}  {# Custom format #}
{{ now() | format }}                       {# Current time #}
````

### Text Filters
````jinja
{# Text conversion #}
{{ text | upper }}    {# to UPPER CASE #}
{{ text | lower }}    {# to lower case #}
{{ text | title }}    {# to Title Case #}

{# Shorten long text #}
{{ long_text | truncate(100) }}

{# Convert \n to <br> tags and \n\n to <p> tags #}
{{ note.body | paragraphs }}
````

