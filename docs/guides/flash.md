# Flash Messages

Give feedback to the user after operations / errors.

## Show Messages

```python
flash("Message")
flash("Success message", "success")
flash("Error message", "error")
```
*Note: the message is shown upon next page load*

## Display Messages in a Page

Add this to your base template (above the main content, and aftre the header):

```jinja
{# Show flash messages from any previous events #}
{% include "partials/messages.jinja" %}
```

And add suitable CSS to your stylesheet:

```css
/* Flash Status Messages --------------------------------- */

#messages ul {
    width: fit-content;
    margin: 2rem auto;
    padding: 0;
}

#messages .message {
    list-style: none;
    text-align: center;
    margin-bottom: 1rem;
}

#messages .message.success {
    color: var(--pico-color-green-500);
}

#messages .message.error {
    color: var(--pico-color-red-500);
}
```

This is the code for the partial, which can be modified if required:

```jinja
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <div id="messages">
      <ul>
        {% for category, message in messages %}
          <li class="message {{ category }}">
            {{ message }}
          </li>
        {% endfor %}
      </ul>
    </div>
  {% endif %}
{% endwith %}
```

