from __future__ import division
from channels.generic.websocket import WebsocketConsumer
import json
from . import gcp_speech
import re
import sys
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class ChatConsumer(WebsocketConsumer):
    """
    WebSocketでの通信をハンドルする
    """
    def connect(self):
        # とりあえず無条件で受け入れる
        # 接続を拒否する場合はself.close()する
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        """
        受け取ったメッセージをそのままオウム返しに戻す
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': "hello"
        }))

        language_code = 'ja-JP'  # a BCP-47 language tag

        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        with gcp_speech.MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            num_chars_printed = 0
            for response in responses:
                if not response.results:
                    continue

                # The `results` list is consecutive. For streaming, we only care about
                # the first result being considered, since once it's `is_final`, it
                # moves on to considering the next utterance.
                result = response.results[0]
                if not result.alternatives:
                    continue

                # Display the transcription of the top alternative.
                transcript = result.alternatives[0].transcript

                # Display interim results, but with a carriage return at the end of the
                # line, so subsequent lines will overwrite them.
                #
                # If the previous result was longer than this one, we need to print
                # some extra spaces to overwrite the previous result
                overwrite_chars = ' ' * (num_chars_printed - len(transcript))

                if not result.is_final:
                    # sys.stdout.write(transcript + overwrite_chars + '\r')
                    # sys.stdout.flush()
                    # return(transcript + overwrite_chars + '\r')
                    self.send(text_data=json.dumps({
                        'message': transcript + overwrite_chars + '\r'
                    }))

                    num_chars_printed = len(transcript)


                else:
                    # print(transcript + overwrite_chars)
                    self.send(text_data=json.dumps({
                        'message': transcript + overwrite_chars
                    }))

                    # Exit recognition if any of the transcribed phrases could be
                    # one of our keywords.
                    if re.search(r'\b(exit|quit)\b', transcript, re.I):
                        # print('Exiting..')
                        self.send(text_data=json.dumps({
                            'message': 'Exiting..'
                        }))
                        break

                    num_chars_printed = 0
