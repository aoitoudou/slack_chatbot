import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# ボットトークンを渡してアプリを初期化します
load_dotenv()
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
            }
        ],
        text=f"こんにちは、<@{message['user']}> さん！",
    )

@app.action("button_click")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> さんがボタンをクリックしました！")

@app.message("社内wiki")
def handle_wiki_request(message, say):
    user = message['user']
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{user}> さん、知りたいことは何ですか？"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "機材の使い方"},
                        "action_id": "equipment_usage"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "連絡先"},
                        "action_id": "contacts"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "資料の場所"},
                        "action_id": "document_location"
                    }
                ]
            }
        ]
    )

# "機材の使い方"の選択肢を表示
@app.action("equipment_usage")
def show_equipment_options(ack, body, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "機材の使い方に関する情報を選んでください"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "コピー機"},
                        "action_id": "copier_info"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "製造機"},
                        "action_id": "machine_info"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "PC関連"},
                        "action_id": "pc_info"
                    }
                ]
            }
        ]
    )

# "連絡先"の選択肢を表示
@app.action("contacts")
def show_contact_options(ack, body, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "連絡先に関する情報を選んでください"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "自社"},
                        "action_id": "own_company_contact"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "取引先"},
                        "action_id": "business_partner_contact"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "お得意様"},
                        "action_id": "client_contact"
                    }
                ]
            }
        ]
    )

@app.action("contacts")
def show_contact_options(ack, body, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "知りたい資料はなんですか？"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "法務関連"},
                        "action_id": "legal_affairs"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "セキュリティ関連"},
                        "action_id": "security"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "会計関連"},
                        "action_id": "accounting"
                    }
                ]
            }
        ]
    )

@app.action("legal_affairs")
def show_legal(ack, say):
    ack()
    say("法務関連の資料は～にあります")
    
@app.action("security")
def show_legal(ack, say):
    ack()
    say("セキュリティ関連の資料は～にあります")

@app.action("accounting")
def show_accounting(ack, say):
    ack()
    say("会計関連の資料は～にあります")

# "PC関連"の選択肢を表示
@app.action("pc_info")
def show_pc_options(ack, body, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "PC関連の情報を選んでください"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Excel資料"},
                        "action_id": "excel_info"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "パソコン"},
                        "action_id": "computer_info"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "接続方法"},
                        "action_id": "connection_info"
                    }
                ]
            }
        ]
    )

# 各ボタンに対する説明を返す
@app.action("excel_info")
def show_copier_info(ack, say):
    ack()
    say("シート１は～を求めるためのものです")
    
@app.action("computer_info")
def show_copier_info(ack, say):
    ack()
    say("パソコンが動かなかったら～を確認してください")

@app.action("connection_info")
def show_copier_info(ack, say):
    ack()
    say("～のパスワードを知りたい場合、～さんに確認してください")
@app.action("copier_info")
def show_copier_info(ack, say):
    ack()
    say("コピー機の使い方は以下の通りです…")

@app.action("machine_info")
def show_machine_info(ack, say):
    ack()
    say("製造機の使い方は以下の通りです…")

@app.action("pc_info")
def show_pc_info(ack, say):
    ack()
    say("PC関連の情報は以下の通りです…")

@app.action("own_company_contact")
def show_own_company_contact(ack, say):
    ack()
    say("自社の連絡先は…")

@app.action("business_partner_contact")
def show_business_partner_contact(ack, say):
    ack()
    say("取引先の連絡先は…")

@app.action("client_contact")
def show_client_contact(ack, say):
    ack()
    say("お得意様の連絡先は…")


if __name__ == "__main__":
    # アプリを起動して、ソケットモードで Slack に接続します

    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


