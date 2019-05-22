from locust import HttpLocust, TaskSet, task
import subprocess
from openApiTest import openApiTEst


'''locust test'''



class UserBehavior(TaskSet):

	def on_start(self):
		pass

	@task(1)
	def test(self):

		
		openApiTEst.testVenout()


class WebUserLocust(HttpLocust):

	weight = 1

	task_set = UserBehavior

	min_wait = 0
	max_wait = 0


if __name__ == '__main__':
	re=subprocess.Popen('locust -f D:\\python\\testcase\\testcase\\locustTest.py --host=http://api.g.caipiao.163.com', shell=True)

