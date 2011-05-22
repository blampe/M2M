from django.db import models
#from djangosphinx import SphinxSearch, SphinxRelation, SphinxQuerySet
#import djangosphinx.apis.current as sphinxapi

import re

from advancedsearch.models import Movie

from browseNet.models import Host, Path


# Create your models here.

class File(models.Model):
    '''An indexed file on the Network'''
    
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    MIDs = models.ForeignKey(Movie, "ID")
    path = models.ForeignKey(Path,db_column='PID') # Field name made lowercase.
    filename = models.CharField(max_length=765, db_column='FileName') # Field name made lowercase.
    filenameend = models.CharField(max_length=12, db_column='FileNameEnd') # Field name made lowercase.
    dateadded = models.IntegerField(db_column='DateAdded') # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FileSize') # Field name made lowercase.
    filedate = models.DateTimeField(db_column='FileDate') # Field name made lowercase.
    indexed = models.NullBooleanField(null=True, db_column='Indexed', blank=True) # Field name made lowercase.
    
    objects = models.Manager()
    
    videoEndings    = ".avi|.mpg|.mp4|.m4v|.mov|.mpeg|.wmv|.mkv|.divx|.flv|.m2ts"
    audioEndings    = ".mp3|.flac|.ogg|.wma|.m4a|.aac|.wav|.aif|.au"
    textEndings     = ".txt|.chm|.pdf|.html|.rtf|.doc|.docx|.odt|.tex"
    imageEndings    = ".jpg|.jpeg|.raw|.tiff|.gif|.png|.psd|.tga|.tpic|.svg"
    
    
    def __unicode__(self):
        #-*-coding:iso-8859-1-*-
        return self.filename.encode('raw_unicode_escape').decode('utf-8')
    
    class Meta:
        db_table = u'file'
        


class Show(models.Model):
    ''' an episode of a tv show!'''
    ID = models.IntegerField(primary_key=True)
    FID = models.ManyToOneRel(File, "id")
    season = models.IntegerField()
    episode = models.IntegerField()
    showName = models.CharField(max_length=100)
    episodeName = models.CharField(max_length=100)
    
    #endings = super.videoEndings
    
    
    @classmethod
    def getFromFiles(cls):
        ''' Imports things that are recognized as TV Shows from File table'''

class Music(models.Model):
    ''' Music file.'''
    ID = models.IntegerField(primary_key=True)
    FID = models.ManyToOneRel(File, "id")
    artist = models.CharField(max_length=100)
    album =  models.CharField(max_length=100)
    trackName = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    time = models.TimeField()
    
    #endings = super.audioEndings
    
    @classmethod
    def getFromFiles(cls):
        ''' Imports things that are recognized as Music from File table'''


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

