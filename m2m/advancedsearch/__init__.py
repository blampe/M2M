from django.core.exceptions import ObjectDoesNotExist

from themoviedb.tmdb import search, getMovieInfo, TmdHttpError


import re
import datetime


from models import Movie, Show, Music
from search.models import File
from problems.models import DNEProblem, SavingProblem, ProblemSet

def logComplaints(issues=False):
    ''' issues should be in (problemfiles,couldnotmatchfiles) format'''
    if not issues:
        return
    # fuck the saveSet for now, it's not as interesting.
    #saveSet = File.objects.filter(id__in=[x.id for x in saveIssues])
    
    for f in issues['nomatches']:
        try:
            pset = f.path.hid.problems
        except:
            pset = ProblemSet.objects.create(host=f.path.hid)
        try:
            f.dneproblem
        except:
            prob = DNEProblem(file=f)
            prob.save()
            pset.dneproblem_set.add(prob)
            pset.save()
    
    return

    
def crawlForMovies(count=0):
    ''' Imports things that are recognized as Movies from File table'''
    
    # grab all video files from things with Movie in the path name,
    # excluding things whose filename begin with '.' or '_'
    print "Filtering out non-(%s)" % File.videoEndings
    candidates = File.objects.filter(filenameend__regex=r'(%s)' % File.videoEndings)
    
    dirExcludes = "pornography"
    print "Filtering out things in (%s) directories, things not in movies" % dirExcludes
    candidates = candidates.exclude(path__fullname__regex='(%s)' % dirExcludes)\
                           .filter(path__fullname__icontains='Movies')\
                           .exclude(filename__istartswith='.')\
                           .exclude(filename__istartswith='_')
    
    
    
    # We should now have all likely video files.
    # Filter according to the regexp
    # (.)*( \((([a-zA-Z]) (- )?)?[12][0-9][0-9][0-9]\)\)?.(.)*
    # Filename[ ([Director [- ]]Year)].filenameend
    # so that we can use this shit with tmdb/imdb
    print "Narrowing down filenames a little further to deal with \"(director - year)\" construction"
    candidates.filter(filename__regex=r'(.)+( \(([a-zA-Z]* (- )?)?[12][0-9][0-9][0-9]\)\))?.(.)*')
    
    #issues = {}
    
    #issues['problems'] = []
    #issues['nomatches'] = []
    
    total = len(candidates)
    print "%d files to check. Here we go..." % total
    for candidate in candidates[count:]:
        candidate.remove_problems()
        try:
            pset = candidate.path.hid.problems
        except:
            pset = ProblemSet()
            pset.host = candidate.path.hid
            pset.save()
    
        count += 1
        # skip all of this if the file already has a movie
        print candidate.id
        try:
            if candidate.MIDs != None:
                print "  Candidate file %s is already recognized; moving on!" % candidate.id
                continue
        except ObjectDoesNotExist:
            # an old movie file was deleted
            print "  Previous movie no longer extant, resetting link..."
            candidate.MIDs = None
            candidate.save()
        # get rid of the file extension
        print "#%d out of %d" % (count, total)
        print "  Candidate (ID %d): %s " % (candidate.id, candidate)
        print "  slicing off extension..."
        sliceIndex = candidate.filename.rfind('.')
        info = candidate.filename[:sliceIndex]
        
        # some people (coughWOPRcough) like to use '\.' instead of spaces, in their filenames.
        # fuck those people.
        info = re.split("\.",info)
        info = u" ".join(info)
        info = re.split("\((.*)\)",info)
        
        
        # also '_'
        probablyTitle = info[0].rstrip().replace('_',' ')
        
        # ignore anything between {}
        
        probablyTitle = re.sub(r'{.*}','',probablyTitle)
        probablyTitle = probablyTitle.replace('  ',' ')
        
        # now, clean up MORE BULLSHIT;
        # fuck you guys, we know it's 1080 or 720 or BLURAY
        # because it's a fucking HUGE file. Seriously.
 #       probablyTitle = probablyTitle.replace(' 1080p','').replace(' 720p','').replace(' bluray','')\
 #                       .replace(' hdtv','').replace(' 456p','').replace(' dvd','').replace(' 524p','')\
 #                       .replace(' 368p','').replace(' 400p','').replace(' 480p','').replace(' 336p','')\
 #                       .replace(' 432p','').replace(' tv','').replace(' 340p','').replace(' 346p','')\
 #                       .replace(' 455p','')
        # oh my god fuck this
        
        print "    Stripping out retarded information..."
        extraShit = ['[',']',' dvdrip',' dvdscr',' hddvd',' dvd',' hdtv',' tv',' bluray',' ts',]
        for shit in extraShit:
            probablyTitle = probablyTitle.replace('%s'%shit,'')
            
        # fuck youu ###(#)?pppppp
        bitches = re.split(" \d{3,4}p",probablyTitle)
        
        probablyTitle = ''.join(bitches)
        # get some meta-data
        print "  Stripping metadata out of title, if it's there."
        if len(info) > 1:
            meta = re.search('((?P<DIRECTOR>(.+)) - )?(?P<YEAR>\d{4})', info[1])
            try: # if there's a year
                try:
                    year = meta.group('YEAR')
                    print "  Found year data."
                except:
                    print "  No year data."
                    year = ""
            except KeyError:
                year = ""
        else:
            year = ""
                
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
            candidate.remove_dne_problem()
        else:
            # add problem for later perusal
            candidate.remove_dne_problem()
            prob = DNEProblem()
            prob.file = candidate
            prob.save()
            pset.dneproblem_set.add(prob)
            pset.save()
            
            print "  No love. Moving on!"
            #issues['nomatches'] += [candidate]
            continue
            
        # only take the first result, which is the most likely
        
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
                
                print "    Movie not in database: %s\n" % movie['name'].encode('utf-8')
                certification=movie['certification'],
                latestEntry = Movie(
                            id=int(movieresult['id']), # for API compatibility
                            rating=movie['rating'],
                            votes=int(movie['votes']),
                            name=movie['name'].encode('utf-8'),
                            dateadded=datetime.datetime.now(),
                            url=movie['url'],
                            overview=movie['overview'] if movie['overview'] else 'No overview available',
                            popularity=int(movie['popularity']),
                            imdb_id=movie['imdb_id'] if movie['imdb_id'] else None, # in case we ever want to use imdb data
                            released=movie['released'] if movie['released'] else None,
                            adult=True if movie['adult']=='true' else False,
                            director=movie['cast']['director'][0]['name'] if movie['cast'].has_key('director') else 'Unknown',
                            backdrop=movieresult['images'][1]['poster'] if len(movie['images'])>1 and movie['images'][1].has_key('poster') else '/media/images/no_backdrop.jpg',
                            poster = movie['images'][0]['cover'] if len(movie['images'])>0 and movie['images'][0].has_key('cover') else '/media/images/no_poster.jpg',
                            thumb = movie['images'][0]['thumb'] if len(movie['images'])>0 and movie['images'][0].has_key('thumb') else '/media/images/no_thumb.jpg',
                            runtime=str(datetime.timedelta(minutes=int(movie['runtime']))) if movie['runtime'] else None,
                            )
                print "    adding %s to movie's file set..." % candidate
                latestEntry.files.add(candidate)
                # we have to save here, or the loop below will fail due to no entry in
                # the movies table
                try:
                    latestEntry.save()
                except:
                    print "    Something went wrong; moving on."
                    prob = SavingProblem()
                    prob.file = candidate
                    prob.save()
                    pset.savingproblem_set.add(prob)
                    pset.save()
                    #issues['problems']+= [candidate]
                    
                candidate.remove_saving_problem()
                
                
                print "    setting %s to movie's certification..." % movie['certification']
                if len(MovieCert.objects.filter(cert="None" if movie['certification']==None else movie['certification'])) == 0:
                    print  "      Found a new cert, adding to database..."
                    cert = MovieCert.objects.create(cert="None" if movie['certification']==None else movie['certification'])
                else:
                    cert = MovieCert.objects.get(cert="None" if movie['certification']==None else movie['certification'])
                latestEntry.cert = cert
                
                print "    adding genres to movie's genres..."
                if movie['categories'].has_key('genre'):
                    for genre in movie['categories']['genre']:                    
                        if len(MovieGenre.objects.filter(name=genre)) == 0:
                            print "      Found a new genre, adding it to database..."
                            newGenre = MovieGenre(name=genre)
                            newGenre.save()
                        else:
                            newGenre = MovieGenre.objects.get(name=genre)
                        # add movie to genre and vice versa, then save genre (because we leave
                        # the genre object first!)
                        latestEntry.genres.add(newGenre)
                        newGenre.movies.add(latestEntry)
                        newGenre.save()
                else:
                    latestEntry.genres.add(MovieGenre.objects.get(name="None"))
                latestEntry.save()
               
    print "Success."
    # store problems in database
    #logComplaints(issues)
    return 