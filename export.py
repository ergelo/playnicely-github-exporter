from playnicely.client import PlayNicely
from github2.client import Github

import settings

##########################
#                        #
#  get playnice.ly bits  #
#                        #
##########################

"""
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

items = pn_client.items.list(pn_project.project_id)
print "%d items are ready to be exported from project %s" % (len(items), pn_project.name)

# list all items
#for item in items:
#    print "    %s (ID: %d)" % (item.subject, item.item_id)

"""
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

print "%d items are about to be deleted from project %s" % (len(gh_issues), gh_repo)


print "\nAll done for now, remember, this is Work in Progress!"

