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
            await message.delete()  # Удаляем сообщение с командой если аргументы не предоставлены
            return
        
        condition = args[1] if len(args) > 1 else None
        count = int(args[2]) if len(args) > 2 else 1

        emoji = args[0] if args else "🎲"
        possible = self.config["POSSIBLE_VALUES"].get(emoji, self.config["POSSIBLE_VALUES"]["🎲"])

        client = message.client
        chat = message.to_id

        for _ in range(count):
            rolled = -1
            task = client.send_message(chat, file=InputMediaDice(emoji))
            dice_message = await task
            rolled = dice_message.media.value
            logger.debug("Rolled %d", rolled)

            if condition == "chet" and rolled % 2 == 0:
                break
            elif condition == "nechet" and rolled % 2 != 0:
                break
            await dice_message.delete()  # Удаляем сообщение с броском кубика, если условие не выполнено

        await message.delete()  # Удаляем сообщение с командой .dice после выполнения
