from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import wget
import requests
import os
import time


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
                            welcome_message="Hello! I'm Black Adam, your personal Music Butler! Record music you want to ID by clicking on the mic button!"

                            post_message(recipient_id,welcome_message)
                            post_message(recipient_id,"P.S: I may not be able to figure out if you hum, I've just learnt to identify original music. Type out help if you're not sure what I can do")
                            return HttpResponse(status=200)
                    except:
                        print "Continue"


                    try:
                        if message["message"]["text"]!=None:

                            if message["message"]["text"]=="help" or message["message"]["text"]=="HELP" or message["message"]["text"]=="Help":
                                post_message(recipient_id,"I work just like Shazam or SoundHound. Record the original audio using the microphone button and I'll find the title, artists and associated information.")
                                return HttpResponse(status=200)
                                break
                                break
                            if message["message"]["text"]=="troubleshoot" or message["message"]["text"]=="TROUBLESHOOT" or message["message"]["text"]=="Troubleshoot":
                                troubleshoot="Let's work together shall we? If you've hummed or not recorded the original audio, I can't help you out yet. Sorry"

                                post_message(recipient_id,troubleshoot)
                                post_message(recipient_id,"If not, try recording atleast 15 seconds of the audio. If it still doesn't work, I'll get back to you with the audio source in a bit.(I'll try asking around)")
                                return HttpResponse(status=200)
                                break
                                break


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

                            print return_object
                            try:
                                for t in return_object["metadata"]["music"]:
                                    print "Music activated"
                                    song=t["title"]

                                    songt="Hey, I've identified your song, it's"
                                    post_message(recipient_id,songt)
                                    post_message(recipient_id,song)



                                    genre="Pop"
                                    if "genres" in t:
                                        for g in t["genres"]:
                                            genre=g["name"]
                                            genre=genre+"+"

                                    post_message(recipient_id,"And the artists are,")
                                    for a in t["artists"]:
                                        artist=a["name"]
                                        create_button(recipient_id,artist)

                                    # Check for associated youtube ID
                                    if "youtube" in t["external_metadata"]:
                                        youtube="https://www.youtube.com/watch?v="+str(t["external_metadata"]["youtube"]["vid"])
                                    else:
                                        youtube="https://www.youtube.com/results?search_query="+song+"+"+artist

                                    quick_reply(recipient_id,song,artist,youtube,genre)
                                    time.sleep(8)
                                    post_message(recipient_id, "All done here, record another clip?")

                                    break
                            except:
                                try:
                                    for t in return_object["metadata"]["humming"]:
                                        print "Humming activated"
                                        song = t["title"]

                                        songt = "Hey, I've identified your song, it's"
                                        post_message(recipient_id, songt)
                                        post_message(recipient_id, song)

                                        genre = "Pop"
                                        if "genres" in t:
                                            for g in t["genres"]:
                                                genre = g["name"]
                                                genre = genre + "+"

                                        post_message(recipient_id, "And the artists are,")
                                        for a in t["artists"]:
                                            artist = a["name"]
                                            create_button(recipient_id, artist)

                                        # Check for associated youtube ID
                                        if "youtube" in t["external_metadata"]:
                                            youtube = "https://www.youtube.com/watch?v=" + str(
                                                t["external_metadata"]["youtube"]["vid"])
                                        else:
                                            youtube = "https://www.youtube.com/results?search_query=" + song + "+" + artist

                                        quick_reply(recipient_id, song, artist, youtube, genre)
                                        time.sleep(8)
                                        post_message(recipient_id, "All done here, record another clip?")

                                        break

                                except:

                                    post_message(recipient_id,"Seems like we've got a mutual communication issue")
                                    quick(recipient_id)
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


def quick_reply(recipient_id,song,artist,youtube,genre):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_TOKEN
    response_msg = json.dumps({
        "recipient": {
            "id":recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "YouTube",
                            "image_url": "https://www.seeklogo.net/wp-content/uploads/2016/06/YouTube-icon.png",
                            "subtitle": "Watch your music video on YouTube",
                            "default_action": {
                                "type": "web_url",
                                "url":youtube,
                                "webview_height_ratio": "tall",
                            }

                        },
                        {
                            "title": "Music on SoundCloud",
                            "image_url": "https://www.competitionpolicyinternational.com/wp-content/uploads/2016/09/SoundCloud-Logo.jpg",
                            "subtitle": "Check out the song and various mixes on SoundCloud",
                            "default_action": {
                                "type": "web_url",
                                "url":"https://soundcloud.com/search?q="+song+"%20"+artist ,
                                "webview_height_ratio": "tall"
                            }

                        },
                        {
                            "title": "8 Track it",
                            "image_url": "http://techtalks.ideacellular.com/wp-content/uploads/2016/10/22.png",
                            "subtitle": "Listen to music from Similar Genres on 8tracks",
                            "default_action": {
                                "type": "web_url",
                                "url": "http://8tracks.com/explore/"+genre,
                                "webview_height_ratio": "tall",
                            }

                        }


                    ]
                }
            }
        }
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())

def quick(recipient_id):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
    response_msg = json.dumps({
  "recipient":{
    "id":recipient_id
  },
  "message":{
    "text":"My progamming is limited. But you're not. Pick any of the below to try again",
    "quick_replies":[
      {
        "content_type":"text",
        "title":"Help",
        "payload":"Help"
      },
      {
        "content_type":"text",
        "title":"Troubleshoot",
        "payload":"Troubleshoot"
      }
    ]
  }
})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(status.json())