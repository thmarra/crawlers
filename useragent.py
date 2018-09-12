from modules.useragent import Source

src = Source()

# upload data to mongo database
# src.update_database()
# print('x')
# select random value
r = src.random(as_json=False, priority=1)
print(r)