def queryset_to_json(qs):
    """Convert a queryset to a list of dictionaires. The model must implement a to_json method."""
    if not qs.exists():
        return []

    # TODO: maybe check has_attr(qs.first(), 'to_json') and raise NotImplemented if False?
    return [instance.to_json() for instance in qs]