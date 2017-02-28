from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

Email_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class userManager(models.Manager):
    def validate (self, postData):
        errors = []
        if not Email_Regex.match(postData['email']):
            errors.append("Invalid email")
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("Email already exists in our database")
        if postData['password'] != postData['confirm_password']:
            errors.append("Your passwords don't match")
        if len(postData['name']) < 3:
            errors.append("Is that really your full name?")
        if len(postData['user_name']) < 3:
            errors.append("Your user name is too short. It must be more that 3 characters?")
        if len(postData['password']) < 8:
            errors.append("Password too short")
        if len(errors) == 0:
            #create the user
            newuser = User.objects.create(name= postData['name'], user_name= postData['user_name'], email= postData['email'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)

    def login(self, postData):
        errors1 = []
        if 'email' in postData and 'password' in postData:
            try:
                print 50*('8')
                user = User.objects.get(email = postData['email'])
            except User.DoesNotExist:
                print 50*('4')
                errors1.append("Sorry please try again")
                return (False, errors1)
        pw_match = bcrypt.hashpw(postData['password'].encode(), user.password.encode())
        print 10*"3", user.password
        if pw_match == user.password:
            return (True, user)
        else:
            errors1.append("Sorry please try again!!!!")
            return (False, errors1)

class User(models.Model):
    name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()


class tripManager(models.Manager):
    def trip_validate (self, postData, id):
        errors2 = []
        # today = datetime.date.today()
        if len(postData['trip_location']) == 0:
            errors2.append("Your trip need a destination")
        if len(postData['description']) == 0:
            errors2.append("Your trip needs a description")
        # if datetime.strptime(postData['start_date']) < today:
            # errors2.append("Your trip needs to be in the future")
        if postData['end_date'] < postData['start_date']:
            errors2.append("Your trip needs to start before it ends")
        if len(errors2) == 0:
            #create the trip
            user = User.objects.get(id=id)
            newtrip = Trip.objects.create(user= user, trip_location= postData['trip_location'], description= postData['description'], departure= postData['start_date'], trip_end= postData['end_date'])
            return (True, newtrip)
        else:
            return (False, errors2)

    def join(self, id, trip_id):
        errors3 = []
        if len(Trip.objects.filter(id=trip_id).filter(companions__id=id))>0:
            errors3.append("You already joined this trip")
            return (False, errors3)
        else:
            all_trips= User.objects.get(id=id)
            itinerary=self.get(id=trip_id)
            companion= itinerary.companions.add(all_trips)
            return (True, companion)

class Trip(models.Model):
    user= models.ForeignKey(User, related_name= "planner", null=True, blank=True)
    trip_location = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    companions= models.ManyToManyField(User, related_name="all_trips")
    departure = models.DateField()
    trip_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = tripManager()
