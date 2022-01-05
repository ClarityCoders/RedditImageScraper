import stdiomask
def create_token():
    creds = {}
    creds['client_id'] = input('client_id: ')
    creds['client_secret'] = stdiomask.getpass(prompt="client_secret: ")
    creds['user_agent'] = input('user_agent: ')
    creds['username'] = input('username')
    creds['password'] = stdiomask.getpass()
    return creds
