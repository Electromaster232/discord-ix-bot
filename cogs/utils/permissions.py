import discord
from config import Config


def modcheck(ctx):
    roles = ctx.message.server.roles
    role = discord.utils.get(roles, name="Moderator")
    return role in ctx.message.author.roles or ownercheck(ctx) or admincheck(ctx)



def admincheck(ctx):
    roles = ctx.message.server.roles
    role = discord.utils.get(roles, name="Administrator")
    return role in ctx.message.author.roles or ownercheck(ctx) or admincheck(ctx)

def managecheck(ctx):
    return ctx.message.author.server_permissions.manage_server or ownercheck(ctx)


def ownercheck(ctx):
    return ctx.message.author.id in Config.botowners