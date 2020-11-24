import os 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_log.settings")

import django 
django.setup()

from learning_logs.models import Topic

topics = Topic.objects.all() # gives us everything 

for topic in topics:
    print("Topic ID:", topic.id, "Topic:", topic )


t = Topic.objects.get(id=1) # just one particualr row
print (t.text)
print(t.date_added)


entries = t.entry_set.all() # the way can access certain topic by related  entires. 

for entry in entries:
    print(entry)

