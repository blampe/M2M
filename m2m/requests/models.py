from django.db import models
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


def makeMatch(cid):
    entry = Comments.objects.get(pk=cid)
    try:
        new = Comment.objects.get(pk=cid)
        #print "Found matching comment."
        try:
            new.requestTime=datetime.fromtimestamp(float(entry.time))
        except:
            return False
        new.save()
        new.name=entry.name
        new.email=entry.contact
        new.request=entry.comment
        new.completed=entry.completed
        try:
            new.completedTime=datetime.fromtimestamp(float(entry.completedtime))
        except TypeError:
            new.completedTime=None
        new.save()
        new.completerComment=entry.completedcomment
        new.completingServer=entry.completedemail
        new.completingName=entry.completedname
        new.isDeleted=False
        new.server=entry.email
        new.save()
    except ObjectDoesNotExist:
        new = Comment.objects.create(
            CID=cid,
            requestTime=datetime.fromtimestamp(float(entry.time)),
            name=entry.name,
            email=entry.contact,
            request=entry.comment,
            isDeleted=False,
            server=entry.email
        )
        if entry.completed:
            new.completed=entry.completed,
            new.completedTime=datetime.fromtimestamp(float(entry.completedtime))
            new.completerComment=entry.completedcomment
            new.completingServer=entry.completedemail
            new.completingName=entry.completedname
            new.save()
    #except TypeError:
        #print entry.completedtime


def migrate():
    ''' moves comments over to comment, returns number of changes made'''
    #from django.db import connection
    '''
    #cursor = connection.cursor()
    #cursor.execute('LOCK TABLES comments WRITE')
    '''
    open = Comments.objects.filter(completed=0,isdeleted=0)
    latest = open[0]
    closed = Comments.objects.filter(completed=1,isdeleted=0)
    
    current = Comment.objects.all()
    
    
    count = 0
    for entry in open:
        makeMatch(entry.cid)
        #count += 1

    for entry in closed:
        makeMatch(entry.cid)
            
    # No need to migrate newly deleted posts - there won't be any.
    # however, we can mark changes to see if any have been deleted
    # and flag accordingly
    
    for entry in current:
        try:
            Comments.objects.get(pk=entry.CID)
        except ObjectDoesNotExist:
            if entry.CID > latest.cid:
                entry.isDeleted = True
                entry.deletedTime = datetime.now()
                entry.save()
            
            count += 1
    '''
    #cursor.execute('UNLOCK TABLES')
    '''
    return count


# This is the model for the comments that the old site used
class Comments(models.Model):
    cid = models.IntegerField(primary_key=True, db_column='CID',editable=False) # Field name made lowercase.
    time = models.IntegerField(db_column='Time') # Field name made lowercase.
    name = models.CharField(max_length=120, db_column='Name') # Field name made lowercase.
    email = models.CharField(max_length=180, db_column='Email') # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True) # Field name made lowercase.
    completed = models.IntegerField(db_column='Completed') # Field name made lowercase.
    completedname = models.CharField(max_length=120, db_column='CompletedName', blank=True) # Field name made lowercase.
    completedemail = models.CharField(max_length=120, db_column='CompletedEmail', blank=True) # Field name made lowercase.
    completedcomment = models.TextField(db_column='CompletedComment', blank=True) # Field name made lowercase.
    completedtime = models.IntegerField(null=True, db_column='CompletedTime',editable=False, blank=True) # Field name made lowercase.
    contact = models.EmailField(db_column='Contact',blank = True)
    isdeleted = models.IntegerField(db_column='isDeleted') # Field name made lowercase
    
    def __unicode__(self):
        return self.comment
    
    class Meta:
        db_table = u'comments'

# a cleaned up version of the old comments model, django-ready.
class Comment(models.Model):
    CID = models.IntegerField(primary_key=True,unique=True,editable=False,)
    requestTime = models.DateTimeField()
    name = models.CharField(max_length=120,null=True,blank=True,default='Anonymous') 
    email = models.EmailField(max_length=180,null=True,blank=True) 
    completed = models.BooleanField()
    completedTime = models.DateTimeField(null=True,blank=True)
    completerComment = models.TextField(null=True,blank=True)
    completingName = models.CharField(max_length=120,null=True,blank=True) 
    completingServer = models.CharField(max_length=120,null=True,blank=True) 
    isDeleted = models.BooleanField()
    deleterIP = models.IPAddressField(null=True,blank=True)
    deletedTime = models.DateTimeField(null=True,blank=True)
    request = models.TextField()
    server = models.CharField(max_length=60, null=True,blank=True)
    requestIP = models.IPAddressField(max_length=64,null=True,blank=True)
    # ala facebook
    Likes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.request
    
    def save(self,*args,**kwargs):
        if not self.CID:
            i = Comment.objects.raw('SELECT * FROM requests_comment ORDER BY CID DESC LIMIT 1')[0]
            self.CID = i.CID+1
        super(Comment,self).save(*args,**kwargs)