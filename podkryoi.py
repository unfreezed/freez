import asyncio
import logging

from telethon.tl.types import InputMediaDice

from .. import loader, utils, security

logger = logging.getLogger(__name__)


@loader.tds
class EvenDiceMod(loader.Module):
    """Dice that rolls until an even number is rolled"""
    strings = {"name": "EvenDice"}

    def __init__(self):
        self.config = loader.ModuleConfig("POSSIBLE_VALUES", {"": [1, 2, 3, 4, 5, 6],
                                                              "🎲": [1, 2, 3, 4, 5, 6]},
                                          "Mapping of emoji to possible dice values")

    @loader.unrestricted
    async def dicecmd(self, message):
        """Rolls a die until an even value is obtained. Use `.dice chet`."""
        args = utils.get_args(message)
        if args and args[0].lower() == "chet":
            if await self.allmodules.check_security(message, security.OWNER | security.SUDO):
                emoji = "🎲"
                possible = self.config["POSSIBLE_VALUES"][emoji]
                even_values = {value for value in possible if value % 2 == 0}

                rolled = -1
                chat = message.to_id
                client = message.client
                message = await message.reply("Rolling the dice until an even number is rolled...")
                while True:
                    task = client.send_message(chat, file=InputMediaDice(emoji))
                    if message:
                        message = (await asyncio.gather(message.delete(), task))[1]
                    else:
                        message = await task
                    rolled = message.media.value
                    logger.debug("Rolled %d", rolled)
                    if rolled in even_values:
                        break
            else:
                await message.reply("You do not have permission to use this command.")
        else:
            await message.reply("Invalid command. Use `.dice chet` to roll the dice until an even number.")
