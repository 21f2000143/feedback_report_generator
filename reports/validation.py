def validate_payload(payload):
    # Validate payload is a list
    if not isinstance(payload, list):
        return False

    for item in payload:
        # Validate top-level dictionary keys
        if not isinstance(item, dict):
            return False

        required_keys = {"namespace", "student_id", "events"}
        if not required_keys.issubset(item.keys()):
            return False

        # Validate "namespace" and "student_id" as strings
        if not isinstance(item["namespace"],
                          str) or not isinstance(item["student_id"], str):
            return False

        # Validate "events" is a list
        if not isinstance(item["events"], list):
            return False

        # Validate each event
        for event in item["events"]:
            if not isinstance(event, dict):
                return False

            # Validate event keys
            event_keys = {"type", "created_time", "unit"}
            if not event_keys.issubset(event.keys()):
                return False

            # Validate "type" and "created_time" as strings and "unit" as a string or number
            if (
                not isinstance(event["type"], str)
                or not isinstance(event["created_time"], str)
                or not isinstance(event["unit"], (str, int))
            ):
                return False

    return True
