import discord
from discord.ext import commands
import cogs.cmds as biggay
import importlib

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, page: int=None):
        """This does stuff!"""

        #Your code will go here
        if not page:
            page = 1
        embed = self.build_embed(page)
        msg = await self.bot.say("**Commands List**", embed=embed)
        await self.bot.add_reaction(msg, "⬅")
        await self.bot.add_reaction(msg, '➡')
        while True:
            res = await self.bot.wait_for_reaction(['⬅', '➡'], user=ctx.message.author, message=msg, timeout=15)
            try:
                if res.reaction.emoji == "➡":
                    if page == 6:
                        page = 1
                        embed = self.build_embed(page)
                        await self.bot.edit_message(msg, embed=embed)
                        await self.bot.remove_reaction(msg, "➡", ctx.message.author)
                        continue
                    else:
                        page = page + 1
                        embed = self.build_embed(page)
                        await self.bot.edit_message(msg, embed=embed)
                        await self.bot.remove_reaction(msg, "➡", ctx.message.author)
                        continue
                if res.reaction.emoji == "⬅":
                    if page == 1:
                        page = 6
                        embed = self.build_embed(page)
                        await self.bot.edit_message(msg, embed=embed)
                        await self.bot.remove_reaction(msg, "⬅", ctx.message.author)
                        continue
                    else:
                        page = page - 1
                        embed = self.build_embed(page)
                        await self.bot.edit_message(msg, embed=embed)
                        await self.bot.remove_reaction(msg, "⬅", ctx.message.author)
                        continue
                else:
                    continue
            except AttributeError:
                await self.bot.remove_reaction(msg, "➡", ctx.message.server.me)
                await self.bot.remove_reaction(msg, "⬅", ctx.message.server.me)
                break


    def build_embed(self, page):
        if page == 1:
            return self.build_embed_1()
        if page == 2:
            return self.build_embed_2()
        if page == 3:
            return self.build_embed_3()
        if page == 4:
            return self.build_embed_4()
        if page == 5:
            return self.build_embed_5()
        if page == 6:
            return self.build_embed_6()


    def build_embed_1(self):
        embed = discord.Embed(title=biggay.misctitle, description=biggay.misc, color=0x5964e1)
        embed.set_footer(text="Page No. 1")
        return embed

    def build_embed_2(self):
        embed = discord.Embed(title=biggay.modtitle, description=biggay.mod, color=0x5964e1)
        embed.set_footer(text="Page No. 2")
        return embed

    def build_embed_3(self):
        embed = discord.Embed(title=biggay.managetitle, description=biggay.manage, color=0x5964e1)
        embed.set_footer(text="Page No. 3")
        return embed

    def build_embed_4(self):
        embed = discord.Embed(title=biggay.portaltitle, description=biggay.portal, color=0x5964e1)
        embed.set_footer(text="Page No. 4")
        return embed

    def build_embed_5(self):
        embed = discord.Embed(title=biggay.tagtitle, description=biggay.tags, color=0x5964e1)
        embed.set_footer(text="Page No. 5")
        return embed

    def build_embed_6(self):
        embed = discord.Embed(title=biggay.utiltitle, description=biggay.util, color=0x5964e1)
        embed.set_footer(text="Page No. 6")
        return embed

    @commands.command()
    async def reloadhelp(self):
        importlib.reload(biggay)
        await self.bot.say("Help Message(s) Reloaded.")


def setup(bot):
    bot.add_cog(Mycog(bot))
