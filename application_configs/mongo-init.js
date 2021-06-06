 
print('Start #################################################################');

db = db.getSiblingDB('lumoz');
db.createUser(
  {
    user: 'lumozuser',
    pwd: 'lumoz123',
    roles: [{ role: 'readWrite', db: 'lumoz' }],
  },
);
db.createCollection('users');

db = db.getSiblingDB('tenant2');
db.createUser(
  {
    user: 'tenant2user',
    pwd: 'tenant123',
    roles: [{ role: 'readWrite', db: 'tenant2' }],
  },
);
db.createCollection('users');


print('END #################################################################');
