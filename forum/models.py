threads = {}
users = {}


def create_user(username, email, password):
    if email in users.keys():
        print(email + " has already been registered")
        return
    user = {"username": username, "email": email, "password": password}
    users[email] = user


def create_post(poster, contents, thread_name):
    thread = threads[thread_name]
    post = {"poster": poster, "content": contents}
    # todo: post["date"] = getDate()
    thread.append(post)


def create_thread(thread_name, first_post):
    posts = [first_post]
    threads[thread_name] = posts


def validate(email, password):
    if email not in users.keys():
        print("No such email registered")
        return False
    return users[email]["password"] == password


def get_threads():
    return threads


def get_thread(thread_name):
    return threads[thread_name]


def has_thread(thread_name):
    return thread_name in threads.keys()


def get_users():
    return users


def get_user(email):
    return users[email]
