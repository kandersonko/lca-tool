def user_active(user):
    return user and user.get("status") == "active"
