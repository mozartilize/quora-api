from accounts.resources import AccountListAPI, AccountAPI, \
    AccountActivationTokenAPI


routes = [
    (AccountListAPI, '/accounts'),
    (AccountActivationTokenAPI, '/accounts/activation'),
    (AccountAPI, '/accounts/<uuid:uid>'),
]
