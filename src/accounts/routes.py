from accounts.resources import AccountListAPI, AccountAPI, AuthAPI, \
    AccountActivationTokenAPI


routes = [
    (AccountListAPI, '/accounts'),
    (AccountActivationTokenAPI, '/accounts/activation'),
    (AccountAPI, '/accounts/<uuid:id>'),
    (AuthAPI, '/auth'),
]
