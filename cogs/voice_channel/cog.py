# standard
from email.mime import audio
from typing import Optional
import datetime
import os
# nextcord
import nextcord
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import Context, command, group, Bot, Cog, has_permissions
# local
import config

# text-to-speech
from google.cloud import texttospeech_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'groovy-catalyst-362521-cac475922b5b.json'

class VoiceChannel(Cog, name= "🎤 Voice Channel"):

    def __init__(self, bot : Bot):
        self.bot = bot
    
    @command()
    @has_permissions(administrator=True)
    async def join(self, ctx : Context, channel_id : Optional[str]):
        emb = Embed(
        )
        if channel_id is None:
            try:
                channel = ctx.author.voice.channel
                await channel.connect()
                emb.description = f"Đã kết nối vào kênh Voice `{channel.name}`"
                emb.colour=nextcord.Color.green()
            except Exception as e:
                print(e)
                emb.description = f"Bạn hiện tại không ở trong kênh Voice nào cả!"
                emb.colour=nextcord.Color.red()
        else:
            try:
                channel = await self.bot.fetch_channel(int(channel_id))
                await channel.connect()
                emb.description = f"Đã kết nối vào kênh Voice `{channel.name}`"
                emb.colour=nextcord.Color.green()
            except Exception as e:
                print(e)
                emb.description = f"Kênh Voice với ID `{channel_id}` không tồn tại!"
                emb.colour=nextcord.Color.red()
        await ctx.send(embed=emb)

                
    @command()
    @has_permissions(administrator=True)
    async def leave(self, ctx : Context):
        await ctx.voice_client.disconnect()

    @command(name="tts")
    async def _tts(self, ctx: Context, *, text_to_speech: str):
        """text-to-speech (google-cloud texttospeech_v1 | default: vi-VN, neutral voice)"""
        user = ctx.author
        if user.voice != None:
            try:
                vc = await user.voice.channel.connect()
            except:
                vc = ctx.voice_client
            # instantiates a client
            ttsClient = texttospeech_v1.TextToSpeechClient()
            # set the text input to be synthesized
            synthesis_input = texttospeech_v1.SynthesisInput(text=text_to_speech)
            # build the voice request, in this case, select the language code ("en-US") and the ssml voice gender ("neutral")
            voice = texttospeech_v1.VoiceSelectionParams(
                language_code = "en-US",
                ssml_gender = texttospeech_v1.SsmlVoiceGender.NEUTRAL
            )
            if ctx.author.id == config.blueID:
                voice = texttospeech_v1.VoiceSelectionParams(
                    language_code = "en-US",
                    ssml_gender = texttospeech_v1.SsmlVoiceGender.MALE
                )
            # select the type of audio file we want to return
            audio_config = texttospeech_v1.AudioConfig(
                audio_encoding = texttospeech_v1.AudioEncoding.MP3
            )
            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = ttsClient.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            # The response's audio_content is binary.
            with open("tts_output.mp3", "wb") as out:
                # Write the response to the output file.
                out.write(response.audio_content)
                print('Audio content written to file "tts_output.mp3"')
            # bot play the mp3 audio file 
            vc.play(nextcord.FFmpegPCMAudio("tts_output.mp3"))
        else:
            await ctx.reply(
                "You have to be in a voice channel to use this command."
            )

def setup(bot : commands.Bot):
    bot.add_cog(VoiceChannel(bot))