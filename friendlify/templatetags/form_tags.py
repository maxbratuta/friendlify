from django import template

register = template.Library()


@register.filter(name="add_validation_class")
def add_validation_class(field, validation_class):
    css_class = field.field.widget.attrs.get("class", "")
    value = validation_class.split(',')

    if field.form.is_bound:
        field.field.widget.attrs["class"] = f"{css_class} {value[0]}" if field.errors else f"{css_class} {value[1]}"

    return field
