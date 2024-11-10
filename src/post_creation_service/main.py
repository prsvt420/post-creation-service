import asyncio

from src.post_creation_service.dataclasses import PostData
from src.post_creation_service.services import RedditService, XService


async def main():
    reddit_service: RedditService = RedditService()
    x_service: XService = XService()

    posts = [
        {
            'subreddit': 'test',
            'title': 'test',
            'text': 'test text',
            'image_path': '../../static/img/test.jpg',
        },
    ]

    reddit_service_tasks = [reddit_service.create_post(PostData(**post)) for post in posts]
    x_service_tasks = [x_service.create_post(PostData(**post)) for post in posts]
    await asyncio.gather(*reddit_service_tasks, *x_service_tasks)

if __name__ == '__main__':
    asyncio.run(main())
