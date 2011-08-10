from django.core.management.base import BaseCommand, CommandError

from advancedsearch import *

class Command(BaseCommand):
    args = ''
    help = "crawls for advanced search objects"
    
    def handle(self, *args, **kwargs):
        # we've decided not to do this, for now;
        # there's no reason to delete the un-filed advanced models,
        # and they're nice to have for stats purposes.
        # plus, if we already have them in memory, when/if they reappear
        # we don't have to slow down to talk to an external database.
        # instamatch!

        #self.stdout.write("Cleaning house...")
        #cleanHouse()
        
        self.stdout.write("Starting movie crawl...")
        crawlForMovies()
        
        self.stdout.write("Starting music crawl...")
        crawlForMusic()
        
        self.stdout.write("Crawl completed.")
        
