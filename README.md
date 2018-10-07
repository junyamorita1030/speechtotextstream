# Speechtotextstream

## Description

マイク・ブラウザ・通話アプリからの音声をテキスト化し、画面に表示するアプリです。

ブラウザや通話アプリからの音源を取得するには、loopback.app等のループバック録音用のアプリを使う等してください。

マイク等の音源を切り替える場合は、input_device_indexを変更してください。

```
def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
            input_device_index = 4
        )
```

## Movie

以下の動画を参考にしてください。

https://github.com/junyamorita1030/speechtotextstream/blob/master/stt_from_mic.mov

https://github.com/junyamorita1030/speechtotextstream/blob/master/stt_from_browser.m4v



## How to use

ライブラリをインストール
```
pip install django Pillow pyaudio
```

djangoページを起動

```
cd audio_stream/stt_with_brouser
python manage.py runserver
```

djangoページへアクセス

startボタンを押下

テキスト化したい音源を再生
(マイクを用いる場合はマイクの集音を開始)
