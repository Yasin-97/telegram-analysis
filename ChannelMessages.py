import configparser
import json
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import (
    Channel, ChannelForbidden, Chat, ChatEmpty, ChatForbidden, ChatFull,
    ChatPhoto, InputPeerChannel, InputPeerChat, InputPeerUser, InputPeerEmpty,
    MessageMediaDocument, MessageMediaPhoto, PeerChannel, InputChannel,
    UserEmpty, InputUser, InputUserEmpty, InputUserSelf, InputPeerSelf,
    PeerChat, PeerUser, User, UserFull, UserProfilePhoto, Document,
    MessageMediaContact, MessageMediaEmpty, MessageMediaGame, MessageMediaGeo,
    MessageMediaUnsupported, MessageMediaVenue, InputMediaContact,
    InputMediaDocument, InputMediaEmpty, InputMediaGame,
    InputMediaGeoPoint, InputMediaPhoto, InputMediaVenue, InputDocument,
    DocumentEmpty, InputDocumentEmpty, Message, GeoPoint, InputGeoPoint,
    GeoPointEmpty, InputGeoPointEmpty, Photo, InputPhoto, PhotoEmpty,
    InputPhotoEmpty, FileLocation, ChatPhotoEmpty, UserProfilePhotoEmpty,
    FileLocationUnavailable, InputMediaUploadedDocument, ChannelFull,
    InputMediaUploadedPhoto, DocumentAttributeFilename, photos,
    TopPeer, InputNotifyPeer, Message
)

from telethon.tl.types import Message
from telethon.tl.functions.messages import (GetDialogsRequest, GetHistoryRequest, SendMediaRequest)
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
client.start()
print("Client Created")
# Ensure you're authorized
if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Password: '))

me = client.get_me()

user_input_channel = input("enter entity(telegram URL or entity id):")

if user_input_channel.isdigit():
    entity = PeerChannel(int(user_input_channel))
else:
    entity = user_input_channel

my_channel = client.get_entity(entity)

offset_id = 0
limit = 1000
all_messages = []

while True:
    history = client(GetHistoryRequest(
        peer=my_channel,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))
    if not history.messages:
        break
    messages = history.messages
    for message in messages:
        all_messages.append(message.to_dict())
    offset_id = messages[len(messages)-1].id

with open('channel_messages.json', 'w') as outfile:
    json.dump(all_messages, outfile)