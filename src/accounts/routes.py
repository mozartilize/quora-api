from accounts.resources import AccountListAPI, AccountAPI, AuthAPI, \
    AccountActivationAPI


routes = [
    (AccountListAPI, '/accounts'),
    (AccountActivationAPI, '/accounts', 'accounts/<uuid:id>'),
    (AccountAPI, '/accounts/<uuid:id>'),
    (AuthAPI, '/auth'),
]
