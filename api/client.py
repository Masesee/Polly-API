import requests

BASE_URL = "http://localhost:8000"

def register_user(username, password):
    """
    Registers a new user.

    Args:
        username (str): The desired username.
        password (str): The user's password.

    Returns:
        dict: User data if successful, otherwise None.
    """
    url = f"{BASE_URL}/register"
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred during registration: {e}")
        print(f"Response content: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred during registration: {e}")
        return None


def login_user(username, password):
    """
    Logs in a user and retrieves a JWT token.

    Args:
        username (str): The user's username.
        password (str): The user's password.

    Returns:
        str: The JWT access token if successful, otherwise None.
    """
    url = f"{BASE_URL}/login"
    payload = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, data=payload) # Use data for x-www-form-urlencoded
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred during login: {e}")
        print(f"Response content: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred during login: {e}")
        return None


def create_poll(question: str, options: list[str], token: str):
    """
    Creates a new poll.

    Args:
        question (str): The poll question.
        options (list[str]): A list of options for the poll.
        token (str): The JWT access token for authentication.

    Returns:
        dict: Poll data if successful, otherwise None.
    """
    url = f"{BASE_URL}/polls"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "question": question,
        "options": options
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred during poll creation: {e}")
        print(f"Response content: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred during poll creation: {e}")
        return None

def get_polls(skip: int = 0, limit: int = 10):
    """
    Fetches a list of polls with pagination.

    Args:
        skip (int): Number of items to skip.
        limit (int): Max number of items to return.

    Returns:
        list: A list of poll dictionaries if successful, otherwise None.
    """
    url = f"{BASE_URL}/polls?skip={skip}&limit={limit}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred while fetching polls: {e}")
        print(f"Response content: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred while fetching polls: {e}")
        return None


if __name__ == "__main__":
    # Test registration
    print("--- Testing User Registration ---")
    test_username = "testuser123"
    test_password = "testpassword123"

    print(f"Attempting to register user: {test_username}")
    registered_user = register_user(test_username, test_password)
    if registered_user:
        print("User registered successfully:")
        print(registered_user)
    else:
        print("User registration failed.")

    print(f"\nAttempting to register existing user: {test_username} (should fail)")
    registered_user_again = register_user(test_username, test_password)
    if registered_user_again:
        print("User registered successfully (unexpected):")
        print(registered_user_again)
    else:
        print("User registration failed as expected (username likely taken).")

    # Test login
    print("\n--- Testing User Login ---")
    print(f"Attempting to log in user: {test_username}")
    access_token = login_user(test_username, test_password)
    if access_token:
        print("Login successful. Access Token:")
        print(access_token)
    else:
        print("Login failed.")

    # Test poll creation
    print("\n--- Testing Poll Creation ---")
    if access_token:
        print("Attempting to create a poll with authentication...")
        new_poll = create_poll("What is your favorite color?", ["Red", "Blue", "Green"], access_token)
        if new_poll:
            print("Poll created successfully:")
            print(new_poll)
        else:
            print("Poll creation failed.")

        print("\nAttempting to create another poll...")
        new_poll_2 = create_poll("Best programming language?", ["Python", "JavaScript", "Java"], access_token)
        if new_poll_2:
            print("Second poll created successfully:")
            print(new_poll_2)
        else:
            print("Second poll creation failed.")

    else:
        print("Skipping poll creation test: No access token available.")

    print("\nAttempting to create a poll without authentication (should fail)...")
    unauthorized_poll = create_poll("This should fail", ["Option A", "Option B"], "invalid_token")
    if unauthorized_poll:
        print("Unauthorized poll creation succeeded (unexpected):")
        print(unauthorized_poll)
    else:
        print("Unauthorized poll creation failed as expected.")

    # Test fetching polls
    print("\n--- Testing Fetching Polls ---")
    print("Attempting to fetch polls (skip=0, limit=5)...")
    polls = get_polls(skip=0, limit=5)

    if polls:
        print("Polls fetched successfully:")
        for poll in polls:
            print(poll)
    else:
        print("Failed to fetch polls.")
