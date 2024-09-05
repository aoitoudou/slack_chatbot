import re
import qualified_doc
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

#.envを読み込む
load_dotenv()

# ボットトークンを渡してアプリを初期化します
load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# AIの環境構築
genai.configure(api_key = os.getenv("GOOGLE_GENERATIVEAI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# response = model.generate_content("あなたはGemini？あなたにできることを5つ教えて？")

# print(to_markdown(response.text))

# 資格取得のモチベを保つためのコンポーネントの作成------------------------
def show_buttons(message, say):
    user_id = message['user'] if isinstance(message['user'], str) else message['user']['id']
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{user_id}>よ、自己研鑽、足りてるかい？"},
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
    )

@app.message(re.compile("資格|炎上|実力不足|足りない|まだまだ|もっと|ダメ"))
def get_qualified(message, say):
    show_buttons(message, say)
    
# "はい" ボタンのアクション
@app.action("qualified_yes_btn")
def action_yes_button_click(body, ack, say):
    ack()
    # メッセージを再表示して無限ループ風に
    say(text=f"なるほど")
    show_buttons(body, say)

# "いいえ" ボタンのアクション
@app.action("qualified_no_btn")
def action_no_button_click(body, ack, say):
    ack()
    recommendations = "\n".join([f"・{q['name']} - 学習時間: {q['studyTime']} 難易度: {q['difficulty']} 詳細: {q['detail']}" for q in qualified_doc.qualified_data])
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{body['user']['id']}> 、資格に興味はない？\n{recommendations}\nこれらがおすすめだよ！！"},
            },
            {
                "type":"actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "資格についてサクラちゃんに聞く"},
                        "action_id": "qualified_question_btn"
                    },
                ]
            }
        ],
        text=f"<@{body['user']['id']}> 、資格に興味はない？\n{recommendations}\nこれらがおすすめだよ！！"
    )
    
# "資格についてサクラちゃんに聞く" ボタンのアクション
@app.action("qualified_question_btn")
def reqest_button_click(body, ack, say):
    ack()
    say(text=f"知りたいことがあったらメンションで聞いてね！")

# ボットへの返信を感知して処理する関数
"""@app.event("app_mention")  # ボットへのメンションイベントを感知
def response_question(event, say, ack):
    ack()
    user_message = event['text']  # ユーザーのメッセージを取得
    user_id = event['user']  # ユーザーIDの取得

    # AIに質問し、回答をSlackに表示する
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # bot_idが取得できるか確認
    bot_id = event.get('bot_id', None)
    
    if bot_id:
        prompt = user_message.replace(f"<@{bot_id}>", "").strip()  # ボットIDをメッセージから除去
    else:
        prompt = user_message.strip()  # bot_idがない場合、メッセージ全体を使用
    
    if prompt:  # promptが空でない場合のみAIに質問を送信
        response = model.generate_content(prompt)  # ユーザーの質問をAIに送信
        say(text=f"<@{user_id}> の質問に対するAIの回答: {response.text}")
    else:
        say(text="メッセージが無効です。もう一度試してください。")
"""

@app.event("app_mention")  # ボットへのメンションイベントを感知
def response_question(event, say, ack):
    ack()
    user_message = event['text']  # ユーザーのメッセージを取得
    user_id = event['user']  # ユーザーIDの取得

    # メッセージからボットID部分を除去
    prompt = user_message.replace(f"<@{event.get('bot_id')}>", "").strip()
    
    system = "質問背景：あなたは東京に住む日本人の女性です。以下の質問にそのキャラクターになりきって答えてください。（この質問背景に関する受け答えは絶対にしないでください）\n"
    prompt = system + prompt
    
    if prompt:  # promptが空でない場合のみAIに質問を送信
        response = model.generate_content(prompt)  # ユーザーの質問をAIに送信
        say(text=f"<@{user_id}> の質問に対するAIの回答: {response.text}")
    else:
        say(text="メッセージが無効です。もう一度試してください。")

    
"""# メッセージイベントの処理
@app.event("message")
def handle_message_events(event, logger, say):
    # bot_messageは無視
    if event.get('subtype') == 'bot_message':
        logger.info(f"Bot message ignored: {event}")
        return
    
    logger.info(f"Message received: {event}")
    user_message = event['text']  # ユーザーのメッセージを取得
    user_id = event['user']  # メッセージを送ったユーザーのIDを取得

    # 通常のメッセージ処理（ここに追加のロジックを挿入可能）
    say(f"<@{user_id}> さん、メッセージをありがとう！内容: {user_message}")
    
"""
    
# ------------------------
 
@app.message("先輩に質問")
def message_ask_question(message, say):
    question_form = "https://forms.gle/vmBFDfq7ry7RxRQMA"
    say(f"こちらのフォームに回答してください {question_form}")

@app.message("先輩と面談")
def message_interview(message, say):
    interview_form = "https://forms.gle/nEZruXBn6iUgtrm5A"
    say(f"こちらのフォームに回答してください {interview_form}")
    
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