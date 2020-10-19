
qa_login = ""
qa_password = ""

ppe_login = ""
ppe_password = ""


def get_jenkins_credentials(env):
    if env.lower() == "qa":
        return qa_login, qa_password
    elif env.lower() == "ppe":
        return ppe_login, ppe_password
    else:
        return "", ""