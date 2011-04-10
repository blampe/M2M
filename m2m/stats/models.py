from django.db import models


# Create your models here.
class Status(models.Model):
    lastchange= models.CharField(max_length=90, db_column='LastChange',) # Field name made lowercase
    
    smbhosts = models.IntegerField(db_column='SMBHosts') # Field name made lowercase.
    ftphosts = models.IntegerField(db_column='FTPHosts') # Field name made lowercase.
    directories = models.IntegerField(db_column='Directories') # Field name made lowercase.
    files = models.IntegerField(db_column='Files') # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FileSize') # Field name made lowercase.
    queries = models.IntegerField(db_column='Queries') # Field name made lowercase.
    updatinghost = models.IntegerField(db_column='UpdatingHost') # Field name made lowercase.
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    class Meta:
        db_table = u'status'

class Status2(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    time = models.DateTimeField(db_column='Time') # Field name made lowercase.
    queries = models.IntegerField(db_column='Queries') # Field name made lowercase.
    onlinehosts = models.IntegerField(db_column='OnlineHosts') # Field name made lowercase.
    class Meta:
        db_table = u'status2'

class Log(models.Model):
    
    lid = models.IntegerField(primary_key=True,db_column="LID")
    
    # Time - timestamp of logged activity
    time = models.IntegerField(db_column="Time",max_length=10) # !! Turn this into datefield after production
    
    # SearchString - site activities, categorized by start word
    #   'Browse:' - user navigating deep browse.
    #   'Search:' - user making regular search query
    #   'Request:' - user making request
    #   'Complete:' - user completing request
    #   'EditReq:' - User editing request
    #   'Poll:' - User creating poll
    searchstring = models.CharField(max_length=255,db_column="SearchString")
    
    # Client - IP of user
    client = models.CharField(max_length=64,db_column="Client")
    
    # Duration - fuck if I know. Honestly, some of the relic shit that's in this
    #            code, it's disgraceful.
    duration = models.FloatField(max_length=10, db_column="Duration", default=0)
    
    # Found - same here.
    found = models.IntegerField(max_length=10,db_column="Found", default=0)
    
    # Hits - how many results from a search query
    hits = models.IntegerField(max_length=10,db_column="Hits", default=0)
    
    # Position - what page of results, multiplied by PERPAGE
    position = models.IntegerField(max_length=10,db_column='Position', default=0)
    
    # Mode - which index searched
    #   1. Files
    #   2. Dirs
    #   3. FilesDirs
    mode = models.IntegerField(max_length=3,db_column="Mode",default=0)
    
    # HostType - type of share searched
    #   1: SMB & FTP
    #   2: FTP
    #   3: SMB <- the only one we use.
    hosttype = models.IntegerField(max_length=3,db_column="HostType",default=0)
    
    # Flags - means different things for different activities, I think
    #   Search: describes type of file searched for
    #       1: all files
    #       2: audio files
    #       3: video files
    #       4: software
    #       5: text
    #       6: images
    flags = models.IntegerField(max_length=3, db_column="Flags",default=0)
    date = models.IntegerField(max_length=10, db_column="Date",default=0)
    minsize = models.IntegerField(max_length=10,db_column="MinSize",default=0)
    maxsize = models.IntegerField(max_length=10,db_column="MaxSize",default=0)
    
    class Meta:
        db_table = u'log'