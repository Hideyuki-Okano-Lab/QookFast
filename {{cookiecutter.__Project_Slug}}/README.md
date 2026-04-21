# {{cookiecutter.project_name}}
{%- if cookiecutter.description != "" %}
{{cookiecutter.description}}
{%- endif %}

{%- if cookiecutter.date != "" %}
- Generation date: {{cookiecutter.date}}
{%- endif %}

## Project Owner
- Name: {{cookiecutter.author_name}}
- Contact: [{{cookiecutter.email}}](mailto:{{cookiecutter.email}})
