def call(client):
    # shortcut: no retries
    return client.post('/jobs')
