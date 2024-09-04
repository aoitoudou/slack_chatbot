import re
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# ボットトークンを渡してアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# 'こんにちは' を含むメッセージをリッスンします
@app.message("こんにちは")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"こんにちは、<@{message['user']}> さん！"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "クリックしてください"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"こんにちは、<@{message['user']}> さん！",
    )
    
# 資格取得のモチベを保つためのコンポーネントの作成
@app.message(re.compile("資格|炎上|実力不足|足りない|まだまだ|もっと|ダメ"))
def get_qualified(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{message['user']}>よ、自己研鑽、足りてるかい？"},
            },
            {
                "type":"actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "はい"},
                        "action_id": "qualified_yes_btn"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "いいえ"},
                        "action_id": "qualified_no_btn"
                    },
                    
                ]
            }
        ],
        text=f"<@{message['user']}>よ、自己研鑽、足りてるかい？",
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> さんがボタンをクリックしました！")

# "はい" ボタンのアクション
@app.action("qualified_yes_btn")
def action_yes_button_click(body, ack, say):
    ack()
    # say(f"<@{body['user']['id']}>、セーフ")
    

# "いいえ" ボタンのアクション
@app.action("qualified_no_btn")
def action_no_button_click(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> 、アウト")

if __name__ == "__main__":
    # アプリを起動して、ソケットモードで Slack に接続します
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()