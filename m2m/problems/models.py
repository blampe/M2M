from django.db import models

# Create your models here.
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors

import re

from browseNet.models import Host
from search.models import File

styles = getSampleStyleSheet()

styleH = styles['Heading3']
styleN = styles['Normal']

class ProblemSet(models.Model):
    host = models.OneToOneField(Host, related_name='problems', null=True)
    
    def render(self, Story):
        if self.savingproblem_set.all():
            for p in self.savingproblem_set.all():
                Story = p.render(Story)
        if self.dneproblem_set:
            for p in self.dneproblem_set.all():
                Story = p.render(Story)
        if self.undefproblem_set:
            for p in self.undefproblem_set.all():
                Story = p.render(Story)
        return Story
    def count(self, *args, **kwargs):
        count = 0
        if self.savingproblem_set.all():
            count += self.savingproblem_set.count()
        if self.dneproblem_set:
            count += self.dneproblem_set.count()
        if self.undefproblem_set:
            count += self.dneproblem_set.count()
        return count
    def save(self, *args, **kwargs):
        if self.savingproblem_set.all() or self.dneproblem_set.all() or self.undefproblem_set.all():
            self.host.hasProblems = True
        else:
            self.host.hasProblems = False
        self.host.save()
        models.Model.save(self, *args, **kwargs)
    
    def __unicode__(self):
        return " Problems on %s" % self.host
        
    def __iter__(self):
        if self.savingproblem_set:
            for p in self.savingproblem_set.all():
                yield p
        if self.dneproblem_set:
            for p in self.dneproblem_set.all():
                yield p
        if self.undefproblem_set:
            for p in self.undefproblem_set.all():
                yield p         
        
class Problem(models.Model):
    file = models.OneToOneField(File, related_name="%(class)s", null=True, blank=True)
    pathology = models.ForeignKey(ProblemSet,related_name="%(class)s_set", null=True, blank=True)
    
    name = "Problem"# for printing stuff, redefine this
    
    def render(self, Story):
        raise NotImplementedError("Should have something here")
    
    def render_pdf(self):
        raise NotImplementedError("Should have something here")
    
    def docPage(canvas,doc):
        raise NotImplementedError("Should have something here")
        
    def __unicode__(self):
        return "%s: %d" % (self.name,self.file.id)
        
    class Meta:
        abstract = True
    
class SavingProblem(Problem):
    ''' these are things that failed to update after being linked to an advanced type'''
    name = "Saving Problem" 
    
    def docPage(canvas,doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 10)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - (.25 * inch), Title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(7 * inch, .75 * inch, "Page %d" % (doc.page,))
        canvas.restoreState()
    
    def render(self, Story):
        return self.render_pdf(Story)
        
    def render_pdf(self, Story):
        Story.append(Paragraph("<strong>Files that would not accept advanced links, but should have them:</strong>",
                               styleH))
        for file in self.files:
            Story.append(Paragraph("%s" % file.filename,styleN))
            
        Story.append(Paragraph("There's probably not alot you can do about these files - something about our representation of them is causing problems. This is just to let you know.",styleN))
        return Story
    
    def __unicoode__(self):
        return u"Did Not Save Problem: %d" % self.file.filename
    
        
class DNEProblem(Problem):
    ''' these are things that did not match to an external database - probably a naming issue'''
    
    name = "NoMatch Problem"
    
    def docPage(canvas,doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 10)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - (.25 * inch), Title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(7 * inch, .75 * inch, "Page %d" % (doc.page,))
        canvas.restoreState()
        
        def __unicode__(self):
            return u"Could Not Match Problem: %d" % self.file.id
    
        def render(self, Story):
            return self.render_pdf(Story)
        
        def render_pdf(self,Story):
            Story.append(Paragraph("<strong>Files that couldn't be matched against a database, but probably should have been found:</strong>",styleH))
            for file in self.files:
                Story.append(Paragraph("%s" % file.filename, styleN))
            Story.append(Paragraph("Movies should NOT have 'blueray', 'hdtv', 'tv', '480p' or any of that shit in their names. We can tell, honestly, from the file size, and I can't keep up with the extra fluff to strip it out; I can't catch everything.",styleN))
            return Story

class BadFileProblem(Problem):
    ''' bad files on a host'''
    name = "Bad Files"
    
    def docPage(canvas,doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 10)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - (.25 * inch), Title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(7 * inch, .75 * inch, "Page %d" % (doc.page,))
        canvas.restoreState()    
    
            
class UndefProblem(Problem):
    ''' No category problem'''
    
    name = "Unknown Problem"
    
    def docPage(canvas,doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 10)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - (.25 * inch), Title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(7 * inch, .75 * inch, "Page %d" % (doc.page,))
        canvas.restoreState()
        
        def __unicode__(self):
            return u"Undefined Problem: %d" % self.file.id        
