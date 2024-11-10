from typing import Optional

import aiohttp
import asyncpraw
import tweepy
from asyncpraw.models import InlineImage
from tweepy import asynchronous as asynctweepy

from src.post_creation_service import settings
from src.post_creation_service.dataclasses import PostData


class RedditService:
    @staticmethod
    async def create_connection() -> asyncpraw.reddit.Reddit:
        """Create connection to Reddit service"""

        return asyncpraw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            redirect_uri=settings.REDDIT_REDIRECT_URI,
            user_agent=settings.REDDIT_USER_AGENT,
            username=settings.REDDIT_USERNAME,
            password=settings.REDDIT_PASSWORD
        )

    async def create_post(self, post_data: PostData) -> None:
        """Create post in Reddit service"""

        subreddit: str = post_data.subreddit
        title: str = post_data.title
        selftext: str = post_data.text
        image_path: str = post_data.image_path

        inline_media = await self._prepare_inline_media(image_path)

        async with await self.create_connection() as reddit_client:
            subreddit: asyncpraw.reddit.Subreddit = await reddit_client.subreddit(subreddit)
            await subreddit.submit(title=title, selftext=selftext, inline_media=inline_media)

    @staticmethod
    async def _prepare_inline_media(image_path: str) -> dict:
        """Prepare inline media for submission"""

        if image_path:
            inline_image = InlineImage(path=image_path)
            return {'image': inline_image}
        return {}


class XService:
    @staticmethod
    async def _create_v2_connection() -> asynctweepy.AsyncClient:
        """Create V2 connection to X service"""

        return asynctweepy.client.AsyncClient(
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET_KEY,
            bearer_token=settings.X_BEARER_TOKEN,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET,
        )

    @staticmethod
    async def _create_v1_connection() -> tweepy.API:
        """Create V1 connection to X service"""

        auth: tweepy.OAuth1UserHandler = tweepy.OAuth1UserHandler(
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET_KEY,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET,
        )
        return tweepy.API(auth)

    async def create_post(self, post_data: PostData) -> None:
        """Create post in X service"""

        title: str = post_data.title
        selftext: str = post_data.text
        image_path: str = post_data.image_path

        media_id: Optional[str] = None

        if image_path:
            media_id = await self._upload_media(image_path)

        await self._send_tweet(title, selftext, media_id)

    async def _upload_media(self, image_path: str) -> str:
        """Upload media and return media ID"""

        x_client_v1: tweepy.API = await self._create_v1_connection()
        media: tweepy.Media = x_client_v1.media_upload(image_path)
        return media.media_id

    async def _send_tweet(self, title: str, selftext: str, media_id: str = None) -> None:
        """Send a tweet with optional media"""

        x_client_v2: asynctweepy.AsyncClient = await self._create_v2_connection()

        async with aiohttp.ClientSession() as session:
            x_client_v2.session = session
            tweet_text: str = f"{title}\n\n{selftext}"

            if media_id:
                await x_client_v2.create_tweet(text=tweet_text, media_ids=[media_id])
            else:
                await x_client_v2.create_tweet(text=tweet_text)
