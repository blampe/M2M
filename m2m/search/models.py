from django.db import models
#from djangosphinx import SphinxSearch, SphinxRelation, SphinxQuerySet
#import djangosphinx.apis.current as sphinxapi



from advancedsearch.models import Movie, Episode, Song

from browseNet.models import Host, Path


# Create your models here.

class File(models.Model):
    '''An indexed file on the Network'''
    
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    MIDs = models.ForeignKey(Movie, related_name='files', null=True, on_delete=models.SET_NULL)
    SIDs = models.ForeignKey(Episode, null=True, related_name='files', on_delete=models.SET_NULL)
    MuIDs = models.ForeignKey(Song, null=True,related_name='files', on_delete=models.SET_NULL)
    path = models.ForeignKey(Path,db_column='PID') # Field name made lowercase.
    filename = models.CharField(max_length=765, db_column='FileName') # Field name made lowercase.
    filenameend = models.CharField(max_length=12, db_column='FileNameEnd') # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='DateAdded') # Field name made lowercase.
    filesize = models.BigIntegerField(db_column='FileSize') # Field name made lowercase.
    filedate = models.DateTimeField(db_column='FileDate') # Field name made lowercase.
    indexed = models.NullBooleanField(null=True, db_column='Indexed', blank=True) # Field name made lowercase.
    
    # good = 1, bad = 0, unclear = 3
    goodfile = models.IntegerField(default=1)
    objects = models.Manager()
    
    videoEndings    = ".avi|.mpg|.mp4|.m4v|.mov|.mpeg|.wmv|.mkv|.divx|.flv|.m2ts"
    audioEndings    = ".mp3|.flac|.ogg|.wma|.m4a|.aac|.wav|.aif|.au"
    textEndings     = ".txt|.chm|.pdf|.html|.rtf|.doc|.docx|.odt|.tex"
    imageEndings    = ".jpg|.jpeg|.raw|.tiff|.gif|.png|.psd|.tga|.tpic|.svg"
    
    
    def remove_problems(self):
        self.remove_dne_problem()
        self.remove_saving_problem()
    
    def remove_dne_problem(self):
        try:
            self.dneproblem
            self.dneproblem.delete()
            self.save()
        except:
            pass
    
    def remove_saving_problem(self):
        try:
            self.savingproblem
            self.savingproblem.delete()
            self.save()
        except:
            pass
    def remove_bad_file_problem(self):
        try:
            self.badfileproblem
            self.badfileproblem.delete()
            self.save()
        except:
            pass
    
    def remove_under_problem(self):
        try:
            self.undefproblem
            self.undefproblem.delete()
            self.save()
        except:
            pass
    
    def __unicode__(self):
        #-*-coding:iso-8859-1-*-
        return u'{}'.format(self.filename)
    
    class Meta:
        db_table = u'file'
        
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

