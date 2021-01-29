import discord, os

from core.files import Data
from core import checks

from discord.ext import commands

config = Data("config").json_read

bot = commands.Bot(command_prefix=config["prefix"], case_insensitive=True, help_command=None)

@bot.event
async def on_ready():
    print(f"Bot is ready!\nLogged in as {bot.user}")

@checks.manager()
@bot.command(aliases=["e"])
async def eval(ctx, *, body: str):
    raw = False
    """Evaluates a code"""

    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'guild': ctx.message.guild,
        'message': ctx.message,
       }
    if ctx.message.author.id in Files.config("main", "managers"):
      env.update(globals())

      stdout = io.StringIO()

      to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

      try:
          exec(to_compile, env)
      except Exception as e:
          return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

      func = env['func']
      try:
         with redirect_stdout(stdout):
            ret = await func()
      except Exception:
          value = stdout.getvalue()
          await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
      else:
          value = stdout.getvalue()
          try:
              await ctx.message.add_reaction('\u2705')
          except:
              pass

          if ret is None:
              if value:
                  if raw:
                    await ctx.send(f"{value}")
                  else:
                    await ctx.send(f'```py\n{value}\n```')
          else:
              pass

@checks.manager()
@bot.command(hidden=True)
async def load(ctx, *, module):
    try:
      bot.load_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=discord.Embed(title=f"Loaded {str(module).capitalize()}", description=f"Successfully loaded cogs.{str(module).lower()}!", color=0x2cf818)
      await ctx.send(embed=embed)

@checks.manager()
@bot.command(hidden=True)
async def unload(ctx, *, module):
    try:
      bot.unload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=discord.Embed(title=f"Unloaded {str(module).capitalize()}", description=f"Successfully unloaded cogs.{str(module).lower()}!", color=0xeb1b2c)
      await ctx.send(embed=embed)

@checks.manager()
@bot.command(name="reload", hidden=True)
async def _reload(ctx, *, module):
    try:
      bot.reload_extension(f"cogs.{module}")
    except commands.ExtensionError as e:
      await ctx.send(f'{e.__class__.__name__}: {e}')
    else:
      embed=discord.Embed(title=f"Reloaded {str(module).capitalize()}", description=f"Successfully reloaded cogs.{str(module).lower()}!", color=0x00d4ff)
      await ctx.send(embed=embed)

for file in [i for i in os.listdir("cogs") if i.endswith(".py")]:
    try:
        bot.load_extension(f"cogs.{file[:-3]}")
    except Exception as e:
        print(f"######\nFailed to load {file}: {e}\n######")

bot.run(config["token"])
