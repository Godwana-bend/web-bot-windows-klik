def best_selector(data):
    if data.get('id'): return '#'+data['id']
    if data.get('data-testid'): return '[data-testid="'+data['data-testid']+'"]'
    if data.get('name'): return '[name="'+data['name']+'"]'
    if data.get('aria-label'): return '[aria-label="'+data['aria-label']+'"]'
    tag=data.get('tag','div').lower(); return tag
