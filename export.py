from playnicely.client import PlayNicely
import settings

client = PlayNicely(username=settings.playnicely_user, password=settings.playnicely_password)

# Get user information
me = client.users.show("current")
my_projects = client.users.list_projects("current")

print "Playnice.ly user %s. User ID %d" % (me.username, me.user_id)
print "Your projects are:"
for i, p in enumerate(my_projects):
    print "    [%d] %s" % (i+1, p.name)


while True:

    #get the project you want to to import
    proj_id = raw_input("\nPlease select the project you want to export: ")

    #make sure input is valid
    try:
        proj_id = int(proj_id)
        proj_id_test = proj_id - 1
    except ValueError:
        print "Sorry, the value you entered was not recognized"
    else:
        if proj_id_test in range(len(my_projects)):
            break
        else:
            print "Sorry, you entered an incorrect value, please try again!"

# Get the first of your projects so that we can show some items for it
project = my_projects[proj_id-1]

items = client.items.list(project.project_id)
print "%d items are ready to be exported from project %s" % (len(items), project.name)

# list all items
#for item in items:
#    print "    %s (ID: %d)" % (item.subject, item.item_id)

print "\nAll done! Now you try"

