from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from themoviedb.tmdb import search, getMovieInfo, TmdHttpError

import re
import datetime
# Create your models here.


def getMoviesFromFiles():
        ''' Imports things that are recognized as Movies from File table'''
        from search.models import File
        # grab all video files from things with Movie in the path name,
        # excluding things whose filename begin with '.' or '_'
        candidates = File.objects.filter(filenameend__regex=r'(%s)' % File.videoEndings)
        print "Filtered out non-(%s)" % File.videoEndings
        
        dirExcludes = "pornography"
        
        candidates = candidates.exclude(path__fullname__regex='(%s)' % dirExcludes)\
                               .filter(path__fullname__icontains='Movies')\
                               .exclude(filename__istartswith='.')\
                               .exclude(filename__istartswith='_')
        
        print "Filtered out things in (%s) directories, things not in movies" % dirExcludes
        
        # We should now have all likely video files.
        # Filter according to the regexp
        # (.)*( \((([a-zA-Z]) (- )?)?[12][0-9][0-9][0-9]\)\)?.(.)*
        # Filename[ ([Director [- ]]Year)].filenameend
        # so that we can use this shit with tmdb/imdb
        print "narrowing down filenames a little further..."
        candidates.filter(filename__regex=r'(.)+( \(([a-zA-Z]* (- )?)?[12][0-9][0-9][0-9]\)\))?.(.)*')
        
        for candidate in candidates:
            # get rid of the file extension
            print "  slicing off extension..."
            sliceIndex = candidate.filename.rfind('.')
            info = candidate.filename[:sliceIndex]
            
            # some people (coughWOPRcough) like to use '\.' instead of spaces, in their filenames.
            # fuck those people.
            
            info = re.split("\.",info)
            info = u" ".join(info)
            info = re.split("\((.*)\)",info)
            
            probablyTitle = info[0].rstrip()
            # now, clean up MORE BULLSHIT;
            # fuck you guys, we know it's 1080 or 720 or BLURAY
            # because it's a fucking HUGE file. Seriously.
            probablyTitle = probablyTitle.replace(' 1080p','').replace(' 720p','').replace(' bluray','')\
                            .replace(' hdtv','')
            
            # get some meta-data
            print "  Stripping metadata out of title, if it's there."
            if len(info) > 1:
                diryear = re.search('((?P<DIRECTOR>(.+)) - )?(?P<YEAR>\d{4})', info[1])
                try: # if there's a year
                    year = diryear.group('YEAR')
                    print "  Found year data."
                except KeyError:
                    year = ""
            
                try: # if there's a director
                    director = diryear.group('DIRECTOR')
                    print "  Found director data."
                except KeyError:
                    director = ""
            else:
                year = ""
                director = ""
                    
            # find movies that match the title
            string = "  Querying TMDB... (%s) " % probablyTitle
            print string.encode('utf-8')
            try:
                movies = search("%s %s" % (probablyTitle, year))
            except TmdHttpError, e:
                    print "  TMDB not available: \n\t%s" % e
                    return
                    
            if len(movies) > 0:
                print "  Found something!"
            else:
                print "  No love. Moving on!"
                continue
                                   
            for movieresult in movies[:1]:
                # now, get the info and put in the DB - if it's not already there.
                try:
                    checker = Movie.objects.get(pk=int(movieresult['id']))
                    print "    Movie already in database; no new entry made."
                    print "    Checking to see if this is a new file..."
                    if candidate in checker.files.all():
                        print "    Not a new file, moving on."
                        continue
                    else:
                        print "    New file! adding to list of sources..."
                        checker.files.add(candidate)
                        checker.save()
                        
                # this exception means, obviously, it's a new movie:
                except ObjectDoesNotExist:
                    movie = getMovieInfo(movieresult['id'])
                    print "    Movie not in database: %s\n" % movie['name']
                    certification=movie['certification'],
                    latestEntry = Movie(
                                id=int(movieresult['id']), # for API compatibility
                                rating=movie['rating'],
                                votes=int(movie['votes']),
                                name=movie['name'],
                                
                                url=movie['url'],
                                overview=movie['overview'],
                                popularity=int(movie['popularity']),
                                imdb_id=movie['imdb_id'], # in case we ever want to use imdb data
                                released=movie['released'],
                                adult=True if movie['adult']=='true' else False,
                                director=movie['cast']['director'][0]['name'],
                                #poster = movie['
                                #thumb =
                                #backdrop=
                                runtime=str(datetime.timedelta(minutes=int(movie['runtime']))),
                                goodfile=True
                                )
                    print "    adding %s to movie's file set..." % candidate
                    latestEntry.files.add(candidate)
                    # we have to save here, or the loop below will fail due to no entry in
                    # the movies table
                    latestEntry.save()
                    
                    print "    setting %s to movie's certification..." % movie['certification']
                    if len(MovieCert.objects.filter(cert=movie['certification'])) == 0:
                        cert = MovieCert.objects.create(cert=movie['certification'])
                    else:
                        cert = MovieCert.objects.get(cert=movie['certification'])
                    latestEntry.cert = cert
                    
                    print "    adding genres to movie's genres..."
                    for genre in movie['categories']['genre']:                    
                        if len(MovieGenre.objects.filter(name=genre)) == 0:
                            print "      Found a new genre, adding it to database..."
                            newGenre = MovieGenre(name=genre)
                            newGenre.save()
                        else:
                            newGenre = MovieGenre.objects.filter(name=genre)[0]
                        # add movie to genre and vice versa, then save genre (because we leave
                        # the genre object first!)
                        latestEntry.genres.add(newGenre)
                        newGenre.movies.add(latestEntry)
                        newGenre.save()
                        
                    latestEntry.save()
                    return latestEntry

class Movie(models.Model):
    ''' A movie that's been indexed. Necessarily a file, it also has other attributes.'''
    
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    studios = models
    votes = models.IntegerField()
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2)
    cert = models.ForeignKey('MovieCert',related_name='movies',null=True,on_delete=models.SET_NULL)
    url = models.URLField()
    overview = models.TextField()
    popularity = models.IntegerField()
    imdb_id = models.CharField(unique=True,max_length=100)
    released = models.DateField()
    adult = models.BooleanField()
    
    director = models.CharField(max_length=100)
    
    # There are lots of posters - for now, just store one of their URLs
    #...-cover.jpg
    poster = models.CharField(max_length=250)
    #...-thumb.jpg
    thumb = models.CharField(max_length=250)
    
    runtime = models.TimeField()
    goodfile = models.BooleanField()
    
    #endings = super.videoEndings
    
    def __unicode__(self):
        return "%s" % self.name

class MovieGenre(models.Model):
    movies = models.ManyToManyField(Movie, related_name="genres",null=True)
    
    name = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.name
    
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
    
    cert = models.CharField(max_length=5,unique=True)
    
    def __unicode__(self):
        return self.cert
        
class Show(models.Model):
    ''' an episode of a tv show!'''
    
    season = models.IntegerField()
    episode = models.IntegerField()
    showName = models.CharField(max_length=100)
    episodeName = models.CharField(max_length=100)
    
    #endings = super.videoEndings
    def __unicode__(self):
        return "%s S%dE%d" % (self.showName,self.season,self.episode)

class Music(models.Model):
    ''' Music file.'''
    
    artist = models.CharField(max_length=100)
    album =  models.CharField(max_length=100)
    trackName = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    time = models.TimeField()
    
    #endings = super.audioEndings
    
    def __unicode__(self):
        return "%s, %s" % (self.trackName, self.artist)
    
