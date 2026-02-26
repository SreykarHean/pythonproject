# Only admin has a fixed username + password
admin_username = "admin"
admin_password = "admin123"

def login(username, password):
    # Check if both username and password match admin
    if username == admin_username and password == admin_password:
        return "admin"
    else:
        # Anyone else automatically becomes a user
        return "user"
