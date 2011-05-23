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
        return u"%s" % self.name

class MovieGenre(models.Model):
    movies = models.ManyToManyField(Movie, related_name="genres",null=True)
    
    name = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    # this is dumb. why isn't this handled automatically?
    #def save(self,*args,**kwargs):
    #    if not self.ID:
    #        i = list(MovieGenre.objects.raw('SELECT * FROM advancedsearch_moviegenre ORDER BY ID DESC LIMIT 1'))
    #        if len(i) < 1:
    #            self.ID = 1
    #        else:
    #            self.ID = i[0].ID+1
    #    models.Model.save(self,*args,**kwargs)

class MovieCert(models.Model):
    
    cert = models.CharField(max_length=5,unique=True,null=True)
    
    def __unicode__(self):
        return u'%s' % self.cert
        
class Show(models.Model):
    ''' an episode of a tv show!'''
    
    season = models.IntegerField()
    episode = models.IntegerField()
    showName = models.CharField(max_length=100)
    episodeName = models.CharField(max_length=100)
    
    #endings = super.videoEndings
    def __unicode__(self):
        return u"%s S%dE%d" % (self.showName,self.season,self.episode)

class Music(models.Model):
    ''' Music file.'''
    
    artist = models.CharField(max_length=100)
    album =  models.CharField(max_length=100)
    trackName = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    time = models.TimeField()
    
    #endings = super.audioEndings
    
    def __unicode__(self):
        return u"%s, %s" % (self.trackName, self.artist)
    
