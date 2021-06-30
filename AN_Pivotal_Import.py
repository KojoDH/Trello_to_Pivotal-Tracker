#####
#
# Quick and dirty file import utility to allow Epic & Story creation in Pivotal Tracker
# from Trello Cards + Checklists. Input is Trello cards exported as JSON files, and
# output is two CSV files - the 1st containing Epics, and the 2nd containing their Stories.
# Users are also prompted to enter a unique label (preferably short) for each Epic.
#
# Pivotal Tracker CSV columns & Import/Export guide | https://www.pivotaltracker.com/help/articles/csv_import_export/
#
# The original goal here was to pull data from Trello's API (not started yet) and then push it
# to Pivotal Tracker's API, (code commented out at the bottom of this script) but this was
# ultimately abandoned after PT's API continually just kicked back a generic error message.
#
# Pivotal Tracker API | https://www.pivotaltracker.com/help/api/#top
#
#
# - Kojo DH, 6/30/21
#
#####


from datetime import datetime
import csv, json, os, requests


# Import file(s) and initiate lists
folder = "Cards\\"                                                  # Directory containing the Trello JSON files
files = os.listdir(folder)

header = ["Title", "Labels", "Type", "Current State", "Description"]
ebody = []
sbody = []


# Iterate over Trello export file(s) & parse data into Epic & Story CSV's
for f in files:
    # Read-in export file
    with open((folder+f), 'r', encoding='UTF8') as df:
        data = json.load(df)

    # Create Epics
    dname = data["name"]
    print("> Preparing",dname,"epic...")
    dlabel = input("> (OPTIONAL) Please enter a PT label: ")        # Prompt users for a unique, unifying label
    ddesc = data["desc"]
    ebody.append([dname, dlabel, "epic", "unstarted", ddesc])
        
    # Create Stories
    n = 0                                                           # Initiate controller Variables
    nn = 0
    ac = "ACCEPTANCE CRITERIA"
    num_lists = len(data["checklists"])
    
    while n < num_lists:
        dname = data["checklists"][n]["name"]
        num_ac = len(data["checklists"][n]["checkItems"])

        while nn < num_ac:                                          # Aggregate the checklist items into Acceptance Criteria
            ac = ac + "\n" + str(nn+1) + ". " + data["checklists"][n]["checkItems"][nn]["name"]
            nn += 1
        if "\n" not in ac:                                          # Blanks out Acceptance Criteria if none exists
            ac = ""
        sbody.append([dname, dlabel, "Feature", "unstarted", ac])
        
        ac = "ACCEPTANCE CRITERIA"                                  # Reset controller Variables
        nn = 0
        n += 1


# Populate output files
stamp = datetime.now().strftime("%Y%m%d%H%M")
outfile = 'Output\\'+stamp+'_Epics.csv'
with open(outfile, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for b in ebody:
        writer.writerow(b)

stamp = datetime.now().strftime("%Y%m%d%H%M")
outfile = 'Output\\'+stamp+'_Stories.csv'
with open(outfile, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for b in sbody:
        writer.writerow(b)



#### API SECTION KILLED DUE TO THIS PERSISTENT VAGUE RESPONSE ERROR BELOW
### >>>>>
### {'code': 'unhandled_condition', 'kind': 'error', 'error': 'An unexpected condition occurred.'}
### >>>>>
##
### Read-in API credentials
##with open('..\..\Misc\AKL\APTT.txt', 'r', encoding='ANSI') as tf:
##  dtoken = tf.read()
##
##with open('..\..\Misc\AKL\PPIT.txt', 'r', encoding='ANSI') as pf:
##  dproject = pf.read()
##
##
### Prepare API request
##header = {"X-TrackerToken": dtoken, "Content-Type": "application/json"}
##contents = {"name": dname, "description": ddesc}
##
##url_base = "https://www.pivotaltracker.com/services/edge/projects/"
##url = url_base + dproject + "/epics"
##print("> url |",url)
##
##
### Upload to Pivotal
##response = requests.post(
##    url,
##    headers=header,
##    data=contents
##)
##
##
### Process Pivotal response
##res = response.json()
##print(">>>>>")
##print(res)
##print(">>>>>")
