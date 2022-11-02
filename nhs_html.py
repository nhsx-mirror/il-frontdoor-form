
from random import randint

def html_form_group(content):
    return f"""
    <div class="nhsuk-form-group">
      {content}
    </div>
    """
def html_fieldset(content):
    return f"""
    <fieldset class="nhsuk-fieldset">
      {content}
    </fieldset>
    """

def html_text_input(name, label):
    return html_form_group(f"""
      <label class="nhsuk-label" for="{name}">
        {label}
      </label>
      <input class="nhsuk-input" id="{name}" name="{name}" type="text">
    """)

def html_text_area(name, label, hint=None):
    html_label = f"""
      <label class="nhsuk-label" for="{name}">
        {label}
      </label>
    """
    html_hint = f"""
      <div class="nhsuk-hint" id="{name}-hint">
        {hint}
      </div>
    """ if hint else ""

    html_textarea = f"""
      <textarea class="nhsuk-textarea" id="{name}" name="{name}" rows="5" aria-describedby="{name}-hint"></textarea>
    """

    return html_form_group(html_label + html_hint + html_textarea)

def html_radio_item(name, value, label):
    input_id = f"{name}-{randint(1, 1000000)}"

    return f"""
      <div class="nhsuk-radios__item">
        <input class="nhsuk-radios__input" id="{input_id}" name="{name}" type="radio" value="{value}">
        <label class="nhsuk-label nhsuk-radios__label" for="{input_id}">
          {label}
        </label>
      </div>
    """

def html_legend(legend):
    return f"""
    <legend class="nhsuk-fieldset__legend nhsuk-fieldset__legend--s">
      {legend}
    </legend>
    """

def html_radios(name, legend, options):
    html_options = '<div class="nhsuk_radios">' +\
        "\n".join([html_radio_item(name, o['value'], o['label']) for o in options]) +\
        '</div>'

    return html_form_group(html_fieldset(html_legend(legend) + html_options))

def html_checkbox_item(name, value, label):
    return f"""
      <div class="nhsuk-checkboxes__item">
        <input class="nhsuk-checkboxes__input" id="{name}-{value}" name="{name}" type="checkbox" value="{value}">
        <label class="nhsuk-label nhsuk-checkboxes__label" for="{name}-{value}">
          {label}
        </label>
      </div>
    """

def html_checkbox(name, value, label, hint=None):
    html_hint = f"""
      <div class="nhsuk-hint" id="{name}-hint">
        {hint}
      </div>
    """ if hint else ''

    return html_form_group(html_fieldset(f"""
      {html_hint}
      <div class="nhsuk-checkboxes">
        {html_checkbox_item(name, value, label)}
      </div>"""))

def html_checkboxes(name, legend, options):
    html_options = '<div class="nhsuk_checkboxes">' +\
        "\n".join([html_checkbox_item(name, o['value'], o['label']) for o in options]) +\
        '</div>'

    return html_form_group(html_fieldset(html_legend(legend) + html_options))

def html_button(value):
    return f"""
        <div class="nhsuk-form-group">
            <input type="submit" class="nhsuk-button" value="{value}">
        </div>
    """

def html_conditional_checkbox(name, checkbox_value, checkbox_label, conditional_content, hint=None):
    html_hint = f"""
      <div class="nhsuk-hint" id="{name}-hint">
        {hint}
      </div>
    """ if hint else ''

    return f"""
    {html_hint}
    <div class="nhsuk-checkboxes nhsuk-checkboxes--conditional">
        <div class="nhsuk-checkboxes__item">
          <input class="nhsuk-checkboxes__input" id="{name}" name="{name}" type="checkbox" value="{checkbox_value}" aria-controls="conditional-{name}" aria-expanded="false">
          <label class="nhsuk-label nhsuk-checkboxes__label" for="{name}">
            {checkbox_label}
          </label>
        </div>

        <div class="nhsuk-checkboxes__conditional nhsuk-checkboxes__conditional--hidden" id="conditional-{name}">
            {conditional_content}
        </div>
    </div>
"""
