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

        if await self.allmodules.check_security(message, security.OWNER | security.SUDO):
            try:
                emoji = args[0]
            except IndexError:
                emoji = "🎲"
            possible = self.config["POSSIBLE_VALUES"].get(emoji, self.config["POSSIBLE_VALUES"]["🎲"])

            condition = args[1] if len(args) > 1 else None
            count = int(args[2]) if len(args) > 2 else 1

            rolled = -1
            done = 0
            chat = message.to_id
            client = message.client

            while done < count:
                task = client.send_message(chat, file=InputMediaDice(emoji))
                if message:
                    message = (await asyncio.gather(message.delete(), task))[1]
                else:
                    message = await task
                rolled = message.media.value
                logger.debug("Rolled %d", rolled)

                if condition in ["chet", "nechet"]:
                    if (condition == "chet" and rolled % 2 == 0) or (condition == "nechet" and rolled % 2 != 0):
                        done += 1
                    else:
                        await message.delete()
                else:
                    values = {int(x) for x in condition.split(",")} if condition else set()
                    if rolled in values:
                        done += 1
                    else:
                        await message.delete()
        else:
            emoji = args[0] if args else "🎲"
            await message.reply(file=InputMediaDice(emoji))
