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
        if await self.allmodules.check_security(message, security.OWNER | security.SUDO):
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"
            possible = self.config["POSSIBLE_VALUES"].get(emoji, None)
            if possible is None:
                emoji = "🎲"
                possible = self.config["POSSIBLE_VALUES"][emoji]

            condition = args[1] if len(args) > 1 else ""
            try:
                count = int(args[2])
            except (ValueError, IndexError):
                count = 1

            done = 0
            chat = message.to_id
            client = message.client
            while True:
                task = client.send_message(chat, file=InputMediaDice(emoji))
                if message:
                    message = (await asyncio.gather(message.delete(), task))[1]
                else:
                    message = await task
                rolled = message.media.value
                logger.debug("Rolled %d", rolled)

                if condition == "1" and rolled % 2 != 0:  # Нечетное число
                    done += 1
                elif condition == "2" and rolled % 2 == 0:  # Четное число
                    done += 1
                else:
                    await message.delete()  # Удалить сообщение, если не выпало нужное число

                if done == count:
                    break

        else:
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"
            await message.reply(file=InputMediaDice(emoji))
