class JenkinsJobsReader:
    def __init__(self, job_url, jenkins_jobs_manager):
        self.jenkins_jobs_manager = jenkins_jobs_manager
        self.jenkins_jobs_manager.url = job_url

    def get_latest_build_number(self):

        self.jenkins_jobs_manager.open_url()

        builds = self.jenkins_jobs_manager.driver.find_elements_by_xpath(".//a[@update-parent-class][@class='tip model-link inside build-link display-name zws-inserted']")

        build_numbers = []

        for build in builds:
            build_numbers.append(build.get_attribute("href").split("/")[-2])

        return max(build_numbers)



