import reddit_image_extractor_module2
import time as _time
from flask import Flask, request, render_template

app = Flask(__name__)


def main():
    reddit_image_extractor_module2.run_reddit_downloader()


main()
_time.sleep(86400)  # in seconds (this is 24 hours)

# def run():
#     while True:
#         main()
#         _time.sleep(86400)  ## in seconds (this is 24 hours)


if __name__ == "__main__":
    # run()
    app.run(debug=True)
