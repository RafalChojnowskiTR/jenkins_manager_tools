from JenkinsCredentialsManager import get_jenkins_credentials
from JenkinsJobsManager import JenkinsJobsManager
from JenkinsUrlBuilder import JenkinsUrlBuilder
from JenkinsJobsReader import JenkinsJobsReader

import posixpath


def run():
    env = "qa"
    test_type = "reg"

    jenkins_url = JenkinsUrlBuilder(env, test_type).get_jenkins_url()

    login, password = get_jenkins_credentials(env)

    jenkins_jobs_manager = JenkinsJobsManager(jenkins_url)
    jenkins_jobs_manager.open_url()
    jenkins_jobs_manager.enter_credentials(login, password)
    jenkins_jobs_manager.click_login_button()
    jobs_urls = jenkins_jobs_manager.get_jobs_urls()

    for job_url in jobs_urls:
        latest_build_number = JenkinsJobsReader(job_url, jenkins_jobs_manager).get_latest_build_number()
        latest_build_url = posixpath.join(job_url, latest_build_number, "robot")

        jenkins_jobs_manager.driver.get(latest_build_url)

        if jenkins_jobs_manager.driver.find_element_by_xpath(".//h1").get_attribute("class") == "FAIL":
            print(latest_build_url)

            results = jenkins_jobs_manager.driver.find_elements_by_xpath(".//table[@class='pane sortable']/tbody/tr")
            results = results[1:]
            test_names_and_age = {}

            for result in results:
                td_elements = result.find_elements_by_xpath(".//td")

                if td_elements[1].text == "yes":
                    test_names_and_age[td_elements[0].text] = td_elements[3].text

            print("Number of failed tests: {}".format(len(test_names_and_age)))

            for k, v in test_names_and_age.items():
                print("Age: {}:\n {}".format(v, k))
            print()


if __name__ == "__main__":
    run()
