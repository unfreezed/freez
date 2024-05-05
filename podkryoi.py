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
           .dice <emoji> <condition> <count>"""
        args = utils.get_args(message)
        if not args:
            await message.delete()
            return

        emoji = args[0] if args else "🎲"
        possible = self.config["POSSIBLE_VALUES"].get(emoji, [1, 2, 3, 4, 5, 6])
        if not possible:
            await message.reply("Invalid emoji for dice roll.")
            return

        condition = args[1] if len(args) > 1 else None
        count = int(args[2]) if len(args) > 2 else 1

        chat = message.to_id
        client = message.client
        await message.delete()  # Deleting the command message immediately

        for _ in range(count):
            message = await client.send_message(chat, file=InputMediaDice(emoji))
            rolled = message.media.value
            logger.debug("Rolled %d", rolled)

            if condition == "chet" and rolled % 2 == 0:
                break
            elif condition == "nechet" and rolled % 2 != 0:
                break
            elif condition and int(condition) == rolled:
                break
            await message.delete()  # Delete dice roll message if it doesn't meet the condition
