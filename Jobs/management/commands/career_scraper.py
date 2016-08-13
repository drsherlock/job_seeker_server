from django.core.management.base import BaseCommand, CommandError
import os
import re
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_seeker.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "job_seeker.settings"

import django

django.setup()

from Jobs.models import Company, Job

class Command(BaseCommand):
	def update_jobs(self, company, profiles):
		name = company.company_name
		if profiles is not None:
			company.opening = True
			company.no_openings = len(profiles)
			for profile in profiles:
				job = Job.objects.get_or_create(company=company, job_name=profile)
				print name + ":" + profile
		else:
			company.opening = False
			company.no_openings = 0
			company.clear()
			print name + ":noooooo jobs"
		company.save()


	def find_jobs(self, company, soup):
		allowed = re.compile(r"Developer|Engineer|Designer|Admin|Manager|Writer|Executive|Lead|Analyst|Editor|"
							 r"Associate|Architect|Recruiter|Specialist|Scientist|Support|Expert|SSE|Head|"
							 r"Producer|Evangelist|Ninja", re.IGNORECASE)
		not_allowed = re.compile(r"\bresponsibilities\b|\bdescription\b|\brequirements\b|\bexperience\b|\bempowering\b|\bengineering\b|\b"
					   			 r"find\b|\bskills\b|\brecruiterbox\b|\bgoogle\b|\bcommunicating\b|\bassociated\b|\binternship\b|\byou\b|\b"
					   			 r"proficient\b|\bleadsquared\b|\breferral\b|\bshould\b|\bmust\b|\bbecome\b|\bglobal\b|\bdegree\b|\bgood\b|\b"
					   			 r"capabilities\b|\bleadership\b|\bservices\b|\bexpertise\b|\barchitecture\b|\bhire\b|\bfollow\b|\bjobs\b|\b"
							   	 r"procedures\b|\bconduct\b|\bperk\b|\bmissed\b|\bgeneration\b|\bsearch\b|\btools\b|\bworldwide\b|\bcontact\b|\b"
							   	 r"question\b|\bintern\b|\bclasses\b|\btrust\b|\bability\b|\bbusinesses\b|\bjoin\b|\bindustry\b|\bresponse\b|\b"
							   	 r"using\b|\bwork\b|\bbased\b|\bgrow\b|\bprovide\b|\bunderstand\b|\bheader\b|\bheadline\b|\bmasthead\b|\boffice\b", re.IGNORECASE)

		profile_list = set()
		k = soup.body.findAll(text=allowed)
		for i in k:
			if len(i) < 60 and not_allowed.search(i) is None:
				profile_list.add(i.strip().upper())
		self.update_jobs(company, profile_list)


	def get_html(self, company):
		url = company.career_url
		try:
			career_page = requests.get(url)
		except:
			print company.company_name
		else:
			soup = BeautifulSoup(career_page.text, "lxml")
			self.find_jobs(company, soup)


	def handle(self, *args, **options):
		companies = Company.objects.all()
		for company in companies:
			company.jobs.all().delete()
			self.get_html(company)

# c = Command()
# c.get_company()

#
# url = "https://www.xorlabs.in/jobs/"
# page = urllib2.urlopen(url)
# soup = BeautifulSoup(page, "lxml")
# k = soup.body.findAll(text=re.compile("Writer"))
#
# # print soup.prettify()
# print k
