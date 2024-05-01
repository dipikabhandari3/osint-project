# Import Libraries Needed

import pandas as pd
import requests
import tkinter as tk
from tkinter import *
import instaloader
import praw
from ntscraper import Nitter
import csv

# Function to search Twitter
def search_twt():
    # Get the query from the entry field
    qry = twtentrybox.get().strip()
    lim = 100

    scraper = Nitter(log_level=1)
    tweets = []
    # Search for tweets
    search = scraper.get_tweets(qry, mode = 'user', number = lim)

    for tweet in search["tweets"]: 
        tweets.append([tweet['date'], tweet['user']['username'], tweet['user']['name'], tweet['text'], tweet['stats']['comments'], tweet['stats']['retweets'], tweet['stats']['likes']])

    # Create a DataFrame from the collected tweets and save it to a CSV file
    frm = pd.DataFrame(tweets, columns=["Date", "Username", "Displayname", "Tweet Content", "Amount of Replies", "Retweet Count", "Like Count"]) 
    frm.to_csv(f"{qry}.csv")


# Function to search Instagram
def search_inst():
    # Get the username from the entry field
    uname = username_entry.get()
    # Initialize Instaloader
    init = instaloader.Instaloader()
    # # Get profile information

    prof = instaloader.Profile.from_username(init.context, uname)

    # Extract profile information
    profile_username = prof.username
    profile_id = prof.userid
    profile_name = prof.full_name
    follower_count = prof.followers
    following_count = prof.followees
    count_posts = prof.mediacount
    is_private = prof.is_private
    verified_account = prof.is_verified
    bio = prof.biography
    profile_pic_url = prof.profile_pic_url
    external_url = prof.external_url

    # Write profile information to a text file
    curFile = open(f"{uname}.txt", "w")
    curFile.write(f"Profile Username: {profile_username}\n")
    curFile.write(f"{uname} ID: {profile_id}\n")
    curFile.write(f"{uname} Full Name: {profile_name}\n")
    curFile.write(f"{uname} Follower Count: {follower_count}\n")
    curFile.write(f"{uname} Following: {following_count}\n")
    curFile.write(f"{uname} Number of Posts: {count_posts}\n")
    curFile.write(f"Is {uname} Private: {verified_account}\n")
    curFile.write(f"{uname} Bio: {bio}\n")
    curFile.write(f"{uname} Profile Pic URL: {profile_pic_url}\n")
    curFile.write(f"{uname} Associated External URL: {external_url}\n")
    curFile.close()
    
# Function to search Reddit
def search_reddit():
    # Authenticate with Reddit API
    reddit = praw.Reddit(client_id='bf43fkuhk-GEQTJgOS4W0A', client_secret='aoLJY8jzKgGtiPstJxx7w2d_d7gEog', user_agent='pythonpraw')
    subreddit_name = subreddit_name_entry.get()
    subreddit = reddit.subreddit(subreddit_name)
 
    # Write subreddit information to a text file
    curFile = open(f"{subreddit_name}.txt", "w", encoding='utf-8')
    curFile.write(f"Subreddit name: {subreddit.display_name}\n")
    curFile.write(f"Subreddit title: {subreddit.title}\n")
    curFile.write(f"Subreddit description: {subreddit.description}\n")
    curFile.write(f"Subreddit URL: {subreddit.url}\n")
    curFile.write(f"Subreddit subscribers: {subreddit.subscribers}\n")
    curFile.write("\nLast 10 comments:\n")

    # Write last 10 comments in the subreddit to the file
    for comment in subreddit.comments(limit=20):
        curFile.write(f"{comment.author.name}: {comment.body}\n")

    curFile.close()

# Function to get weather information
def get_weather(event=None):
    api_key = "cf573050f7c9ac49a7b694889408918e"
    root_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city_name_entry.get()
    url = f"{root_url}appid={api_key}&q={city_name}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        temperature = data['main']['temp']
        temperature_fahrenheit = round(((temperature - 273.15) * 9/5) + 32, 2)
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        wind = data['wind']['speed']


        # Write weather information to a text file
        with open(f'{city_name}-weather.txt', 'w') as curFile:
            curFile.write(f"City Name: {city_name}\n")
            curFile.write(f"Weather Condition: {description}\n")
            curFile.write(f"Temperature: {temperature_fahrenheit} Fahrenheit\n")
            curFile.write(f"Humidity: {humidity} %\n")
            curFile.write(f"Wind Speed: {wind} mph\n")
            curFile.write(f"Pressure: {pressure} inHg")
        
# Create the main window
COLOR_PRIMARY = "#2a9d8f"
COLOR_SECONDARY = "#264653"
COLOR_LIGHT_BACKGROUND = "#e9c46a"
COLOR_LIGHT_TEXT = "#f4a261"
COLOR_BUTTON_ACTIVE = "#e76f51"
FONT = "Arial"
FONT_SIZE = 12
FONT_BOLD = "bold"

window = tk.Tk()
window.title("OSINT")
window.configure(bg=COLOR_SECONDARY)
window.geometry("650x400")


# Styling Functions
def style_button(button):
    button.config(
        font=(FONT, FONT_SIZE, FONT_BOLD),
        bg=COLOR_PRIMARY,
        fg=COLOR_LIGHT_TEXT,
        activebackground=COLOR_BUTTON_ACTIVE,
        bd=0,
        padx=10,
        pady=5
    )
    button.pack(padx=10, pady=10, fill=tk.BOTH)

def style_label(label):
    label.config(
        font=(FONT, FONT_SIZE, FONT_BOLD),
        bg=COLOR_SECONDARY,
        fg=COLOR_LIGHT_BACKGROUND
    )
    label.pack(padx=10, pady=10, fill=tk.BOTH)

def style_entry(entry):
    entry.config(
        font=(FONT, FONT_SIZE),
        bg="white",
        fg="black",
        insertbackground="black",  # Cursor color
        bd=0,
        relief=tk.FLAT
    )
    entry.pack(padx=10, pady=5, fill=tk.BOTH)

topFrame = Frame(window)
topFrame.pack(side=BOTTOM)

bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM)

topleftFrame = Frame(topFrame)
topleftFrame.pack(side= LEFT)

toprightFrame = Frame(topFrame)
toprightFrame.pack(side=LEFT)

bottomleftFrame = Frame(bottomFrame)
bottomleftFrame.pack(side=LEFT)

bottomrightFrame = Frame(bottomFrame)
bottomrightFrame.pack(side=LEFT)

# Labels and Entry fields for Twitter search
opening = tk.Label(window, text="Please enter data name to be collected", bg="azure", font=("Times New Roman", 15, "bold"))
opening.pack(ipadx=5, ipady=5, fill=tk.X)

twtlabel = tk.Label(topleftFrame, text="Twitter name:", font=("Times New Roman", 15, "bold"))
twtlabel.pack(ipadx=5, ipady=5,side=TOP)
twtentrybox = tk.Entry(topleftFrame)
twtentrybox.pack(ipadx=5, ipady=5)

search_twt_btn = tk.Button(topleftFrame, text="Retrieve Twitter Data", command=search_twt, font=("Times New Roman", 15, "bold"))
search_twt_btn.pack(side=BOTTOM)

# Labels and Entry fields for Instagram search
instalabel = tk.Label(toprightFrame, text="Instagram Username:", font=("Times New Roman", 15, "bold"))
instalabel.pack(ipadx=5, ipady=5,side=TOP)
username_entry = tk.Entry(toprightFrame)
username_entry.pack(ipadx=5, ipady=5)
retrieveinstadata = tk.Button(toprightFrame, text="Retrieve Instagram Data", command=search_inst,  font=("Times New Roman", 15, "bold"))
retrieveinstadata.pack(side=BOTTOM)

# Labels and Entry fields for Reddit search
subreddit_name_label = tk.Label(bottomleftFrame, text="Sub-Reddit Name:", font=("Times New Roman", 15, "bold"))
subreddit_name_label.pack(ipadx=5, ipady=5,side=TOP)
subreddit_name_entry = tk.Entry(bottomleftFrame)
subreddit_name_entry.pack(ipadx=5, ipady=5)
scrape_reddit_btn = tk.Button(bottomleftFrame, text="Retrieve Sub-Reddit Data", command=search_reddit, font=("Times New Roman", 15, "bold"))
scrape_reddit_btn.pack(side=BOTTOM)

# Labels and Entry fields for weather search
city_name_label = tk.Label(bottomrightFrame, text="City Name:", font=("Times New Roman", 15, "bold"))
city_name_label.pack(ipadx=5, ipady=5,side=TOP)
city_name_entry = tk.Entry(bottomrightFrame)
city_name_entry.pack(ipadx=5, ipady=5)
scrape_city_btn = tk.Button(bottomrightFrame, text="Retrieve weather Data", command=get_weather,font=("Times New Roman", 15, "bold"))
scrape_city_btn.pack(side=BOTTOM)


# Apply styles to existing widgets using the defined functions
opening.configure(font=(FONT, FONT_SIZE, FONT_BOLD), bg=COLOR_PRIMARY, fg=COLOR_LIGHT_TEXT)
style_label(twtlabel)
style_label(instalabel)
style_label(subreddit_name_label)
style_label(city_name_label)

style_entry(twtentrybox)
style_entry(username_entry)
style_entry(subreddit_name_entry)
style_entry(city_name_entry)

style_button(search_twt_btn)
style_button(retrieveinstadata)
style_button(scrape_reddit_btn)
style_button(scrape_city_btn)

for frame in [topleftFrame, toprightFrame, bottomleftFrame, bottomrightFrame]:
    frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)


# Start the tkinter event loop
window.mainloop()
