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

                chat = message.to_id
                client = message.client
                # Delete the command message first
                await message.delete()
                
                while True:
                    task = client.send_message(chat, file=InputMediaDice(emoji))
                    message = await task
                    rolled = message.media.value
                    logger.debug("Rolled %d", rolled)
                    if rolled in even_values:
                        break
                    else:
                        # Delete the dice message if it's not an even number
                        await message.delete()
            else:
                # If the security check fails, reply that permission is needed (message not deleted here for context)
                reply = await message.reply("You do not have permission to use this command.")
                await asyncio.sleep(5)  # Give the user some time to read the message
                await reply.delete()
                await message.delete()
        else:
            # If the command is invalid, notify the user and delete the notification after some time
            reply = await message.reply("Invalid command. Use `.dice chet` to roll the dice until an even number.")
            await asyncio.sleep(5)  # Give the user some time to read the message
            await reply.delete()
            await message.delete()
