from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Movie(models.Model):
    ''' A movie that's been indexed. Necessarily a file, it also has other attributes.'''
    
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    votes = models.IntegerField()
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2)
    cert = models.ForeignKey('MovieCert',related_name='movies',null=True,on_delete=models.SET_NULL)
    url = models.URLField()
    overview = models.TextField()
    popularity = models.IntegerField()
    imdb_id = models.CharField(max_length=100,null=True)
    released = models.DateField(null=True)
    adult = models.BooleanField()
    dateadded = models.DateTimeField()
    director = models.CharField(max_length=100)
    
    # There are lots of posters - for now, just store one of their URLs
    #...-cover.jpg
    poster = models.URLField()
    #...-thumb.jpg
    thumb = models.URLField()
    backdrop = models.URLField()
    
    runtime = models.TimeField(null=True)
    
    #endings = super.videoEndings
    
    def __unicode__(self):
        return u"{}".format(self.name)
        
class MovieGenre(models.Model):
    movies = models.ManyToManyField(Movie, related_name="genres",null=True)
    
    name = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return u'{}'.format(self.name)
    
class MovieCert(models.Model):
    
    cert = models.CharField(max_length=5,unique=True,null=True)
    
    def __unicode__(self):
        return u'{}'.format(self.cert)
        
class Episode(models.Model):
    ''' an episode of a tv show!'''
    
    season = models.ForeignKey('Season',null=True)
    episode = models.IntegerField()
    showName = models.ForeignKey('Show')
    episodeName = models.CharField(max_length=100)
    
    #endings = super.videoEndings
    def __unicode__(self):
        return u"{} S{}E{}".format(self.showName,self.season,self.episode)

class Season(models.Model):
    pass
        
class Show(models.Model):
    pass

        
class Song(models.Model):
    ''' Music file.'''
    
    artist = models.ForeignKey('Artist', null=True)
    album =  models.ForeignKey('Album', null=True)
    name = models.CharField(max_length=100)
    time = models.TimeField()
    explicit = models.BooleanField(default=False)
    tracknum = models.IntegerField()
    #endings = super.audioEndings
    appleID = models.BigIntegerField(null=True,unique=True)
    applePreview = models.URLField(null=True)
    
    dateadded = models.DateTimeField(null=True)
    
    #Matchtypes:
    # 1: perfect
    # 2: dir structure match
    # 3: ummm...dunno.
    matchtype = models.IntegerField()
    
    def __unicode__(self):
        return u"{}".format(self.name)

class MusicGenre(models.Model):
    songs = models.ManyToManyField(Song,related_name="genres", null=True)
    name = models.CharField(max_length=100,unique=True)
    
    def __unicode__(self):
        return u"{}".format(self.name)
    
class Album(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey('Artist', null=True)
    explicit = models.BooleanField(default=False)
    appleCover = models.URLField(null=True)
    cover = models.URLField(null=True)
    appleID = models.BigIntegerField(null=True,unique=True)
    no_cover = models.URLField(null=True)
    releaseDate = models.DateTimeField(null=True)
    
    dateadded = models.DateTimeField(null=True)
    
    def __init__(self,*args,**kwargs):
        models.Model.__init__(self,*args,**kwargs)
        
        self.trackCount = len(self.song_set.all())
    
    def __unicode__(self):
        return u"{}".format(self.name)
        
class Artist(models.Model):
    name = models.CharField(max_length=100)
    appleID = models.BigIntegerField(null=True,unique=True)
    
    dateadded = models.DateTimeField(null=True)
    
    def __unicode__(self):
        return u"{}".format(self.name)