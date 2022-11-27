def queryset_to_json(qs):
    """Convert a queryset to a list of dictionaires. The model must implement a to_json method."""
    if not qs.exists():
        return []

    if not hasattr(qs.first(), "to_json"):
        raise NotImplementedError("This method requires that a to_json method be implemented on the model class")

    return [instance.to_json() for instance in qs]