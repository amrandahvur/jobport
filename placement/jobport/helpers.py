# //=======================================================================
# // Copyright JobPort, IIIT Delhi 2015.
# // Distributed under the MIT License.
# // (See accompanying file LICENSE or copy at
# //  http://opensource.org/licenses/MIT)
# //=======================================================================


# __author__ = 'naman'

import re

from django.contrib.auth.models import User
from django.utils import timezone


def is_member(user, group):
    """Checks if the user object is a member of the group or not."""
    return user.groups.filter(name=group)


def is_eligible(candidate, job):
    """Checks if the user object is a eligible candidate for the job or not.
    All the logic for checking eligibility goes here!"""
    eligibility = {}
    eligibility['value'] = True
    # list of all the reasons that contribute towards uneligibilty
    eligibility['reasons'] = []

    if (candidate.batch.pg_or_not == 'G'):
        if (candidate.cgpa_ug < job.cgpa_min):
            eligibility['value'] = False
            eligibility['reasons'].append(
                "Your CGPA is below the requirement.")
    else:
        if (candidate.cgpa_pg < job.cgpa_min):
            eligibility['value'] = False
            eligibility['reasons'].append(
                "Your CGPA is below the requirement.")

    if (candidate.percentage_tenth < job.min_tenthmarks):
        eligibility['value'] = False
        eligibility['reasons'].append(
            "Your 10th Marks are below the requirement.")

    if (candidate.percentage_twelfth < job.min_twelfthmarks):
        eligibility['value'] = False
        eligibility['reasons'].append(
            "Your 12th Marks are below the requirement.")

    if (candidate.backlogs > job.max_blacklogs):
        eligibility['value'] = False
        eligibility['reasons'].append("You have too many backlogs.")

    if (candidate.status == 'B'):
        eligibility['value'] = False
        eligibility['reasons'].append(
            "You have been blocked by the placement cell.")

    if (job.status == 'C' or job.status == 'A'):
        eligibility['value'] = False
        eligibility['reasons'].append("This Job cannot be applied to.")

    Vals = []
    for b in job.batch.all():
        if (b != candidate.batch):
            Vals.append(False)
        else:
            Vals.append(True)
    if not any(Vals):
        eligibility['value'] = False
        eligibility['reasons'].append("You are not eligible for this job!")
    return eligibility


def checkdeadline(job):
    """Checks if the deadline has passed or not."""
    if (timezone.now() > job.deadline):
        return True
    else:
        return False


def is_admin(user):
    """Checks if the user object is a member of the admin group or not."""
    allowed_group = {'admin'}
    usr = User.objects.get(username=user)
    groups = [x.name for x in usr.groups.all()]
    if allowed_group.intersection(set(groups)):
        return True
    return False


def special_match(strg, search=re.compile(r'[^A-Za-z0-9., -]').search):
    return not bool(search(strg))


def contact_match(strg, search=re.compile(r'[0-9]\n').search):
    return not bool(search(strg))


def onlyspecchar_match(strg, search=re.compile(r'^[., -]').search):
    return not bool(search(strg))


def onlynumbers(strg, search=re.compile(r'^[0-9]').search):
    return bool(search(strg))
