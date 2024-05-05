import asyncio
import logging

from telethon.tl.types import InputMediaDice

from .. import loader, utils, security

logger = logging.getLogger(__name__)

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
            emoji = args[0] if args else "🎲"
            condition = args[1] if len(args) > 1 else ""
            count = int(args[2]) if len(args) > 2 else 1
            possible = self.config["POSSIBLE_VALUES"].get(emoji, [1, 2, 3, 4, 5, 6])

            done = 0
            chat = message.to_id
            client = message.client
            original_message = message
            while done < count:
                message = await client.send_message(chat, file=InputMediaDice(emoji))
                rolled = message.media.value
                logger.debug("Rolled %d", rolled)

                if (condition == "chet" and rolled % 2 == 0) or (condition == "nechet" and rolled % 2 != 0):
                    done += 1
                else:
                    await message.delete()

            await original_message.delete()
        else:
            emoji = args[0] if args else "🎲"
            await message.reply(file=InputMediaDice(emoji))

