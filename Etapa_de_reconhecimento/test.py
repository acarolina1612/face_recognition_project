import time
from datetime import datetime, timedelta

now = datetime.now()
after = now + timedelta(seconds=10)
var = ('result', now)

print(var[1], after)
print(type(now), type(after))