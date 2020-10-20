import praw
import requests
import cv2
import numpy as np
import os
import pickle

from utils.create_token import create_token

# Create directory if it doesn't exist to save images
def create_folder(image_path):
    CHECK_FOLDER = os.path.isdir(image_path)
    # If folder doesn't exist, then create it.
    if not CHECK_FOLDER:
        os.makedirs(image_path)

# Path to save images
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "images/")
ignore_path = os.path.join(dir_path, "ignore_images/")
create_folder(image_path)

# Get token file to log into reddit.
# You must enter your....
# client_id - client secret - user_agent - username password
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
else:
    creds = create_token()
    pickle_out = open("token.pickle","wb")
    pickle.dump(creds, pickle_out)

reddit = praw.Reddit(client_id=creds['client_id'],
                    client_secret=creds['client_secret'],
                    user_agent=creds['user_agent'],
                    username=creds['username'],
                    password=creds['password'])


f_final = open("sub_list.csv", "r")
img_notfound = cv2.imread('imageNF.png')
for line in f_final:
    sub = line.strip()
    subreddit = reddit.subreddit(sub)

    print(f"Starting {sub}!")
    count = 0
    for submission in subreddit.new(limit=20):
        if "jpg" in submission.url.lower() or "png" in submission.url.lower():
            try:
                resp = requests.get(submission.url.lower(), stream=True).raw
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                # Could do transforms on images like resize!
                compare_image = cv2.resize(image,(224,224))

                # Get all images to ignore
                for (dirpath, dirnames, filenames) in os.walk(ignore_path):
                    ignore_paths = [os.path.join(dirpath, file) for file in filenames]
                ignore_flag = False

                for ignore in ignore_paths:
                    ignore = cv2.imread(ignore)
                    difference = cv2.subtract(ignore, compare_image)
                    b, g, r = cv2.split(difference)
                    total_difference = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                    if total_difference == 0:
                        ignore_flag = True

                if not ignore_flag:
                    cv2.imwrite(f"{image_path}{sub}{count}.png", image)
                    count += 1
                    
            except Exception as e:
                print(f"Image failed. {submission.url.lower()}")
                print(e)
        