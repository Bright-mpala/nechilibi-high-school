"""
Compatibility shims for removed dependencies.
"""


def ExportModelOperationsMixin(model_name):
    """
    No-op replacement for django_prometheus.models.ExportModelOperationsMixin.
    Returns a plain base class so all existing model definitions work unchanged.
    """
    class _Noop:
        pass
    return _Noop
