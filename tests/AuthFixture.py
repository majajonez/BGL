

class AuthFixture:
    def __init__(self, client):
        self.client = client

    def register_raw(self,data):
        return self.client.post('/auth/register', data=data)


    def register(self,email, user, city, password):
        return self.register_raw(data={'user': user, 'email': email, 'password': password, 'city': city})