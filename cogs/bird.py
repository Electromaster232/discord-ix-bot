from discord.ext import commands
import os

class Bird:
    """Do things with BIRD"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def route(self, subnet):
        """Enter an IP or subnet to lookup"""




def setup(bot):
    bot.add_cog(Bird(bot))
