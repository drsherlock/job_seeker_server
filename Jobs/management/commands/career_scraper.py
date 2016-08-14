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
							 r"Producer|Evangelist|Ninja|Representative|Marketer|Consultant|Strategist|"
							 r"Curator|Programmer", re.IGNORECASE)
							# QA Automation, Inside Sales

		not_allowed = re.compile(r"\bresponsibilities\b|\bdescription\b|\brequirements\b|\bexperience\b|\bhire\b|"
								 r"\bempowering\b|\bengineering\b|\bwork\b|\bskills\b|\brecruiterbox\b|\bjobs\b|"
								 r"\bgoogle\b|\bcommunicating\b|\bassociated\b|\binternship\b|\bgood\b|\bjoin\b|"
					   			 r"\bproficient\b|\bleadsquared\b|\breferral\b|\bshould\b|\bbecome\b|\bprovide\b|"
					   			 r"\bglobal\b|\bdegree\b|\bcapabilities\b|\bleadership\b|\bservices\b|\bperk\b|"
					   			 r"\bexpertise\b|\barchitecture\b|\bprocedures\b|\bunderstand\b|\bgeneration\b|"
					   			 r"\bconduct\b|\bmissed\b|\bsearch\b|\btools\b|\bbusinesses\b|\bfind\b|\bbased\b|"
					   			 r"\bworldwide\b|\bcontact\b|\bquestion\b|\bintern\b|\bclasses\b|\btrust\b|\byou\b|"
					   			 r"\bability\b|\bindustry\b|\bresponse\b|\bgrow\b|\bmust\b|\bheadline\b|\bfollow\b|"
							   	 r"\busing\b|\bheader\b|\boffice\b|\bjobscore\b|\bmasthead\b|\bheading\b|\bpassed\b|"
							   	 r"\btime\b|\bcolor\b|\bdevelop\b|\bbox\b|\bcrm\b|\bexceptional\b|\binterns\b|\blater\b", re.IGNORECASE)

		profile_list = set()
		k = soup.body.findAll(text=allowed)
		for i in k:
			if len(i) < 100 and not_allowed.search(i) is None:
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
