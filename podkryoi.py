import asyncio
import logging

from telethon.tl.types import InputMediaDice

from .. import loader, utils, security

logger = logging.getLogger(__name__)

@loader.tds
class DiceMod(loader.Module):
    """Dice"""
    strings = {"name": "Dice"}

    def __init__(self):
        self.config = loader.ModuleConfig("POSSIBLE_VALUES", {"": [1, 2, 3, 4, 5, 6],
                                                              "🎲": [1, 2, 3, 4, 5, 6],
                                                              "🎯": [1, 2, 3, 4, 5, 6],
                                                              "🏀": [1, 2, 3, 4, 5]},
                                          "Mapping of emoji to possible values")

    @loader.unrestricted
    async def dicecmd(self, message):
        """Rolls a die (optionally with the specified value)
           .dice <emoji> <count>"""
        args = utils.get_args(message)
        if await self.allmodules.check_security(message, security.OWNER | security.SUDO):
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"

            possible = self.config["POSSIBLE_VALUES"].get(emoji, None)
            if possible is None:
                emoji = "🎲"
            
            try:
                count = int(args[1])
            except (ValueError, IndexError):
                count = 1

            chat = message.to_id
            client = message.client
            task = None

            for _ in range(count):
                task = client.send_message(chat, file=InputMediaDice(emoji))

            if task:
                await asyncio.gather(message.delete(), task)
        else:
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"
            await message.reply(file=InputMediaDice(emoji))
