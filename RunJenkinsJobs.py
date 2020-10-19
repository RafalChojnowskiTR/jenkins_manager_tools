import sys
import getopt

from JenkinsUrlBuilder import JenkinsUrlBuilder
from JenkinsJobsManager import JenkinsJobsManager
from JenkinsCredentialsManager import get_jenkins_credentials


def get_parameters(argv):
    env = ''
    test_type = ''
    test_group = ''

    try:
        opts, args = getopt.getopt(argv, "he:t:g", ["env=", "type="])
    except getopt.GetoptError:
        print('usage: RunJenkinsJobs.py -e <environment[qa/ppe]> -t <type[reg/smk]> -g <group[agws/core]>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: RunJenkinsJobs.py -e <environment[qa/ppe]> -t <type[reg/smk]> -g <group[agws/core]>')
            sys.exit()
        elif opt in ("-e", "--env"):
            env = arg
        elif opt in ("-t", "--type"):
            test_type = arg
        elif opt in ("-g", "--group"):
            test_group = arg

    print('Environment is: ', env)
    print('Test Type is: ', test_type)
    print('Test Group is: ', test_group)

    return env, test_type, test_group


def filter_jobs_urls(jobs_urls, test_group):
    return {job_url: duration for job_url, duration in jobs_urls.items() if test_group in job_url}


def get_duration_in_seconds(duration):
    duration_splitted = duration.split()
    total_sec = 0

    if len(duration_splitted) == 4:
        if duration_splitted[1] in ["godz", "h"]:
            total_sec += float(duration_splitted[0]) * 3600
            total_sec += float(duration_splitted[2]) * 60
        elif duration_splitted[1].startswith("m"):
            total_sec += float(duration_splitted[0]) * 60
            total_sec += float(duration_splitted[2])
    elif len(duration_splitted) == 2:
        if duration_splitted[1].startswith("m"):
            total_sec += float(duration_splitted[0]) * 60
        elif duration_splitted[1].startswith("s"):
            total_sec += float(duration_splitted[0])
    return total_sec


def sort_jobs_urls_by_duration(jobs_urls_and_durations):
    for job_url, duration in jobs_urls_and_durations.items():
        jobs_urls_and_durations[job_url] = get_duration_in_seconds(duration)

    return {key: value for key, value in sorted(jobs_urls_and_durations.items(), key=lambda item: item[1])}


if __name__ == "__main__":

    def run(env, test_type, test_group):
        jenkins_url_builder = JenkinsUrlBuilder(env, test_type)
        jenkins_url = jenkins_url_builder.get_jenkins_url()

        login, password = get_jenkins_credentials(env)

        selenium_jenkins_jobs_runner = JenkinsJobsManager(jenkins_url)
        selenium_jenkins_jobs_runner.open_url()
        selenium_jenkins_jobs_runner.enter_credentials(login, password)
        selenium_jenkins_jobs_runner.click_login_button()

        jobs_urls_and_durations = selenium_jenkins_jobs_runner.get_jobs_urls_and_durations()
        jobs_urls_and_durations = filter_jobs_urls(jobs_urls_and_durations, test_group)
        jobs_urls_and_durations = sort_jobs_urls_by_duration(jobs_urls_and_durations)

        for k, v in jobs_urls_and_durations.items():
            print(k + ": " + str(v))

        failed_jobs = selenium_jenkins_jobs_runner.run_jobs(jobs_urls_and_durations.keys())
        print("Jobs that failed to run (Job might be turned off): {}".format(failed_jobs))


    # env, test_type, test_group = get_parameters(sys.argv[1:])
    # run(env, test_type, test_group)

    # env, test_type, test_group = "ppe", "reg", "agws"
    # run(env, test_type, test_group)
    # env, test_type, test_group = "ppe", "reg", "core"
    # run(env, test_type, test_group)
    # env, test_type, test_group = "ppe", "reg", "server"
    # run(env, test_type, test_group)
    # env, test_type, test_group = "ppe", "reg", "file"
    # run(env, test_type, test_group)

    # env, test_type, test_group = "qa", "reg", "agws"
    # run(env, test_type, test_group)
    # env, test_type, test_group = "qa", "reg", "core"
    # run(env, test_type, test_group)
    # env, test_type, test_group = "qa", "reg", "server"
    # run(env, test_type, test_group)
    env, test_type, test_group = "qa", "reg", "file"
    run(env, test_type, test_group)
