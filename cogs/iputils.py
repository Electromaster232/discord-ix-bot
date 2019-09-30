from discord.ext import commands
import subprocess
import json
import requests
import asyncio
from cogs.utils import chat_formatting


class IpUtils:
    """Get Info About IPs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping4(self, ip):
        """Ping an IPv4"""
        cmd = subprocess.check_output(["ping", "-4", "-c", "4", str(ip)])
        self.bot.say(chat_formatting.box(cmd.decode))

    @commands.command()
    async def ping6(self, ip):
        """Ping an IPv6"""
        cmd = subprocess.check_output(["ping", "-6", "-c", "4", str(ip)])
        self.bot.say(chat_formatting.box(cmd.decode))

    @commands.command()
    async def traceroute(self, v, ip):
        """Trace the route of an IP"""
        cmd = self.run("traceroute -{} {}".format(v, ip))
        for page in chat_formatting.pagify(cmd.decode(), ['\n', ' '], shorten_by=12):
            await self.bot.say(chat_formatting.box(page))

    @commands.command()
    async def iplookup(self, ip):
        """Get Info About an IP"""

        r = requests.get('http://ip-api.com/json/' + ip)
        # Make request to IP site
        response = r.text
        # We return a text version of the response instead of a dict so the parser understands it
        parsed_json = json.loads(response)
        # load the text output into the parser
    
        # Check for fail status
        if parsed_json['status'] == "fail":
            await self.bot.say("This operation failed, please check you made no mistakes and are not using an IP in the Private Range.")

        # and now folks for a long string of crap that converts everything into your response
        else:
            await self.bot.say("Country : " + parsed_json['country'])
            await self.bot.say("Region : " + parsed_json['regionName'])
            longfixed = str(parsed_json['lon'])
            # Longitude and Latitude are floats, lets fix that
            await self.bot.say("Longitude : " + longfixed)
            latfixed = str(parsed_json['lat'])
            await self.bot.say("Latitude : " + latfixed)
            await self.bot.say("City : " + parsed_json['city'])
            await self.bot.say("Zip Code : " + parsed_json['zip'])
            await self.bot.say("AS : " + parsed_json['as'])
            await self.bot.say("ISP : " + parsed_json['isp'])
   

    async def run(self, cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()
        return stdout.decode()

def setup(bot):
    bot.add_cog(IpUtils(bot))
