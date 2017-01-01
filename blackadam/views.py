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
                            welcome_message="Hello! I'm Black Adam, your personal Music Butler! Record music you want to identify by clicking on the mic button!"

                            post_message(recipient_id,welcome_message)
                            post_message(recipient_id,"P.S: I may not be able to figure out if you hum, I've just learnt to identify original music.")
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
                                    songt="Hey, I've identified your song, it's"
                                    post_message(recipient_id,songt)
                                    post_message(recipient_id,song)

                                    post_message(recipient_id,"And the artists are,")
                                    for a in t["artists"]:
                                        artist=a["name"]
                                        create_button(recipient_id,artist)
                                    post_message(recipient_id,"All done here, record another clip?")
                                    quick_reply(recipient_id,song,artist)
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
                "url": "https://www.music-map.com/"+message+".html",
                "title": "Find Similar",
                "webview_height_ratio": "tall"
            }
        ]}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())


def quick_reply(recipient_id,song,artist):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_TOKEN
    response_msg = json.dumps({
  "recipient":{
    "id":recipient_id
  },
  "message":{
    "text":"I can pull up the song on these platforms,",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"YouTube",
        "payload":{
            "url":"https://www.youtube.com/results?search_query="+song+"+"+artist
        }
      },
      {
        "content_type":"text",
        "title":"Lyrics",
        "payload":{
            "url":"http://www.lyrics.com/lyrics/"+song+"%20"+artist
        }

      }
    ]
  }
})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())