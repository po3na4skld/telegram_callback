from keras.callbacks import Callback
import requests


class TelegramCallback(Callback):

    def __init__(self, username):
        super(TelegramCallback, self).__init__()
        self.token = 'your bot token'
        res = requests.get("https://api.telegram.org/bot{}/getUpdates".format(self.token))
        jsn = res.json()['result']
        for updt in jsn:
            if updt['message']['from']['username'] == username:
                self.chat_id = updt['message']['chat']['id']

    def send_info(self, text):
        requests.post("https://api.telegram.org/bot{}/sendMessage".format(self.token),
                      data={'chat_id': self.chat_id, 'text': text})

    def on_train_begin(self, logs=None):
        if requests is None:
            raise ImportError('Notification requires the requests library.')
        text = 'Training successfully started.'
        self.send_info(text)

    def on_train_end(self, logs=None):
        text = 'Training successfully ended.'
        self.send_info(text)

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        text = 'Epoch {}: '.format(epoch + 1)
        for metric in self.params['metrics']:
            text += '{}: {:.3f} '.format(metric, logs[metric])
        self.send_info(text)
