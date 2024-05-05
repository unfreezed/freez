
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
           .dice <emoji> <outcomes> <count>"""
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
            values = set()
            try:
                for val in args[1].split(","):
                    value = int(val)
                    if value in possible:
                        values.add(value)
            except (ValueError, IndexError):
                values.clear()
            try:
                count = int(args[2])
            except (ValueError, IndexError):
                count = 1

            rolled = -1
            chat = message.to_id
            client = message.client
            deleted = False  # Отслеживание состояния удаления сообщения

            # Ограничение количества попыток до 2 (один начальный бросок и один повторный)
            for attempt in range(2):
                task = client.send_message(chat, file=InputMediaDice(emoji))
                message = await task
                rolled = message.media.value
                logger.debug("Rolled %d", rolled)
                if rolled not in values and not deleted:
                    await message.delete()
                    deleted = True
                elif rolled in values:
                    break  # Выход из цикла, если бросок успешен
        else:
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"
            await message.reply(file=InputMediaDice(emoji))
