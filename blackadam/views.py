from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import wget
import requests
import os


# Create your views here.
from blackadam.scripts import audio_file



PAGE_TOKEN='EAATCCukVUwkBAI9ZBY5kHy12ZCIMaogxuLxNnhgEnfUkpZB9mxTdxWmBnhsZCuE50UYFLoHJNStNTJAbcw64k8KUWFrT9xJtgLuyRbE35PZBh7uY6or8VZAIoJ4R6Jw3KUAQFwIJNFSLRiqLOEiKatHetVstvlpi8OH4a8vi2AoAZDZD'



@csrf_exempt
def webhook(request):
    if (request.method=="GET"):
        if(request.GET['hub.verify_token']=="blackadam"):
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse("Wrong verification token")

    if (request.method=="POST"):
        dict=json.loads(request.body.decode('utf-8'))

        try:
            for entry in dict['entry']:

                for message in entry['messaging']:

                    recipient_id = message['sender']['id']



                    '''
                    Get Started Button Code

                    '''
                    try:
                        if message["postback"]["payload"]=="START":
                            welcome_message="Welcome! I am Black Adam, your personal Music Butler! To record your music click on the mic button and I'll tell you whatever I know!"
                            post_message(recipient_id,welcome_message)
                            return HttpResponse(status=200)
                    except:
                        print "Continue"


                    try:
                        if message["message"]["text"]!=None:
                            err_message = "I can help you out with identifying music for now. Click the record button to witness me!"
                            post_message(recipient_id,err_message)
                            return HttpResponse(status=200)
                            break
                            break

                    except:
                        for attachment in message["message"]["attachments"]:
                            audio=attachment["payload"]["url"]
                            print audio
                            wget.download(audio,out="music.mp3")
                            return_object=audio_file("music.mp3")
                            os.remove("music.mp3")
                            return_object=json.loads(return_object.decode('utf-8'))


                            try:
                                for t in return_object["metadata"]["music"]:
                                    song=t["title"]
                                    songt="Hey, I've identified your song, the song is called,"
                                    post_message(recipient_id,songt)
                                    post_message(recipient_id,song)

                                    post_message(recipient_id,"The artists are,")
                                    for a in t["artists"]:
                                        artist=a["name"]
                                        create_button(recipient_id,artist)
                                    post_message(recipient_id,"All done here, record another clip?")

                                    break
                            except:
                                post_message(recipient_id,"Sorry, my programming is limited!")
                                return HttpResponse(status=200)


                            return HttpResponse(return_object,status=200,content_type="application/json")




        except:
            return HttpResponse(status=200)





def post_message(recipient_id,message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_TOKEN
    response_msg = json.dumps({"recipient": {"id": recipient_id}, "message": {"text": message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())


def create_button(recipient_id,message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = json.dumps({"recipient": {"id": recipient_id}, "message": { "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":message,
        "buttons":[
          {
            "type":"web_url",
            "url":"https://www.google.co.in/#&q="+message,
            "title":"Click for more info",
            "webview_height_ratio":"compact"
          },
            {
                "type": "web_url",
                "url": "http://musicroamer.com/#/search?artist="+message,
                "title": "Similar artists and tracks",
                "webview_height_ratio": "tall"
            }
        ]}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())
