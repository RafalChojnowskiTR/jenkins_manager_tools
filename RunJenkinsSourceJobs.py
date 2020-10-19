from JenkinsJobsManager import JenkinsJobsManager
from JenkinsCredentialsManager import get_jenkins_credentials


def run(env="qa"):
    jenkins_url = "http://{}.rcqa-jenkins.reutersr53.net/view/git%20projects%20sources/".format(env)

    login, password = get_jenkins_credentials(env)

    selenium_jenkins_jobs_runner = JenkinsJobsManager(jenkins_url)
    selenium_jenkins_jobs_runner.open_url()
    selenium_jenkins_jobs_runner.enter_credentials(login, password)
    selenium_jenkins_jobs_runner.click_login_button()
    jobs_urls_and_durations = selenium_jenkins_jobs_runner.get_jobs_urls_and_durations()

    for k, v in jobs_urls_and_durations.items():
        print(k + ": " + str(v))

    failed_jobs = selenium_jenkins_jobs_runner.run_source_jobs(jobs_urls_and_durations.keys())
    print("Jobs that failed to run (Job might be turned off): {}".format(failed_jobs))


if __name__ == "__main__":
    env = "qa"

    run(env)
