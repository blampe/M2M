from django.db import models

from themoviedb.tmdb import search, getMovieInfo, TmdHttpError
# Create your models here.


def getFromFiles(cls):
        ''' Imports things that are recognized as Movies from File table'''
        
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
            sliceIndex = candidate.filename.rfind('.')
            info = candidate.filename[:sliceIndex]
            
            # some people (coughWOPRcough) like to use '\.' instead of spaces, in their filenames.
            # fuck those people.
            
            info = re.split("\.",info)
            info = " ".join(info)
            info = re.split("\((.*)\)",info)
            
            probablyTitle = info[0].rstrip()
            # get some meta-data
            print "Stripping metadata out of title, if it's there."
            if len(info) > 1:
                diryear = re.search('((?P<DIRECTOR>(.+)) - )?(?P<YEAR>\d{4})', info[1])
                try: # if there's a year
                    year = diryear.group('YEAR')
                    print "Found year data."
                except KeyError:
                    year = ""
            
                try: # if there's a director
                    director = diryear.group('DIRECTOR')
                    print "Found director data."
                except KeyError:
                    director = ""
            else:
                year = ""
                director = ""
                    
            # find movies that match the title
            print "Querying TMDB... (%s) " % probablyTitle
            try:
                movies = search("%s %s" % (probablyTitle, year))
            except TmdHttpError, e:
                    print "TMDB not available: \n\t%s" % e
                    return
                    
            if len(movies) > 0:
                print "Found something!"
                                   
            for movieresult in movies[:10]:
                # now, get the info and put in the DB - if it's not already there.
                try:
                    checker = Movie.objects.get(pk=int(movieresult['id']))
                    print "Movie already in database; no new entry made."
                    print "Checking to see if this is a new host..."
                    if candidate in checker.FIDs:
                        print "Not a new file, moving on."
                        continue
                    else:
                        print "New file! adding to list of sources..."
                        checker.FIDs += candidate
                        checker.save()
                except:
                    movie = getMovieInfo(movieresult['id'])
                    print "Movie not in database:"
                    print "\t Found: %s" % movie['name']
                    
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
class Movie(models.Model):
    from themoviedb.tmdb import search,getMovieInfo
    
    ''' A movie that's been indexed. Necessarily a file, it also has other attributes.'''
    ID = models.IntegerField(primary_key=True)
    
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
    
    
            
            
