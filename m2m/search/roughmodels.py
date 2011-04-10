# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Admin(models.Model):
    aid = models.IntegerField(primary_key=True, db_column='AID') # Field name made lowercase.
    login = models.CharField(max_length=96, db_column='Login') # Field name made lowercase.
    password = models.CharField(max_length=96, db_column='PassWord') # Field name made lowercase.
    name = models.CharField(max_length=96, db_column='Name') # Field name made lowercase.
    www = models.CharField(max_length=765, db_column='WWW') # Field name made lowercase.
    email = models.CharField(max_length=192, db_column='Email') # Field name made lowercase.
    rights = models.IntegerField(db_column='Rights') # Field name made lowercase.
    logintime = models.IntegerField(db_column='LoginTime') # Field name made lowercase.
    loginip = models.CharField(max_length=48, db_column='LoginIP') # Field name made lowercase.
    class Meta:
        db_table = u'admin'

class Comments(models.Model):
    cid = models.IntegerField(primary_key=True, db_column='CID') # Field name made lowercase.
    time = models.IntegerField(db_column='Time') # Field name made lowercase.
    name = models.CharField(max_length=120, db_column='Name') # Field name made lowercase.
    email = models.CharField(max_length=180, db_column='Email') # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True) # Field name made lowercase.
    completed = models.IntegerField(db_column='Completed') # Field name made lowercase.
    completedname = models.CharField(max_length=120, db_column='CompletedName', blank=True) # Field name made lowercase.
    completedemail = models.CharField(max_length=120, db_column='CompletedEmail', blank=True) # Field name made lowercase.
    completedcomment = models.TextField(db_column='CompletedComment', blank=True) # Field name made lowercase.
    completedtime = models.IntegerField(null=True, db_column='CompletedTime', blank=True) # Field name made lowercase.
    
    def __unicode__(self):
        return self.comment
    
    class Meta:
        db_table = u'comments'

class File(models.Model):
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    pid = models.IntegerField(db_column='PID') # Field name made lowercase.
    filename = models.CharField(max_length=765, db_column='FileName') # Field name made lowercase.
    filenameend = models.CharField(max_length=12, db_column='FileNameEnd') # Field name made lowercase.
    dateadded = models.IntegerField(db_column='DateAdded') # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FileSize') # Field name made lowercase.
    filedate = models.DateTimeField(db_column='FileDate') # Field name made lowercase.
    indexed = models.IntegerField(null=True, db_column='Indexed', blank=True) # Field name made lowercase.
    
    def __unicode__(self):
        return self.filename
    
    class Meta:
        db_table = u'file'

class Ftp(models.Model):
    hid = models.IntegerField(db_column='HID') # Field name made lowercase.
    hostname = models.CharField(max_length=192, db_column='HostName') # Field name made lowercase.
    login = models.CharField(max_length=96, db_column='Login') # Field name made lowercase.
    password = models.CharField(max_length=192, db_column='PassWord') # Field name made lowercase.
    port = models.IntegerField(db_column='Port') # Field name made lowercase.
    startingdir = models.CharField(max_length=384, db_column='StartingDir') # Field name made lowercase.
    filelist = models.CharField(max_length=384, db_column='FileList') # Field name made lowercase.
    comment = models.CharField(max_length=765, db_column='Comment') # Field name made lowercase.
    editableby = models.CharField(max_length=192, db_column='EditableBy') # Field name made lowercase.
    
    def __unicode__(self):
        return self.hostname+":"+self.port
    
    class Meta:
        db_table = u'ftp'

class History(models.Model):
    uid = models.IntegerField(db_column='UID') # Field name made lowercase.
    position = models.IntegerField(db_column='Position') # Field name made lowercase.
    searchstring = models.CharField(max_length=765, db_column='SearchString') # Field name made lowercase.
    mode = models.IntegerField(db_column='Mode') # Field name made lowercase.
    hosttype = models.IntegerField(db_column='HostType') # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags') # Field name made lowercase.
    date = models.IntegerField(db_column='Date') # Field name made lowercase.
    datevalue = models.IntegerField(db_column='DateValue') # Field name made lowercase.
    minsize = models.IntegerField(db_column='MinSize') # Field name made lowercase.
    maxsize = models.IntegerField(db_column='MaxSize') # Field name made lowercase.
    hits = models.IntegerField(db_column='Hits') # Field name made lowercase.
    class Meta:
        db_table = u'history'

class Host(models.Model):
    hid = models.IntegerField(primary_key=True, db_column='HID') # Field name made lowercase.
    ip = models.CharField(max_length=48, db_column='IP') # Field name made lowercase.
    hosttype = models.IntegerField(db_column='HostType') # Field name made lowercase.
    expirecount = models.IntegerField(db_column='ExpireCount') # Field name made lowercase.
    period = models.IntegerField(db_column='Period') # Field name made lowercase.
    counter = models.IntegerField(db_column='Counter') # Field name made lowercase.
    scanorder = models.IntegerField(db_column='ScanOrder') # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags') # Field name made lowercase.
    lastscan = models.DateTimeField(db_column='LastScan') # Field name made lowercase.
    totalfilesize = models.BigIntegerField(db_column='TotalFileSize') # Field name made lowercase.
    networkaddress = models.CharField(max_length=192, db_column='NetworkAddress') # Field name made lowercase.
    
    def __unicode__(self):
        return self.networkaddress
    
    class Meta:
        db_table = u'host'

class Log(models.Model):
    lid = models.IntegerField(primary_key=True, db_column='LID') # Field name made lowercase.
    time = models.IntegerField(db_column='Time') # Field name made lowercase.
    duration = models.FloatField(db_column='Duration') # Field name made lowercase.
    found = models.IntegerField(db_column='Found') # Field name made lowercase.
    hits = models.IntegerField(db_column='Hits') # Field name made lowercase.
    position = models.IntegerField(db_column='Position') # Field name made lowercase.
    client = models.CharField(max_length=192, db_column='Client') # Field name made lowercase.
    searchstring = models.CharField(max_length=765, db_column='SearchString') # Field name made lowercase.
    mode = models.IntegerField(db_column='Mode') # Field name made lowercase.
    hosttype = models.IntegerField(db_column='HostType') # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags') # Field name made lowercase.
    date = models.IntegerField(db_column='Date') # Field name made lowercase.
    minsize = models.IntegerField(db_column='MinSize') # Field name made lowercase.
    maxsize = models.IntegerField(db_column='MaxSize') # Field name made lowercase.
    class Meta:
        db_table = u'log'

class Path(models.Model):
    pid = models.IntegerField(primary_key=True, db_column='PID') # Field name made lowercase.
    hash = models.IntegerField(db_column='Hash') # Field name made lowercase.
    ppid = models.IntegerField(db_column='PPID') # Field name made lowercase.
    hid = models.IntegerField(db_column='HID') # Field name made lowercase.
    sid = models.IntegerField(db_column='SID') # Field name made lowercase.
    shortname = models.CharField(max_length=765, db_column='ShortName') # Field name made lowercase.
    fullname = models.CharField(max_length=765, db_column='FullName') # Field name made lowercase.
    pathsize = models.BigIntegerField(db_column='PathSize') # Field name made lowercase.
    dateadded = models.IntegerField(db_column='DateAdded') # Field name made lowercase.
    indexed = models.IntegerField(db_column='Indexed') # Field name made lowercase.
    class Meta:
        db_table = u'path'

class Share(models.Model):
    sid = models.IntegerField(primary_key=True, db_column='SID') # Field name made lowercase.
    hid = models.IntegerField(db_column='HID') # Field name made lowercase.
    sharename = models.CharField(max_length=192, db_column='ShareName') # Field name made lowercase.
    login = models.CharField(max_length=96, db_column='Login') # Field name made lowercase.
    password = models.CharField(max_length=192, db_column='PassWord') # Field name made lowercase.
    totalfilesize = models.BigIntegerField(db_column='TotalFileSize') # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags') # Field name made lowercase.
    
    def __unicode(self):
        return self.sharename
    
    class Meta:
        db_table = u'share'

class Smb(models.Model):
    hid = models.IntegerField(db_column='HID') # Field name made lowercase.
    hostname = models.CharField(max_length=96, db_column='HostName') # Field name made lowercase.
    workgroup = models.CharField(max_length=96, db_column='WorkGroup') # Field name made lowercase.
    login = models.CharField(max_length=96, db_column='Login') # Field name made lowercase.
    password = models.CharField(max_length=192, db_column='PassWord') # Field name made lowercase.
    
    def __unicode__(self):
        return self.hostname
    
    class Meta:
        db_table = u'smb'

class SphinxTestJjs092348792(models.Model):
    id = models.BigIntegerField(primary_key=True)
    field1 = models.TextField(blank=True)
    field2 = models.TextField(blank=True)
    attr1 = models.IntegerField()
    lat = models.FloatField()
    long = models.FloatField()
    class Meta:
        db_table = u'sphinx_test_jjs_092348792'

class Status(models.Model):
    lastchange = models.CharField(max_length=90, db_column='LastChange', blank=True) # Field name made lowercase.
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

class User(models.Model):
    uid = models.IntegerField(primary_key=True, db_column='UID') # Field name made lowercase.
    lastsearched = models.IntegerField(db_column='LastSearched') # Field name made lowercase.
    current = models.IntegerField(db_column='Current') # Field name made lowercase.
    save = models.IntegerField(db_column='Save') # Field name made lowercase.
    class Meta:
        db_table = u'user'

