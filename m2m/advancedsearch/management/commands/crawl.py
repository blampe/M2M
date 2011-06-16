from django.core.management.base import BaseCommand, CommandError

from advancedsearch import *

class Command(BaseCommand):
    args = ''
    help = "crawls for advanced search objects"
    
    def handle(self, *args, **kwargs):
        crawlForMovies()
        
        self.stdout.write("Crawl completed.")
        