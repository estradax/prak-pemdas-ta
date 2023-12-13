def create_login_interface(username, password):
    # Determine the width of the login box
    box_width = 60

    # Create the login interface
    login_interface = f"""
+{'=' * (box_width - 2)}+
|{username:^{box_width-2}}|
+{'=' * (box_width - 2)}+
    """

    return login_interface

# Example usage:
username_input = input("Enter your username: ")
password_input = input("Enter your password: ")

login_interface = create_login_interface(username_input, password_input)
print(login_interface)
