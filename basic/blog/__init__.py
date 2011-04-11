#from django.contrib.comments.models import Comment
#from django.core.mail import send_mail
#from django.dispatch import dispatcher
#from django.db.models import signals

# Get comment notifications

#def comment_notification(sender, instance):
#    subject = "New Comment on %s" % instance.get_content_object().title
#    msg = "Comment text: \n\n%s" % instance.comment
#    send_mail(subject, msg, 'news@m2m.st.hmc.edu', ['haak.erling@gmail.com'])
#
#dispatcher.connect(comment_notification, sender=Comment, signal=signals.post_save)
