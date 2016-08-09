import os
import re
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_seeker.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "job_seeker.settings"

import django

django.setup()

from Jobs.models import Company, Job


def update_jobs(company, profiles):
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


def find_jobs(company, soup):
    allowed = re.compile(r"Developer|Designer|Engineer|Admin|Manager|Writer|Executive|Lead|Analyst|Editor|"
                         r"Associate|Architect|Recruiter|Specialist|Scientist|Support|Expert|SSE|Head"
                         r"Producer|Evangelist", re.IGNORECASE)
    not_allowed = ['responsibilities', 'description', 'requirements', 'experience', 'empowering', 'engineering',
                   'find', 'skills', 'recruiterbox', 'google', 'communicating', 'associated', 'internship',
                   'proficient', 'leadsquared', 'referral', 'should', 'must', 'become', 'global', 'degree', 'good',
                   'capabilities', 'leadership', 'services', 'expertise', 'architecture', 'hire', 'follow',
                   'procedures', 'conduct', 'perk', 'missed', 'generation', 'search', 'tools', 'worldwide', 'contact',
                   'question', 'intern', 'classes', 'trust', 'ability', 'businesses', 'join', 'industry', 'response', 'you', 'using', 'work', 'based', 'grow', 'provide']

    profile_list = set()
    k = soup.body.findAll(text=allowed)
    for i in k:
        if len(i) < 60 and not any(x in i.lower() for x in not_allowed):
            profile_list.add(i.strip().upper())
    update_jobs(company, profile_list)


def get_html(company):
    url = company.career_url
    career_page = requests.get(url)
    soup = BeautifulSoup(career_page.text, "lxml")
    find_jobs(company, soup)


def get_company():
    companies = Company.objects.all()
    for company in companies:
        get_html(company)


get_company()

#
# url = "https://www.xorlabs.in/jobs/"
# page = urllib2.urlopen(url)
# soup = BeautifulSoup(page, "lxml")
# k = soup.body.findAll(text=re.compile("Writer"))
#
# # print soup.prettify()
# print k
