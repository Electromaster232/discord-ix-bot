from discord.ext import commands
from cogs.utils import permissions
from cogs.utils import chat_formatting
import subprocess

class Bird:
    """Do things with BIRD"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def route(self, subnet):
        """Enter an IP or subnet to lookup in BIRD"""
        cmd = subprocess.check_output(["birdc", "show", "route", "for", str(subnet)])
        out = "```\n{0}\n```".format(cmd)
        for page in chat_formatting.pagify(out, ['\n', ' '], shorten_by=12):
            await self.bot.say(page)

    @commands.command()
    async def status(self):
        """Check the status of BIRD"""
        cmd = subprocess.check_output(["birdc", "show", "proto"])
        out = "```\n{0}\n```".format(cmd)
        for page in chat_formatting.pagify(out, ['\n', ' '], shorten_by=12):
            await self.bot.say(page)

    @commands.command()
    async def statusinfo(self, astable):
        """Enter an IP or subnet to lookup in BIRD"""
        cmd = subprocess.check_output(["birdc", "show", "proto", str(astable)])
        out = "```\n{0}\n```".format(cmd)
        for page in chat_formatting.pagify(out, ['\n', ' '], shorten_by=12):
            await self.bot.say(page)

    @commands.command()
    @commands.check(permissions.admincheck)
    async def birdrestart(self, astable):
        """Enter an IP or subnet to restart in BIRD"""
        cmd = subprocess.check_output(["birdc", "restart", str(astable)])
        out = "```\n{0}\n```".format(cmd)
        for page in chat_formatting.pagify(out, ['\n', ' '], shorten_by=12):
            await self.bot.say(page)


def setup(bot):
    bot.add_cog(Bird(bot))
