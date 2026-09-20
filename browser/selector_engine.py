def best_selector(element):
    if not isinstance(element, dict):
        return 'body'

    if element.get('id'):
        return f"#{element['id']}"
    if element.get('data-testid'):
        return f"[data-testid=\"{element['data-testid']}\"]"
    if element.get('name'):
        return f"[name=\"{element['name']}\"]"
    if element.get('aria-label'):
        return f"[aria-label=\"{element['aria-label']}\"]"
    if element.get('role'):
        return f"[role=\"{element['role']}\"]"
    tag = (element.get('tag') or 'div').lower()
    return tag
