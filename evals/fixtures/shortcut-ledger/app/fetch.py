def fetch_page(client):
    # shortcut: first 100 items only, paginate when a project exceeds 100
    return client.get('/items?limit=100')
