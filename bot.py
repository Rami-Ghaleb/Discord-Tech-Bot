import discord
from discord.ext import commands
import praw
import requests
from bs4 import BeautifulSoup

#replace placeholders with your credentials
DISCORD_BOT_TOKEN = "your_discord_bot_token_here"
REDDIT_CLIENT_ID = "your_reddit_client_id_here"
REDDIT_SECRET = "your_reddit_client_secret_here"


# Define the intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Discord bot setup
bot = commands.Bot(command_prefix='!', intents=intents)

# Reddit API setup
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent='discord_bot'
)

@bot.command()
async def latest(ctx, count=5):
    # Get latest posts from the r/netsec subreddit
    subreddit = reddit.subreddit('netsec')
    latest_posts = [f"**{post.title}**: {post.url}" for post in subreddit.new(limit=count)]

    # Scrape data from The Hacker News website
    url = 'https://thehackernews.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='post', limit=count)

    # Extract titles and URLs
    latest_articles = [f"**{article.h2.text.strip()}**: {article.a['href']}" for article in articles]

        # Send the data to Discord
    await ctx.send("Latest Cyber Attacks and Tech Innovations:")

    await ctx.send("\n**r/netsec Updates:**")
    for post in latest_posts:
        await ctx.send(post)

    await ctx.send("\n**The Hacker News Updates:**")
    for article in latest_articles:
        await ctx.send(article)

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

