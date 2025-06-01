from werkzeug.security import generate_password_hash, check_password_hash

data = generate_password_hash("qwerty")
print(data)
print(check_password_hash(data, "qwerty9"))