import discord
from discord.ext import commands
import praw
import requests
from bs4 import BeautifulSoup

# Replace the placeholders with your actual Discord bot token, Reddit client ID, and client secret
DISCORD_BOT_TOKEN = 'MTA5NTAzMTcxNzY5OTUzODk4NA.GcrzZQ.FeB9Kxl9NMa0RxVme0SdsH8mlD5KpMeS6UrD5M'
REDDIT_CLIENT_ID = 'jl64wYpAxB8pN3NbpdS2zA'
REDDIT_CLIENT_SECRET = 'mTqljIKqoKvlNq-1fNGHiFdWcQR4XA'

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

