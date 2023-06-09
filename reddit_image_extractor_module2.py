import time
import http_module
import menu_module
import url_to_file_module
import config
import time as _time

import tweepy as tp

meme_ids = []

def gen_reddit_url(subreddit, sort_type, sort_arg, after):
    if sort_type != "":
        sort_type = "/" + sort_type
    if sort_arg != "":
        sort_arg = "&" + sort_arg
    url = "https://www.reddit.com/r/" + subreddit + sort_type + "/.json?limit=100" + sort_arg + "&after=" + after
    return url

def extract_reddit_image_url(json_file):
    ret = {}
    posts = json_file["data"]["children"]
    for element in posts:
        url = element["data"]["url"]
        title = element["data"]["title"]
        asciistr = title.encode("ascii", errors="ignore").decode()
        unclean = str(asciistr)
        clean_title = unclean.translate(str.maketrans(" ","_","/.\\?#:;*<>\"'|"))
        if (".jpg" in url or ".jpeg" in url or ".png" in url or ".gif" in url):
            if (not ".gifv" in url and not ".mp4" in url):
                ret[clean_title] = url
    return ret

def run_reddit_downloader():
    # menu_module.run_menu()
    if config.subreddit:
        for subreddit in config.subreddit:
            http_module.download_count = 0
            http_module.error_count = 0
            print("--------------------------------------------------")
            print("Starting downloads for: " + subreddit)
            print("--------------------------------------------------" + "\n")
            after = ""
            elapsed_time = 4
            total_dict = {}
            while http_module.download_count < config.down_limit and after != None:
                start_time = time.time()
                if elapsed_time < 4:
                    time.sleep(4)
                url = gen_reddit_url(subreddit, config.sort_type, config.sort_arg, after)
                json_file = http_module.get_json(url)
                img_dict = extract_reddit_image_url(json_file)
                http_module.download_img(img_dict, "reddit/" + subreddit, config.down_limit)
                after = json_file["data"]["after"]
                elapsed_time = time.time() - start_time
                total_dict.update(img_dict)
                # print (total_dict)
                # extension = list(total_dict.items())[0][1]
                # extension2 = extension.__str__()
                # extension3 = extension2[-1:-4:-1]
                # extension4 = extension3[::-1]

            url_to_file_module.write_dict(subreddit, "reddit/url/" + subreddit, total_dict)
            print("--------------------------------------------------")
            print("Done downloading " + subreddit + " Error Count: " + str(http_module.error_count))
            print("--------------------------------------------------" + "\n")

            # Bot logging in to Twitter.
            consumer_key = "Wjyy4qzaFbvtJBweeViuydH6o"
            consumer_secret = "J61Z3ZiUplDjRhNQSGFykUNaiuXxqvJvE6RjKfe0zqtARBXtuV"
            access_token = "82548025-C99p7amZmFGmzsZbZddTvqSPgFU4xBEXASN4PeGZy"
            access_secret = "AQaHCPAEk73T4gikqGJnpVfHPihNlh5g2WVruQkp0wxyI"

            auth = tp.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            api = tp.API(auth)
            print('Logged In')

            extension = list(total_dict.items())[0][1]
            extension2 = extension.__str__()
            extension3 = extension2[-1:-4:-1]
            extension4 = extension3[::-1]
            

            meme = api.media_upload('reddit/cryptocurrencymemes/' + next(iter(total_dict)).__str__() + '.' + extension4)
            meme_ids.append(meme.media_id)
            api.update_status(status="@coinfreeway Meme of the Day!", media_ids=meme_ids)
            print('Meme posted!')
            _time.sleep(86400)  # in seconds (this is 24 hours)



    else:
        print("no subreddit entered")
