class Account:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.username = kwargs['username']
        self.email = kwargs['email']
        self.pw_hash = kwargs['pw_hash']
        self.activated_at = kwargs['activated_at']

    def __str__(self):
        return '<User %r>' % self.username
