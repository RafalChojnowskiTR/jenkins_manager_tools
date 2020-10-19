from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import posixpath


class JenkinsJobsManager:
    def __init__(self, url):
        self.driver = webdriver.Chrome('./chromedriver')
        self.url = url
        self.jenkins_jobs_urls = []

    def __del__(self):
        try:
            self.driver.close()
        except Exception:
            pass

    def open_url(self):
        self.driver.get(self.url)

    def enter_credentials(self, login, password):
        self.driver.find_element_by_id("j_username").send_keys(login)
        self.driver.find_element_by_name("j_password").send_keys(password)

    def click_login_button(self):
        self.driver.find_element_by_name("Submit").click()

    def get_jobs_urls(self):
        elements_xpath = './/table[@id="projectstatus"]/tbody/tr[@id]'
        elements = self.driver.find_elements_by_xpath(elements_xpath)

        return [posixpath.join(self.url, element.get_attribute("id").replace("_", "/")) for element in elements]

    def get_jobs_urls_and_durations(self):
        elements_xpath = './/table[@id="projectstatus"]/tbody/tr[@id]'
        elements = self.driver.find_elements_by_xpath(elements_xpath)

        job_urls = [posixpath.join(self.url, element.get_attribute("id").replace("_", "/")) for element in elements]

        durations = self.driver.find_elements_by_xpath(elements_xpath + "/td[6]")

        durations_list = [duration.text for duration in durations]

        return dict(zip(job_urls, durations_list))

    def run_jobs(self, jobs_urls):
        failed_jobs = []

        for job_url in jobs_urls:
            print(job_url)
            self.driver.get(posixpath.join(job_url, "build?delay=0sec"))

            try:
                self.driver.find_element_by_id("yui-gen1-button").click()
            except NoSuchElementException:
                failed_jobs.append(job_url)
                print("Could not run job: {}".format(job_url))

        return failed_jobs

    def run_source_jobs(self, jobs_urls):
        failed_jobs = []

        for job_url in jobs_urls:
            print(job_url)

            try:
                self.driver.get(job_url)
                self.driver.find_element_by_xpath(".//*[@id='tasks']/div[5]/a[2]").click()
            except Exception:
                failed_jobs.append(job_url)
                print("Could not run job: {}".format(job_url))

        return failed_jobs

