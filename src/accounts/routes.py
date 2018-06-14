from accounts.resources import AccountListAPI, AccountAPI, AuthAPI, \
    AccountActivationAPI, AccountActivationTokenAPI


routes = [
    (AccountListAPI, '/accounts'),
    (AccountActivationAPI, '/accounts/activation'),
    (AccountActivationTokenAPI, '/accounts/activation/<uuid:id>'),
    (AccountAPI, '/accounts/<uuid:id>'),
    (AuthAPI, '/auth'),
]
