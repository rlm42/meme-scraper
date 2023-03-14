import reddit_image_extractor_module2
import time as _time
import gunicorn

def main():
    reddit_image_extractor_module2.run_reddit_downloader()

def run():
    while True:
        main()
        _time.sleep(86400)  ## in seconds (this is 24 hours)

if __name__ == "__main__":
    run()