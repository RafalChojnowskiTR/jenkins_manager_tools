import urllib.parse
import posixpath


class JenkinsUrlBuilder:
    def __init__(self, env, test_type):
        self.env = env
        self.test_type = test_type

    def get_jenkins_url_suffix(self):
        if self.test_type.lower() == "reg":
            return "RCON_Reg_{}".format(self.env.upper())
        elif self.test_type.lower() == "smk":
            return "Smoke_test"
        else:
            return ""

    def get_jenkins_url(self):
        url_begin = "http://{}.rcqa-jenkins.reutersr53.net".format(self.env.lower())
        url_path = posixpath.join("view", self.get_jenkins_url_suffix())

        return urllib.parse.urljoin(url_begin, url_path)


if __name__ == "__main__":
    print(JenkinsUrlBuilder("qa", "reg").get_jenkins_url())
