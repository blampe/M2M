from django.core.management.base import BaseCommand, CommandError

from advancedsearch import *

class Command(BaseCommand):
    args = ''
    help = "crawls for advanced search objects"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Cleaning house...")
        cleanHouse()
        
        self.stdout.write("Starting movie crawl...")
        crawlForMovies()
        
        self.stdout.write("Starting music crawl...")
        crawlForMusic()
        
        self.stdout.write("Crawl completed.")
        