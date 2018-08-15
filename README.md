PMongo
===============
A small Python MongoDB Document-Based access engine.

Install
===============
```
 pip install pmongo
```

Useage
===============
```python
# base use

# import
from pmongo.document import Document
from pmongo.utils import get_mongo_db

db = get_mongo_db(dbname='test')


# define document class
class Data(Document):
    db = db
    class Meta:
        ordering = ['age']


# new a instance
d1 = Data()

# set data and save
d1['grade'] = 2
d1['name'] = 'Tom'
d1['age'] = 8
d1.save()

d2 = Data()
d2['grade'] = 2
d2['name'] = 'Lucy'
d2['age'] = 6
d2.save()

d3 = Data()
d3['grade'] = 3
d3['name'] = 'Jack'
d3['age'] = 7
d3.save()

# display document ObjectId
print 'd1.id:', d1.id

# query
print 'grade=2:', Data.objects.find(grade=2).all()

# query count
print 'count of grade=2:', Data.objects.find(grade=2).count()

# default order by
print 'default order by', Data.objects.find().all()
print 'default order by -age', Data.objects.find().order_by('-age').all()

# change
d2['grade'] = 1
d2.save()

print 'count of grade=2:', Data.objects.find(grade=2).count()

# delete document
Data.objects.find(grade=2).delete()

print '-------'

# django like query
from pmongo.query import QueryManger


class Data2(Document):
    db = db
    objects = QueryManger()


print Data2.objects.create(age=20, name='Tom')

Data2(age=10, name='Jone').save()
Data2(age=15, name='Jack').save()

print 'age>=10:', Data2.objects.find(age__gte=10).count()
print 'age>11:', Data2.objects.find(age__gt=11).count()

print 'between 10~21', Data2.objects.find(age__between=(10, 21)).count()

# delete age field
d1.unset(['age'])
print d1

# update data
print 'update', Data2.objects.find(age__between=(10, 21)).update(age=25)

print 'between 10~21', Data2.objects.find(age__between=(10, 21)).count()

print 'age=25', Data2.objects.find(age=25).count()

Data(name='Robin', books=[{'bid': 1, 'name': 'Python Cookbook'}, {'bid': 2, 'name': 'Java 23 Days'}, {'bid': 3, 'name': 'Android Kit'}]).save()
Data(name='Tom', books=[{'bid': 10, 'name': 'DDL'}]).save()

print 'book of [1]:', Data.objects.find({'books.bid': 1}).count()
print 'book of [2, 10]:', Data.objects.find({'books.bid': {'$in': [2, 10]}}).count()

print Data.objects.find(name='Tom').values(name=0, _id=0).all()

d1 = Data.objects.find().first()
d2 = Data.objects.find().first()

print '--------'

print id(d1), d1
print id(d2), d2
print d1 == d2

print set([d1, d2])

print Data.objects.find().delete()
print Data2.objects.find().delete()

```

Output:

```
d1.id: 5b7392e82801ca3f35f838b9
grade=2: [Data[{u'grade': 2, u'age': 6, u'_id': ObjectId('5b7392e82801ca3f35f838ba'), u'name': u'Lucy'}], Data[{u'grade': 2, u'age': 8, u'_id': ObjectId('5b7392e82801ca3f35f838b9'), u'name': u'Tom'}]]
count of grade=2: 2
default order by [Data[{u'grade': 2, u'age': 6, u'_id': ObjectId('5b7392e82801ca3f35f838ba'), u'name': u'Lucy'}], Data[{u'grade': 3, u'age': 7, u'_id': ObjectId('5b7392e82801ca3f35f838bb'), u'name': u'Jack'}], Data[{u'grade': 2, u'age': 8, u'_id': ObjectId('5b7392e82801ca3f35f838b9'), u'name': u'Tom'}]]
default order by -age [Data[{u'grade': 2, u'age': 8, u'_id': ObjectId('5b7392e82801ca3f35f838b9'), u'name': u'Tom'}], Data[{u'grade': 3, u'age': 7, u'_id': ObjectId('5b7392e82801ca3f35f838bb'), u'name': u'Jack'}], Data[{u'grade': 2, u'age': 6, u'_id': ObjectId('5b7392e82801ca3f35f838ba'), u'name': u'Lucy'}]]
count of grade=2: 1
-------
Data2[{'age': 20, '_id': ObjectId('5b7392e82801ca3f35f838bc'), 'name': 'Tom'}]
age>=10: 3
age>11: 2
between 10~21 3
Data[{'grade': 2, '_id': ObjectId('5b7392e82801ca3f35f838b9'), 'name': 'Tom'}]
update 3
between 10~21 0
age=25 3
book of [1]: 1
book of [2, 10]: 2
[Data[{u'books': [{u'bid': 10, u'name': u'DDL'}]}]]
--------
4558252368 Data[{u'grade': 1, u'age': 6, u'_id': ObjectId('5b7392e82801ca3f35f838ba'), u'name': u'Lucy'}]
4558252304 Data[{u'grade': 1, u'age': 6, u'_id': ObjectId('5b7392e82801ca3f35f838ba'), u'name': u'Lucy'}]
True
set([Data[{u'grade': 1, u'age': 6, u'_id': ObjectId('5b7392e82801ca3f35f838ba'), u'name': u'Lucy'}], Data[{u'grade': 1, u'age': 6, u'_id': ObjectId('5b7392e82801ca3f35f838ba'), u'name': u'Lucy'}]])
4
3
```