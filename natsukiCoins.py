#!/usr/bin/python



import json
import praw
import pprint 
import re 
import time
import datetime

__author__ = "Mobus Dorphin"
__license__ = "GPL"
__email__ = "celestialtuba@gmail.com"


def finish():
  print("Number of nickles: {}".format(matchCount))
  print("That totals ${}!".format(float(matchCount) * .05))

  with open('datestamp', 'w') as f:
     f.write(str(mostRecentComment))

  with open('nickleCount', 'w') as n:
     n.write(str(matchCount))
  print("Run Complete!")
#  print(datetime.strftime(datetime.now(), "%Y-%m-%d %H%M"))
  print(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M"))



print("Starting Run")
#print(datetime.strftime(datetime.now(), "%Y-%m-%d %H%M"))
print(datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M"))

matchCount = 0
datestamp = ""
expression = re.compile('.*(username|checks|skcehc|name|c.{0,3}h.{0,3}e.{0,3}c.{0,3}k.{0,3}s)', re.I | re.DOTALL)

#################################
# A set of checks to ensure the regex matches what I expect it to match
#################################
if expression.match("name fits"):
  print "it fits"
if expression.match("Name fits"):
  print "It Fits"
if expression.match("username checks out"):
  print "checks out"
if expression.match("Tuo skcehc emanresu"):
  print "skcehc"
if expression.match("Username"):
  print "Username"
if expression.match('*obligatory "relevant username"*'):
  print "obligatory"
if expression.match('c h e c k'):
  print "c h e c k"
if expression.match('c      h           e              c           k'):
  print "c              h              e              c         k"



#################################
# Load the credentials from saved json and set up the reddit crawler
#################################
with open('credentials.json', 'r') as f:
  library = json.load(f)

reddit = praw.Reddit(client_id=library['client_id'],
                        client_secret=library['client_secret'],
                        password=library['password'],
                        user_agent=library['user_agent'],
                        username=library['username'])

# If this prints properly, we are ready to go
print(reddit.user.me())

#################################
# Determine the most recent processed comment and complete nickel count from previous run
#################################
with open('datestamp') as f:
  datestamp = f.read()

with open('nickleCount') as n:
  matchCount = int(n.read())

print "Datestamp: " + datestamp
print("Number of previous nickles: %d" % matchCount)

mostRecentComment = datestamp 
matchesThisRun = 0;
print mostRecentComment
print datestamp

#################################
# Now on to the show!
#################################

# Gather all comments that u/I_wanna_sex_Natsuki has made, sorted by New
comments = reddit.redditor('I_wanna_sex_Natsuki').comments.new(limit=None)
# Iterate through each comment, one by one
for comment in comments:
  print(comment.permalink.encode('utf-8'))
  try: 
    # Once we've created our individual comment for this run of the FOR loop
    # we need to call refresh() or all replies will be empty
    # (This is just due to an optimization of the reddit API)
    comment.refresh()
  except (KeyboardInterrupt, SystemExit):
    print("Number of matches found: %d" % matchCount)
    finish()
    raise
  except:
    print "WHOOOPS!  That didn't work!"
    continue
  for reply in comment.replies:
     # Now that we've got IWSN's comment, lets look through each reply
     # to see if we can find a match for our regex
     if matchesThisRun == 5:
       # I had to put this in to prevent duplicate posts.  Since the reddit API only
       # allows 1 post every 10 minutes, we can't post more than 5 times in an hour
       # Since the job runs hourly, we're just going to stop checking once we've reached
       # 5 matches, and let next hour's run work on the rest
       finish()
       exit()
     if float(datestamp) < reply.created: 
       if expression.match(reply.body):
         #If we found a new reply, and that reply's body matches our regex, we do the magic!
         print "Match Found: "
         matchCount += 1
	 matchesThisRun += 1
         nickleValue = float(matchCount * .05)
         numProteinBars = int(nickleValue / 2.49)
         remainingMunny = float(nickleValue - (numProteinBars * 2.49))
         print(reply.reply("Look!  Another nickel!\n\nCurrently, _I_wanna_sex_Natsuki_ has found __{}__ nickels under the vending machine for a total of __${:1.2f}__!\n\nThat's enough for {} protein bars at $2.49 each with ${:1.2f} left over!\n\n>^(Beep Boop! I keep track of the theoretical nickels _I_wanna_sex_Natsuki_ would have whenever someone says 'username checks out'.)\n\n>^See [^this ^post](https://www.reddit.com/r/DDLC/comments/7ywdft/natsuki_likes_yuri/dujrpbs/) ^and [^this ^post](https://www.reddit.com/r/DDLC/comments/8170ot/were_all_hypocrites_and_thats_ok/dv1ucod/) ^(for context.  Please report any issues to u/mobusdorphin!)\n^^^psst ^^^we're ^^^on [^^^github](https://github.com/mobusdorphin/natsukiCoins) ^^^now!".format(matchCount, nickleValue, numProteinBars, remainingMunny)))
         print("This is a test of the IWSN Nickel Bot.  At current count, u/I_wanna_sex_Natsuki has {} nickels for a total of ${:1.2f}".format(matchCount, float(matchCount) * .05))
         if float(mostRecentComment) < reply.created: mostRecentComment = reply.created
         time.sleep(610)
     else: 
       print("Old Comment")
     print reply.body.encode('utf-8')
     print reply.created
finish()
exit()
