from discord.ext import commands
from cogs.utils import permissions
import subprocess


class Bird:
    """Do things with BIRD"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def route(self, subnet):
        """Enter an IP or subnet to lookup in BIRD"""
        cmd = subprocess.check_output(["birdc", "show", "route", "for", str(subnet)])
        out = f"```\n{cmd}\n```"
        await self.bot.say(out)

    @commands.command()
    async def status(self):
        """Check the status of BIRD"""
        cmd = subprocess.check_output(["birdc", "show", "proto"])
        out = f"```\n{cmd}\n```"
        await self.bot.say(out)

    @commands.command()
    async def statusinfo(self, astable):
        """Enter an IP or subnet to lookup in BIRD"""
        cmd = subprocess.check_output(["birdc", "show", "proto", str(astable)])
        out = f"```\n{cmd}\n```"
        await self.bot.say(out)

    @commands.command()
    @commands.check(permissions.admincheck)
    async def birdrestart(self, astable):
        """Enter an IP or subnet to restart in BIRD"""
        cmd = subprocess.check_output(["birdc", "restart", str(astable)])
        out = f"```\n{cmd}\n```"
        await self.bot.say(out)


def setup(bot):
    bot.add_cog(Bird(bot))