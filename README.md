# gameofde_rest
Flask Rest API for Capstone project.

## Getting Started
```
pip3 install -r requirements.txt
python3 api.py
```

## Test Commands
Using [httpie](https://httpie.org/)
```python
# Creating a user:
http POST http://127.0.0.1:5000/create_account username="USERNAME" password="PASSWORD" email="EMAIL" role="admin"
# Logging in:
http POST http://127.0.0.1:5000/login username="USERNAME" password="PASSWORD"
# Submitting a cipher:
http POST http://127.0.0.1:5000/caesar 'Cookie:auth_token=AUTH_TOKEN_HERE' cipher='hello'

```
