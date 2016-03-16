def requires_at_least_one_of(*fields):
    """
    Validates that at least one of the given fields or group of fields exist in the schema.
    """
    def validate(document):
        for field in fields:
            if isinstance(field, str) and document.get(field) is not None:
                return None
            elif isinstance(field, list) and all(document.get(item) is not None for item in field):
                return None
        return "One of %s is required" % str(fields)

    return validate


def requires_exactly_one_of(*fields):
    """
    Validates that exactly one of the given fields or group of fields exist in the schema.
    """
    def validate(document):
        presented_fields = []
        for field in fields:
            if isinstance(field, str) and document.get(field) is not None:
                presented_fields.append(field)
            elif isinstance(field, list) and all(document.get(item) is not None for item in field):
                presented_fields.append(field)
        if len(presented_fields) == 1:
            return None
        else:
            return "Exactly one of %s is required" % str(fields)

    return validate

def requires_all_or_none_of(*fields):
    """
    Validates that all or none of the given fields exist in the schema.
    """
    def validate(document):
        presented_fields = [f for f in fields if document.get(f) is not None]
        if len(presented_fields) == 0 or len(presented_fields) == len(fields):
            return None
        else:
            return "All or none of %s is required" % str(fields)

    return validate

def mutually_exclusive(*fields):
    """
    Validates that the given fields or group of fields aren't present at the same time in the schema.
    """
    def validate(document):
        presented_fields = []
        for field in fields:
            if isinstance(field, str) and document.get(field) is not None:
                presented_fields.append(field)
            elif isinstance(field, list) and all(document.get(item) is not None for item in field):
                presented_fields.append(field)
        if len(presented_fields) <= 1:
            return None
        else:
            return "Mutually Exclusive of %s is required" % str(fields)

    return validate


