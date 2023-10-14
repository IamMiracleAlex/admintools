def get_user_domain(email):
    return email.split("@")[-1].strip()