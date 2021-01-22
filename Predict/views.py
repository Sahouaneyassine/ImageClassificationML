import os
from email.mime.image import MIMEImage

from django.shortcuts import render,get_object_or_404,redirect
from Predict.forms import InputForm
from Predict.models import Input
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

from django.core.mail import send_mail

from django.shortcuts import render
from keras.preprocessing import image
import numpy as np
import tensorflow as tf
from keras.models import load_model
global graph,model
import numpy as np
from keras.preprocessing import image
from random import randrange
# Create your views here.
print("Keras model loading.......")
model = load_model('Predict/catdog_cnn_model.h5')
print("Model loaded!!")


def home(request):
    id=0

    if request.method=="GET":
        return render(request,'Predict/home.html',{'form':InputForm(),'id':id})
    else:
        form = InputForm(request.POST,request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            newform.save()
            id=newform.id
            inputt = get_object_or_404(Input, pk=id)
            return redirect('results',inputt_id=id)
        else:
            print("error")
            form=InputForm()
            return render(request, 'Predict/home.html', {'form': InputForm() ,'id':id})



def results(request,inputt_id):

    inputt = get_object_or_404(Input, pk=inputt_id)
    imageee=inputt.photo.url

    from keras.preprocessing import image

    test_image = image.load_img(r""+imageee[1::], target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict_proba(test_image)




    print(result[0])
    if result[0][0] >= 0.5:
        prediction = 'this is ' + str(result[0][0] * 100) + ' % a ' + 'dog'

    else:
        prediction = 'this is ' + str((1-result[0][0]) * 100) + ' % a ' + 'cat'

    print(prediction)

    from pathlib import Path
    from email.mime.image import MIMEImage
    from django.core.mail import EmailMultiAlternatives

    recipient = "sahouaneyassine1999@gmail.com"
    sender = settings.EMAIL_HOST_USER  #
    image_path = imageee[1::]
    image_name = Path(image_path).name

    subject = "I am sending you nice image."
    text_message = f"Email with a nice embedded image "

    html_message = f"""
    <!doctype html>
        <html lang=en>
            <head>
                <meta charset=utf-8>
                <title>Some title.</title>
            </head>

            <body>
                <h1></h1>
                <p>
                Your Picture Prediction Results ---> {prediction}.<br>
                <img src='cid:{image_name}'/>
                </p>
            </body>
        </html>
    """

    # the function for sending an email
    def send_email(subject, text_content, html_content=None, sender=sender, recipient=recipient, image_path=None,
                   image_name=None):
        email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=sender,
                                       to=recipient if isinstance(recipient, list) else [recipient])

        if all([html_content, image_path, image_name]):
            email.attach_alternative(html_content, "text/html")
            email.content_subtype = 'html'  # set the primary content to be text/html
            email.mixed_subtype = 'related'  # it is an important part that ensures embedding of an image

            with open(image_path, mode='rb') as f:
                image = MIMEImage(f.read())
                email.attach(image)
                image.add_header('Content-ID', f"<{image_name}>")

        email.send()

    # send an test email
    send_email(subject="You Prediction Results", text_content=text_message, html_content=html_message, sender=sender, recipient=recipient,
               image_path=image_path, image_name=image_name)









    return render(request, 'Predict/results.html', {'input': inputt,'rslt':prediction})



















