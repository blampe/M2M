from django.db import models

import re
# Create your models here.


class Path(models.Model):
    pid = models.IntegerField(primary_key=True, db_column='PID') # Field name made lowercase.
    hash = models.IntegerField(db_column='Hash') # Field name made lowercase.
    ppid = models.IntegerField(db_column='PPID') # Field name made lowercase.
    hid = models.ForeignKey('Host',db_column='HID',related_name='browse_path_set') # Field name made lowercase.
    sid = models.ForeignKey('Share',db_column='SID') # Field name made lowercase.
    shortname = models.CharField(max_length=765, db_column='ShortName') # Field name made lowercase.
    fullname = models.CharField(max_length=765, db_column='FullName') # Field name made lowercase.
    pathsize = models.BigIntegerField(db_column='PathSize') # Field name made lowercase.
    dateadded = models.IntegerField(db_column='DateAdded') # Field name made lowercase.
    indexed = models.BooleanField(db_column='Indexed') # Field name made lowercase.
    
    
    def __unicode__(self):
        return self.fullname.decode('raw_unicode_escape').decode('utf-8')
    
    class Meta:
        db_table = u'path'

class Share(models.Model):
    shareid = models.IntegerField(primary_key=True, db_column='SID') # Field name made lowercase.
    hostid = models.ForeignKey('Host',db_column='HID') # Field name made lowercase.
    sharename = models.CharField(max_length=192, db_column='ShareName') # Field name made lowercase.
    login = models.CharField(max_length=96, db_column='Login') # Field name made lowercase.
    password = models.CharField(max_length=192, db_column='PassWord') # Field name made lowercase.
    totalfilesize = models.BigIntegerField(db_column='TotalFileSize') # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags') # Field name made lowercase.
    
    def __unicode__(self):
        return self.sharename.decode('raw_unicode_escape').decode('utf-8')
    
    class Meta:
        db_table = u'share'

class Smb(models.Model):
    hid = models.OneToOneField('Host',primary_key=True, db_column='HID') # Field name made lowercase.
    hostname = models.CharField(max_length=96, db_column='HostName',unique=True) # Field name made lowercase.
    workgroup = models.CharField(max_length=96, db_column='WorkGroup') # Field name made lowercase.
    login = models.CharField(max_length=96, db_column='Login') # Field name made lowercase.
    password = models.CharField(max_length=192, db_column='PassWord') # Field name made lowercase.
    def __unicode__(self):
        return self.hostname
    
    class Meta:
        db_table = u'smb'

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
    hasProblems = models.NullBooleanField(null=True,default=False)

    servesDirect = models.BooleanField()
    directPort = models.IntegerField(db_column="directPort")
    
    def __unicode__(self):
        if (re.search('dhcp',self.networkaddress,flags=re.IGNORECASE)) or (len(self.networkaddress) < 5): #dhcp links suck
            return self.ip
        else:
            return self.networkaddress
    
    class Meta:
        db_table = u'host'
