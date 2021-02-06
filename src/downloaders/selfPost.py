from src.utils import printToFile as print
import io
import os
from pathlib import Path

from src.errors import FileAlreadyExistsError, TypeInSkip
from src.utils import GLOBAL
from src.utils import printToFile as print

VanillaPrint = print


class SelfPost:
    def __init__(self, directory, post):
        if "self" in GLOBAL.arguments.skip:
            raise TypeInSkip

        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = GLOBAL.config['filename'].format(**post)

        file_dir = directory / (filename + ".md")
        print(file_dir)
        print(filename + ".md")

        if Path.is_file(file_dir):
            raise FileAlreadyExistsError

        try:
            self.writeToFile(file_dir, post)
        except FileNotFoundError:
            file_dir = post['POSTID'] + ".md"
            file_dir = directory / file_dir

            self.writeToFile(file_dir, post)

    @staticmethod
    def writeToFile(directory, post):
        """Self posts are formatted here"""
        content = ("## ["
                   + post["TITLE"]
                   + "]("
                   + post["CONTENTURL"]
                   + ")\n"
                   + post["CONTENT"]
                   + "\n\n---\n\n"
                   + "submitted to [r/"
                   + post["SUBREDDIT"]
                   + "](https://www.reddit.com/r/"
                   + post["SUBREDDIT"]
                   + ") by [u/"
                   + post["REDDITOR"]
                   + "](https://www.reddit.com/user/"
                   + post["REDDITOR"]
                   + ")")

        with io.open(directory, "w", encoding="utf-8") as FILE:
            VanillaPrint(content, file=FILE)
        print("Downloaded")
