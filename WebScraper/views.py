from django.shortcuts import render
import snscrape.modules.twitter as sntwitter
import praw
import pymongo
import csv
from django.http import HttpResponse

def HomePage(request):
    return render(request, "HTML/HomePage.html")

def Results(request):
    topic = request.POST['Topic']
    web = request.POST['WebChoose']
    number_of_posts = int(request.POST['posts_number'])

    posts = []
    res = []
    if web == 'twitter':
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(topic).get_items()):
            if i>number_of_posts:
                break
            res.append({
                'topic': topic,
                'source_site': 'Twitter',
                'post': tweet.content
            })
            posts.append(tweet.content)

    elif web == 'reddit':
        reddit = praw.Reddit(client_id='PowdByc93qmVcWvbiF_0-g',
                            client_secret='17LxqiO3FgDliSnCvzvqr5pSphJKpg',
                            user_agent='scrap')

        for i, submission in enumerate(reddit.subreddit('all').search(topic)):
            if i > number_of_posts:
                break
            res.append({
                'topic': topic,
                'source_site': 'Reddit',
                'post': submission.title
            })
            posts.append(submission.title)

    # Save data in MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Social_Media"]
    collection = db["posts"]
    collection.insert_many(res)

    return render(request, "HTML/Results.html", {'res':posts , 'topic': topic, 'web':web})

def Archive(request):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Social_Media"]
    collection = db["posts"]
    posts = collection.find()
    return render(request, "HTML/Archive.html", {"data": posts})

def Csv(request):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Social_Media"]
    collection = db["posts"]
    posts = collection.find()

    # Create a CSV response object
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'

    # Write the CSV data to the response
    writer = csv.writer(response)
    writer.writerow(['Source Site', 'Topic', 'Post'])
    for post in posts:
        writer.writerow([post['source_site'], post['topic'], post['post']])

    return response