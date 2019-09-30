from discord.ext import commands
import discord
import logging
import asyncio
import traceback
import sys
import os
from config import Config


description = '''ElectroNIX Bot v1.0'''
# Set logging level
logging.basicConfig(level=logging.ERROR)

# this specifies what extensions to load when the bot starts up
startup_extensions = []




# Create the bot object
bot = commands.Bot(command_prefix=Config.botprefix, description=description)

def ownercheck(ctx):
    return ctx.message.author.id in Config.botowners


@bot.event
async def on_ready():
    print("© 2017 Electromaster232")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('READY')
    await bot.change_presence(status=discord.Status.online, game=discord.Game(name="ix!help"))



@commands.check(ownercheck)
@bot.command()
async def load(extension_name: str):
    """Loads an extension."""
    try:
        bot.load_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("The extension {} was loaded.".format(extension_name))

@commands.check(ownercheck)
@bot.command()
async def unload(extension_name: str):
    """Unloads an extension."""
    try:
        bot.unload_extension("cogs.{}".format(extension_name))
    except:
        await bot.say("There was an error")
    await bot.say("The extension {} was unloaded.".format(extension_name))

@commands.check(ownercheck)
@bot.command()
async def reload(extension_name: str):
    """Reloads an extension"""
    try:
        bot.unload_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as error:
        await bot.say("```py\n{}: {}\n```".format(type(error).__name__, str(error)))
        return
    await bot.say("The extension {} was unloaded.".format(extension_name))
    try:
        bot.load_extension("cogs.{}".format(extension_name))
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("The extension {} was loaded.".format(extension_name))


@bot.command()
async def ping():
    """Simple Ping Command"""
    em = discord.Embed(description="Pong!", color=discord.Color.blue())
    await bot.say(embed=em)


@bot.command()
async def owner():
    """Tells you who the bot owner is"""
    owner = str((await bot.application_info()).owner)
    em = discord.Embed(description=owner, color=discord.Color.green())
    await bot.say(embed=em)

@commands.check(ownercheck)
@bot.command()
async def loadall():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                bot.load_extension("cogs.{}".format(file)[0:-3])
            except discord.ClientException:
                pass
            except ImportError:
                pass
    await bot.say("All modules have been loaded.")

@commands.check(ownercheck)
@bot.command()
async def unloadall():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                bot.unload_extension("cogs.{}".format(file)[0:-3])
            except discord.ClientException:
                pass
            except ImportError:
                pass
    await bot.say("All modules have been loaded.")


@commands.check(ownercheck)
@bot.command(pass_context=True)
async def debug(ctx, *, code):
    """Evaluate code"""

    global_vars = globals().copy()
    global_vars['bot'] = bot
    global_vars['ctx'] = ctx
    global_vars['message'] = ctx.message
    global_vars['author'] = ctx.message.author
    global_vars['channel'] = ctx.message.channel
    global_vars['server'] = ctx.message.server

    try:
        result = eval(code, global_vars, locals())
        if asyncio.iscoroutine(result):
            result = await result
        result = str(result)  # the eval output was modified by me but originally submitted by DJ electro
        if len(result) > 2000:
            err2 = Exception("TooManyChars")
            raise err2
        embed = discord.Embed(title="<:success:442552796303196162> Evaluated successfully.", color=0x80ff80)
        embed.add_field(name="Input :inbox_tray:", value="```" + code + "```")
        embed.add_field(name="Output :outbox_tray:", value="```" + result + "```")
        await bot.say(embed=embed)
    except Exception as error:
        if str(type(error).__name__ + str(error)) == "HTTPException: BAD REQUEST (status code: 400)":
            return
        else:
            embed = discord.Embed(title="<:error:442552796420767754> Evaluation failed.", color=0xff0000)
            embed.add_field(name="Input :inbox_tray:", value="```" + code + "```", inline=True)
            embed.add_field(name="Error <:error2:442590069082161163>",
                        value='```{}: {}```'.format(type(error).__name__, str(error)))
            await bot.say(embed=embed)
            return

@bot.event
async def on_command_error(event, ctx):
    if isinstance(event, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, ":no_entry: Access to this command is restricted.")
        return
    if isinstance(event, commands.MissingRequiredArgument):
        await send_cmd_help(ctx)
        return
    if isinstance(event, commands.CommandNotFound):
        pass
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(event), event, event.__traceback__, file=sys.stderr)


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)

@bot.event
async def on_command(command, ctx):
    message = ":pencil2: Command `{}` has been ran by `{}` in `{}` (`{}`)".format(ctx.message.content, ctx.message.author, ctx.message.channel, ctx.message.server)
    command = bot.get_command(str(ctx.command))
    try:
        check = command.checks[0]
        allowed = check(ctx)
    except IndexError:
        allowed = True
    if not allowed:
        message = message + ". They were denied access to the command."
    await bot.send_message(bot.get_channel(Config.loggingchannel), message)


# Load extensions and start the bot
if __name__ == "__main__":
    #bot.remove_command("help")
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
# Run the bot object with token
    bot.run(Config.bottoken)
