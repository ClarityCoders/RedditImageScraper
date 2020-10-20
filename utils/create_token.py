def create_token():
    creds = {}
    creds["client_id"] = input("Client_id: ")
    creds["client_secret"] = input("client_secret: ")
    creds["user_agent"] = input("user_agent: ")
    creds["username"] = input("username: ")
    creds["password"] = input("password: ")
    return creds