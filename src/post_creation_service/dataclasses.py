from Lib.dataclasses import dataclass


@dataclass
class PostData:
    title: str
    text: str
    subreddit: str
    image_path: str
