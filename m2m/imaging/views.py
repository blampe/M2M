from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
# Create your views here.

import PIL
from PIL import ImageFont, Image, ImageDraw

from advancedsearch.models import Movie

from django.conf import settings

def bad_request(request):
    response = HttpResponse(mimetype="image/gif")
    img = Image.open("C:/Users/haak/M2M/m2m/media/images/badfile.gif" if settings.DEBUG else "/home/haak/M2M/m2m/media/images/badfile.gif")
    
    img.save(response,"GIF")
    return response

    

def no_poster(request,id):
    id = int(id)
    try:
        movie = Movie.objects.get(pk=id)
    except:
        return bad_request(request)
        
    fnt = ImageFont.truetype("StencilStd.otf" if settings.DEBUG else "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf", 25)
    response = HttpResponse(mimetype="image/jpeg")
    img = Image.open("C:/Users/haak/M2M/m2m/media/images/no_poster.jpg" if settings.DEBUG else "/home/haak/M2M/m2m/media/images/no_poster.jpg")

    draw = ImageDraw.Draw(img)
    txtsize = draw.textsize(movie.name,font=fnt)
#   x = (img.size[0]/2) - (txtsize[0]/2) # for centered text
  
    draw_word_wrap(img, movie.name, fnt,
                    ypos = 10,
                    max_width=img.size[0],fill=(255,255,255))
    
    img.save(response,"JPEG")
    return response
    
    
def draw_word_wrap(img, text, font,xpos=0, ypos=0, max_width=130,
                   fill=(0,0,0)):
    '''Draw the given ``text`` to the x and y position of the image, using
    the minimum length word-wrapping algorithm to restrict the text to
    a pixel width of ``max_width.``
    '''
    draw = ImageDraw.Draw(img)
    text_size_x, text_size_y = draw.textsize(text, font=font)
    remaining = max_width
    space_width, space_height = draw.textsize(' ', font=font)
    # use this list as a stack, push/popping each line
    output_text = []
    # split on whitespace...    
    for word in text.split(None):
        word_width, word_height = draw.textsize(word, font=font)
        if word_width + space_width > remaining:
            output_text.append(word)
            remaining = max_width - word_width
        else:
            if not output_text:
                output_text.append(word)
            else:
                output = output_text.pop()
                output += ' %s' % word
                output_text.append(output)
            remaining = remaining - (word_width + space_width)
    for text in output_text:
        draw.text((xpos, ypos), text, font=font, fill=fill)
        ypos += text_size_y