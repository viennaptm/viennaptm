{{ objname }}
{{ "=" * objname|length }}

.. rubric:: Module

.. code-block:: python

   {{ module }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:

{% block methods %}
.. automethod:: __init__

{% if methods %}
.. rubric:: {{ _('Methods') }}

.. autosummary::
{% for item in methods %}
   ~{{ name }}.{{ item }}
{% endfor %}
{% endif %}
{% endblock %}