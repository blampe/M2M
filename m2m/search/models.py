from django.db import models
#from djangosphinx import SphinxSearch, SphinxRelation, SphinxQuerySet
#import djangosphinx.apis.current as sphinxapi

import re

from browseNet.models import Host, Path


# Create your models here.

class File(models.Model):
    '''An indexed file on the Network'''
    id = models.IntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
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
        


class Movie(models.Model):
    from themoviedb.tmdb import search,getMovieInfo
    
    ''' A movie that's been indexed. Necessarily a file, it also has other attributes.'''
    ID = models.IntegerField(primary_key=True)
    FIDs = models.ForeignKey(File, "id")
    
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    studios = models
    votes = models.IntegerField()
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2)
    certification = models.CharField(max_length=10)
    url = models.URLField()
    overview = models.TextField()
    popularity = models.IntegerField()
    imdb_id = models.CharField(unique=True,max_length=100)
    released = models.DateField()
    adult = models.BooleanField()
    
    genre = models.CharField(max_length=10)
    director = models.CharField(max_length=100)
    
    # There are lots of posters - for now, just store one of their URLs
    #...-cover.jpg
    poster = models.CharField(max_length=250)
    #...-thumb.jpg
    thumb = models.CharField(max_length=250)
    
    runtime = models.TimeField()
    goodfile = models.BooleanField()
    
    #endings = super.videoEndings
    
    @classmethod
    def getFromFiles(cls):
        ''' Imports things that are recognized as Movies from File table'''
        
        # grab all video files from things with Movie in the path name,
        # excluding things whose filename begin with '.' or '_'
        candidates = []
        for fileType in File.videoEndings.split('|'):
            candidates += File.objects.exclude(path__fullname__icontains='Pornography')\
                            .filter(path__fullname__icontains='Movies')\
                            .filter(filenameend__iexact=fileType)\
                            .exclude(filename__istartswith='.')\
                            .exclude(filename__istartswith='_')
            
        # We should now have all likely video files.
        # Filter according to the regexp
        # (.)*( \((([a-zA-Z]) (- )?)?[12][0-9][0-9][0-9]\)\)?.(.)*
        # Filename[ ([Director [- ]]Year)].filenameend
        # so that we can use this shit with tmdb/imdb
        candidates.filter(filename__regex=r'(.)+( \(([a-zA-Z]* (- )?)?[12][0-9][0-9][0-9]\)\))?.(.)*')
        
        for candidate in candidates:
            sliceIndex = candidate.filename.rfind('.')
            info = candidate.filename[:sliceIndex]
            info = re.split("\((.*)\)\Z",info)
            probablyTitle = info[0].rstrip()
            # get some meta-data
            if len(info) > 1:
                diryear = re.search('((?P<DIRECTOR>(.+)) - )?(?P<YEAR>\d{4})', info[1])
                try: # if there's a year
                    year = diryear.group('YEAR')
                except KeyError:
                    year = ""
                try: # if there's a director
                    director = diryear.group('DIRECTOR')
                except KeyError:
                    director = ""
                    
            # find movies that match the title
            movies = search("%s %s" % (probablyTitle, year))
            for movieresult in movies:
                # now, get the info and put in the DB - if it's not already there.
                try:
                    checker = Movie.objects.get(pk=int(movieresult['id']))
                    continue
                except:
                    movie = getMovieInfo(movieresult['id'])
                    '''latestEntry = Movie(
                                rating=movie['rating'],
                                votes=movie['votes'],
                                name=movie['name'],
                                certification=movie['certification'],
                                url=movie['url'],
                                overview=movie['overview']
                                popularity=moveie['popularity'],
                                imdb_id=movie['imdb_id']
                                released=movie['released'],
                                adult=movie['adult'],
                                genre=movie['genre'],
                                director=director
                                poster = movie['
                                thumb =
                                backdrop=
                                runtime=
                                goodfile=True)'''
            
            

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

