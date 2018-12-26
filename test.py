# -*- coding: UTF-8 -*
'''
Created on 2018-06-15

@author: trb
'''

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
print('d1.id:', d1.id)

# query
print('grade=2:', Data.objects.find(grade=2).all())

# query count
print('count of grade=2:', Data.objects.find(grade=2).count())

# default order by
print('default order by', Data.objects.find().all())
print('default order by -age', Data.objects.find().order_by('-age').all())

# change
d2['grade'] = 1
d2.save(update_fields=['grade'])

print('count of grade=2:', Data.objects.find(grade=2).count())

# delete document
Data.objects.find(grade=2).delete()

print('-------')

# django like query
from pmongo.query import QueryManger


class Data2(Document):
    db = db
    objects = QueryManger()


print(Data2.objects.create(age=20, name='Tom'))

Data2(age=10, name='Jone').save()
Data2(age=15, name='Jack').save()

print('age>=10:', Data2.objects.find(age__gte=10).count())
print('age>11:', Data2.objects.find(age__gt=11).count())

print('between 10~21', Data2.objects.find(age__between=(10, 21)).count())

# delete age field
d1.unset(['age'])
print(d1)

# update data
print('update', Data2.objects.find(age__between=(10, 21)).update(age=25))

print('between 10~21', Data2.objects.find(age__between=(10, 21)).count())

print('age=25', Data2.objects.find(age=25).count())

Data(name='Robin', books=[{'bid': 1, 'name': 'Python Cookbook'}, {'bid': 2, 'name': 'Java 23 Days'}, {'bid': 3, 'name': 'Android Kit'}]).save()
Data(name='Tom', books=[{'bid': 10, 'name': 'DDL'}]).save()

print('book of [1]:', Data.objects.find({'books.bid': 1}).count())
print('book of [2, 10]:', Data.objects.find({'books.bid': {'$in': [2, 10]}}).count())

print(Data.objects.find(name='Tom').values(name=0, _id=0).all())

d1 = Data.objects.find().first()
d2 = Data.objects.find().first()

print('--------')

print(id(d1), d1)
print(id(d2), d2)
print(d1 == d2)

print(set([d1, d2]))

rcount = Data.objects.find().count()
d1 = Data.objects.find(name='Robin').first()
d2 = Data.objects.find(_id=d1.id).first()
rname = d2['name']
d2['name'] = 'June'
d2.save()
d2['name'] = rname
d2.save(update_fields=['name'])
d2 = Data.objects.find(_id=d1.id).first()
ncount = Data.objects.find().count()
print(d1.data == d2.data)
print(rcount == ncount)

print(Data.objects.find().delete())
print(Data2.objects.find().delete())
