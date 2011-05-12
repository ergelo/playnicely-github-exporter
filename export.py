from playnicely.client import PlayNicely
from github2.client import Github
from time import sleep

import settings
import sys

##########################
#                        #
#  get playnice.ly bits  #
#                        #
##########################

pn_client = PlayNicely(username=settings.playnicely_user, password=settings.playnicely_password)

# Get user information
pn_user = pn_client.users.show("current")
pn_projects = pn_client.users.list_projects("current")

print "Playnice.ly user %s. User ID %d" % (pn_user.username, pn_user.user_id)
print "Your projects are:"
for i, p in enumerate(pn_projects):
    print "    [%d] %s" % (i+1, p.name)

while True:
    #get the project you want to to export
    pn_proj_id = raw_input("\nPlease select the project you want to export: ")

    #make sure input is valid
    try:
        pn_proj_id = int(pn_proj_id)
        pn_proj_id_test = pn_proj_id - 1
    except ValueError:
        print "Sorry, the value you entered was not recognized"
    else:
        if pn_proj_id_test in range(len(pn_projects)):
            break
        else:
            print "Sorry, you entered an incorrect value, please try again!"

# Get the project that you want to export from
pn_project = pn_projects[pn_proj_id-1]

items = pn_client.items.list(pn_project.project_id, detail="full")
print "%d items are ready to be exported from project %s\n" % (len(items), pn_project.name)

# list all items
#for item in items:
#    print "    %s (ID: %d)" % (item.subject, item.item_id)

#####################
#                   #
#  get github bits  #
#                   #
#####################

gh_client = Github(username=settings.github_user, api_token=settings.github_token)
gh_repos = gh_client.repos.list(settings.github_user)

for i, p in enumerate(gh_repos):
    print "    [%d] %s" % (i+1, p.name)

while True:
    #get the repo you want to import to:
    gh_repo_id = raw_input("\nPlease select the project you want to import to: ")

    #make sure input is valid
    try:
        gh_repo_id = int(gh_repo_id)
        gh_repo_id_test = gh_repo_id - 1
    except ValueError:
        print "Sorry, the value you entered was not recognized"
    else:
        if gh_repo_id_test in range(len(gh_repos)):
            break
        else:
            print "Sorry, you entered an incorrect value, please try again!"

# Get the repo that you want to import to:
gh_repo = settings.github_user+'/'+gh_repos[gh_repo_id-1].name
gh_issues = gh_client.issues.list(gh_repo)
gh_issues.extend(gh_client.issues.list(gh_repo, state='closed'))

#make sure there's no issues in gh
if len(gh_issues):
    print "There are %d issues in project %s. If you want to maintain playnice.ly issue numbering please remove them from your github account web interface." % (len(gh_issues), gh_repo)

    #get input from user
    quit = raw_input("\nPress q to exit the script, any other key to continue: ")

    #quit if so commanded
    if quit == 'q':
        sys.exit()
    else:
        pass

###################
#                 #
#  user matching  #
#                 #
###################

pn_user_ids = pn_client.projects.show(project_id=pn_project.project_id, detail="full").user_ids

pn_users = []

print "Users for playnice.ly project %s:" % (pn_project.name)
for i,u in enumerate(pn_user_ids):
    user = pn_client.users.show(user_id=u, detail="compact")
    print "[%d] %s" % (i+1, user.username)
    pn_users.append(user)

print "\nAttempting to match with github users...\n"

matches = []

for user in pn_users:
    results = gh_client.users.search(user.first_name+" "+user.surname)    
    if len(results) > 0:
        if len(results) == 1:
            while True:
                match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, results[0].username))
                if match == 'Y' or match == '':
                    matches.append((user.user_id, results[0].username))
                    print '\n'
                    break
                elif match == 'n':
                    print 'I\'m sorry, we couldn\'t match %s automatically.' % (user.username)
                    query = raw_input("Search GitHub for user: ")
                    q_results = gh_client.users.search(query)
                    if q_results:
                        if len(q_results) == 1:
                            match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                            if match == 'Y' or match == '':
                                matches.append((user.user_id, q_results[0].username))
                                print '\n'
                                break
                            elif match == 'n':
                                print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                            else:
                                print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                        else:
                            print "the following github matches were found for playnice.ly user %s:" % (user.username)
                            for i,r in enumerate(results):
                                print "[%d] %s" % (i+1, r.username)

                            while True:
                                match = raw_input("Enter the number corresponding to the correct match. Enter \'n\' if there is no match:")
                                if match == 'n':
                                    while True:
                                        query = raw_input("Search GitHub for user: ")
                                        q_results = gh_client.users.search(query)
                                        if q_results:
                                            if len(q_results) == 1:
                                                match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                                                if match == 'Y' or match == '':
                                                    matches.append((user.user_id, q_results[0].username))
                                                    print '\n'
                                                    break
                                                elif match == 'n':
                                                    print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                                                else:
                                                    print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                                else:
                                    try:
                                        match = int(match)
                                        if match-1 in range(len(results)):
                                            matches.append((user.user_id, r.username))
                                            break
                                    except ValueError:
                                        pass

                                    print "Sorry, the value you entered was not recognized"

                else:
                    print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
        else:
            print "the following github matches were found for playnice.ly user %s:" % (user.username)
            for i,r in enumerate(results):
                print "[%d] %s" % (i+1, r.username)

            while True:
                match = raw_input("Enter the number corresponding to the correct match. Enter \'n\' if there is no match, \'g\' if the user is not on github:")
                if match == 'g':
                    break
                elif match == 'n':
                    while True:
                        query = raw_input("Search GitHub for user: ")
                        q_results = gh_client.users.search(query)
                        if q_results:
                            if len(q_results) == 1:
                                match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                                if match == 'Y' or match == '':
                                    matches.append((user.user_id, q_results[0].username))
                                    print '\n'
                                    break
                                elif match == 'n':
                                    print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                                else:
                                    print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                            else:
                                print "the following github matches were found for playnice.ly user %s:" % (user.username)
                                for i,r in enumerate(results):
                                    print "[%d] %s" % (i+1, r.username)

                                while True:
                                    match = raw_input("Enter the number corresponding to the correct match. Enter \'n\' if there is no match:")
                                    if match == 'n':
                                        while True:
                                            query = raw_input("Search GitHub for user: ")
                                            q_results = gh_client.users.search(query)
                                            if q_results:
                                                if len(q_results) == 1:
                                                    match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                                                    if match == 'Y' or match == '':
                                                        matches.append((user.user_id, q_results[0].username))
                                                        print '\n'
                                                        break
                                                    elif match == 'n':
                                                        print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                                                    else:
                                                        print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                                    else:
                                        try:
                                            match = int(match)
                                            if match-1 in range(len(results)):
                                                matches.append((user.user_id, r.username))
                                                break
                                        except ValueError:
                                            pass

                                        print "Sorry, the value you entered was not recognized"

                else:
                    try:
                        match = int(match)
                        if match-1 in range(len(results)):
                            matches.append((user.user_id, r.username))
                            break
                    except ValueError:
                        pass

                    print "Sorry, the value you entered was not recognized"

    elif len(results) == 0:
        print "No matches were found for user %s" % (user.username)
        while True:
            query = raw_input("Search GitHub for user: ")
            q_results = gh_client.users.search(query)
            if q_results:
                if len(q_results) == 1:
                    match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                    if match == 'Y' or match == '':
                        matches.append((user.user_id, q_results[0].username))
                        print '\n'
                        break
                    elif match == 'n':
                        print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                    else:
                        print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                else:
                    print "the following github matches were found for playnice.ly user %s:" % (user.username)
                    for i,r in enumerate(results):
                        print "[%d] %s" % (i+1, r.username)

                    while True:
                        match = raw_input("Enter the number corresponding to the correct match. Enter \'n\' if there is no match:")
                        if match == 'n':
                            while True:
                                query = raw_input("Search GitHub for user: ")
                                q_results = gh_client.users.search(query)
                                if q_results:
                                    if len(q_results) == 1:
                                        match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                                        if match == 'Y' or match == '':
                                            matches.append((user.user_id, q_results[0].username))
                                            print '\n'
                                            break
                                        elif match == 'n':
                                            print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                                        else:
                                            print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                        else:
                            try:
                                match = int(match)
                                if match-1 in range(len(results)):
                                    matches.append((user.user_id, r.username))
                                    break
                            except ValueError:
                                pass

                            print "Sorry, the value you entered was not recognized"

    else:
        print "the following github matches were found for playnice.ly user %s:" % (user.username)
        for i,r in enumerate(results):
            print "[%d] %s" % (i+1, r.username)

        while True:
            match = raw_input("Enter the number corresponding to the correct match. Enter \'n\' if there is no match, \'g\' if the user is not on github:")
            if match == 'g':
                break
            elif match == 'n':
                while True:
                    query = raw_input("Search GitHub for user: ")
                    q_results = gh_client.users.search(query)
                    if q_results:
                        if len(q_results) == 1:
                            match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                            if match == 'Y' or match == '':
                                matches.append((user.user_id, q_results[0].username))
                                print '\n'
                                break
                            elif match == 'n':
                                print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                            else:
                                print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                        else:
                            print "the following github matches were found for playnice.ly user %s:" % (user.username)
                            for i,r in enumerate(results):
                                print "[%d] %s" % (i+1, r.username)

                            while True:
                                match = raw_input("Enter the number corresponding to the correct match. Enter \'n\' if there is no match:")
                                if match == 'n':
                                    while True:
                                        query = raw_input("Search GitHub for user: ")
                                        q_results = gh_client.users.search(query)
                                        if q_results:
                                            if len(q_results) == 1:
                                                match = raw_input("pn: %s and gh: %s were matched. correct? [Y/n]" % (user.username, q_results[0].username))
                                                if match == 'Y' or match == '':
                                                    matches.append((user.user_id, q_results[0].username))
                                                    print '\n'
                                                    break
                                                elif match == 'n':
                                                    print 'I\'m sorry, we couldn\'t match %s.' % (user.username)
                                                else:
                                                    print 'Unrecognized input, enter \'Y\' to confirm match, or \'n\' not to.'
                                else:
                                    try:
                                        match = int(match)
                                        if match-1 in range(len(results)):
                                            matches.append((user.user_id, r.username))
                                            break
                                    except ValueError:
                                        pass

                                    print "Sorry, the value you entered was not recognized"

            else:
                try:
                    match = int(match)
                    if match-1 in range(len(results)):
                        matches.append((user.user_id, r.username))
                        break
                except ValueError:
                    pass

                print "Sorry, the value you entered was not recognized"

####################
#                  #
#  issue transfer  #
#                  #
####################

print "\nInitiating issue transfer"

for item in items[3:10]:
    if item.status == "Closed":
        item_state = "Closed"
    else:
        item_state = "Open"

    item_user = ''
    for pn, gh in matches:
        if pn == item.responsible:
            item_user = gh
            break
        
    gh_issue = gh_client.issues.open(gh_repo, title=item.subject, body=item.body)
    gh_issue.user = item_user
    gh_issue.state = item_state
    
    # print '\n'
    # for attr in dir(item):
    #     print "item.%s = %s" % (attr, getattr(item, attr))
    # print '\n'

    # print '\n'
    # for attr in dir(gh_issue):
    #     print "gh_issue.%s = %s" % (attr, getattr(gh_issue, attr))
    # print '\n'

    sleep(1)


'''
print '\npn items'
print items

print '\ngh issues'
print gh_issues

print '\n matches, ids (pn, gh)'
print matches
'''

print "\nAll done for now, remember, this is Work in Progress!"

