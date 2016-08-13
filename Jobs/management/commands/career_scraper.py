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
		allowed = re.compile(r"Developer|Designer|Engineer|Admin|Manager|Writer|Executive|Lead|Analyst|Editor|"
							 r"Associate|Architect|Recruiter|Specialist|Scientist|Support|Expert|SSE|Head|"
							 r"Producer|Evangelist|Ninja|Scalability", re.IGNORECASE)
		not_allowed = ['responsibilities', 'description', 'requirements', 'experience', 'empowering', 'engineering',
					   'find', 'skills', 'recruiterbox', 'google', 'communicating', 'associated', 'internship',
					   'proficient', 'leadsquared', 'referral', 'should', 'must', 'become', 'global', 'degree', 'good',
					   'capabilities', 'leadership', 'services', 'expertise', 'architecture', 'hire', 'follow',
					   'procedures', 'conduct', 'perk', 'missed', 'generation', 'search', 'tools', 'worldwide', 'contact',
					   'question', 'intern', 'classes', 'trust', 'ability', 'businesses', 'join', 'industry', 'response',
					   'you', 'using', 'work', 'based', 'grow', 'provide', 'jobs', 'understand']

		profile_list = set()
		k = soup.body.findAll(text=allowed)
		for i in k:
			if len(i) < 60 and not any(x in i.lower() for x in not_allowed):
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
