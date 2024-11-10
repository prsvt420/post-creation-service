from typing import Optional

import aiohttp
import asyncpraw
import tweepy
from asyncpraw.models import InlineImage
from tweepy import asynchronous as asynctweepy

from src.post_creation_service import settings
from src.post_creation_service.dataclasses import PostData


class RedditService:
    def __init__(self) -> None:
        self.client: Optional[asyncpraw.reddit.Reddit] = None

    async def connect(self) -> None:
        """Create connection to Reddit service"""

        self.client: asyncpraw.reddit.Reddit = asyncpraw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            redirect_uri=settings.REDDIT_REDIRECT_URI,
            user_agent=settings.REDDIT_USER_AGENT,
            username=settings.REDDIT_USERNAME,
            password=settings.REDDIT_PASSWORD
        )

    async def disconnect(self) -> None:
        """Disconnect from Reddit service"""

        await self.client.close()

    async def create_post(self, post_data: PostData) -> None:
        """Create post in Reddit service"""

        if not self.client:
            await self.connect()

        subreddit: asyncpraw.reddit.Subreddit = await self.client.subreddit(post_data.subreddit)
        inline_media = await self._prepare_inline_media(post_data.image_path)

        await subreddit.submit(
            title=post_data.title,
            selftext=post_data.text,
            inline_media=inline_media,
        )

        await self.disconnect()

    @staticmethod
    async def _prepare_inline_media(image_path: str) -> dict:
        """Prepare inline media for submission"""

        if image_path:
            inline_image: InlineImage = InlineImage(path=image_path)
            return {'image': inline_image}
        return {}


class XService:
    def __init__(self) -> None:
        self.client_v1: Optional[tweepy.API] = None
        self.client_v2: Optional[asynctweepy.AsyncClient] = None

    async def connect(self) -> None:
        """Create connections to X service"""
        self.client_v1: tweepy.API = tweepy.API(tweepy.OAuth1UserHandler(
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET_KEY,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET,
        ))
        self.client_v2: asynctweepy.AsyncClient = asynctweepy.AsyncClient(
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET_KEY,
            bearer_token=settings.X_BEARER_TOKEN,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET,
        )

    async def create_post(self, post_data: PostData) -> None:
        """Create post in X service"""

        if not self.client_v1 or not self.client_v2:
            await self.connect()

        title: str = post_data.title
        selftext: str = post_data.text
        image_path: str = post_data.image_path

        media_id: Optional[str] = None

        if image_path:
            media_id = await self._upload_media(image_path)

        await self._send_tweet(title, selftext, media_id)

    async def _upload_media(self, image_path: str) -> str:
        """Upload media and return media ID"""

        media: tweepy.Media = self.client_v1.media_upload(image_path)
        return media.media_id

    async def _send_tweet(self, title: str, selftext: str, media_id: str = None) -> None:
        """Send a tweet with optional media"""

        async with aiohttp.ClientSession() as session:
            self.client_v2.session = session
            tweet_text: str = f"{title}\n\n{selftext}"

            if media_id:
                await self.client_v2.create_tweet(text=tweet_text, media_ids=[media_id])
            else:
                await self.client_v2.create_tweet(text=tweet_text)
