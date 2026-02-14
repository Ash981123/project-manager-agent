#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
é¡¹ç›®ç®¡ç†Agent - GitHub Actionsç‰ˆæœ¬
è‡ªåŠ¨ä»Žé£žä¹¦å¤šç»´è¡¨æ ¼è¯»å–ä»»åŠ¡ï¼Œå¹¶å‘é€æé†’åˆ°é£žä¹¦
"""

import os
import sys
import json
from datetime import datetime, timedelta
import pytz

# é£žä¹¦SDK
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
from lark_oapi.api.im.v1 import *


class FeishuReminder:
    """é£žä¹¦æé†’å™¨"""

    def __init__(self):
        # ä»ŽçŽ¯å¢ƒå˜é‡è¯»å–é…ç½®
        self.app_id = os.environ.get('FEISHU_APP_ID')
        self.app_secret = os.environ.get('FEISHU_APP_SECRET')
        self.app_token = os.environ.get('FEISHU_APP_TOKEN')
        self.table_id = os.environ.get('FEISHU_TABLE_ID')
        self.chat_id = os.environ.get('FEISHU_CHAT_ID')

        # éªŒè¯é…ç½®
        if not all([self.app_id, self.app_secret, self.app_token, self.table_id, self.chat_id]):
            print("âŒ é”™è¯¯ï¼šç¼ºå°‘å¿…è¦çš„çŽ¯å¢ƒå˜é‡é…ç½®")
            print("è¯·åœ¨GitHubä»“åº“çš„Settings -> Secretsä¸­é…ç½®ï¼š")
            print("- FEISHU_APP_ID")
            print("- FEISHU_APP_SECRET")
            print("- FEISHU_APP_TOKEN")
            print("- FEISHU_TABLE_ID")
            print("- FEISHU_CHAT_ID")
            sys.exit(1)

        # åˆå§‹åŒ–å®¢æˆ·ç«¯
        self.client = lark.Client.builder() \
            .app_id(self.app_id) \
            .app_secret(self.app_secret) \
            .build()

    def get_weekly_tasks(self):
        """èŽ·å–æœ¬å‘¨ä»»åŠ¡"""
        try:
            # èŽ·å–æ‰€æœ‰è®°å½•
            request = ListAppTableRecordRequest.builder() \
                .app_token(self.app_token) \
                .table_id(self.table_id) \
                .page_size(500) \
                .build()

            response = self.client.bitable.v1.app_table_record.list(request)

            if not response.success():
                print(f"âŒ èŽ·å–è®°å½•å¤±è´¥: {response.msg}")
                return []

            # è®¡ç®—æœ¬å‘¨èŒƒå›´
            tz = pytz.timezone('Asia/Shanghai')
            now = datetime.now(tz)
            week_start = now - timedelta(days=now.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

            print(f"ðŸ“… æœ¬å‘¨èŒƒå›´: {week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}")

            # ç­›é€‰æœ¬å‘¨ä»»åŠ¡
            weekly_tasks = []
            if response.data and response.data.items:
                for item in response.data.items:
                    fields = item.fields

                    # èŽ·å–æˆªæ­¢æ—¥æœŸ
                    deadline = fields.get('æˆªæ­¢æ—¥æœŸ')
                    if not deadline:
                        continue

                    try:
                        deadline_dt = datetime.fromtimestamp(deadline / 1000, tz=tz)
                    except:
                        continue

                    # æ£€æŸ¥æ˜¯å¦åœ¨æœ¬å‘¨èŒƒå›´å†…
                    if week_start <= deadline_dt <= week_end:
                        status = fields.get('çŠ¶æ€', '')
                        if status != 'å·²å®Œæˆ':
                            task = {
                                'name': fields.get('ä»»åŠ¡åç§°', 'æœªå‘½åä»»åŠ¡'),
                                'deadline': deadline_dt,
                                'priority': fields.get('ä¼˜å…ˆçº§', 'ä¸­'),
                                'status': status,
                                'description': fields.get('æè¿°', '')
                            }
                            weekly_tasks.append(task)

            # æŽ’åº
            priority_order = {'é«˜': 1, 'ä¸­': 2, 'ä½Ž': 3}
            weekly_tasks.sort(key=lambda x: (
                priority_order.get(x['priority'], 4),
                x['deadline']
            ))

            print(f"âœ… æ‰¾åˆ° {len(weekly_tasks)} ä¸ªå¾…åŠžä»»åŠ¡")
            return weekly_tasks

        except Exception as e:
            print(f"âŒ èŽ·å–ä»»åŠ¡å¼‚å¸¸: {e}")
            return []

    def send_task_card(self, tasks, is_thursday=False):
        """å‘é€ä»»åŠ¡å¡ç‰‡åˆ°é£žä¹¦"""
        try:
            # æ ¹æ®æ˜ŸæœŸå‡ å†³å®šæ ‡é¢˜å’Œé¢œè‰²
            if is_thursday:
                title = "ðŸ”” æœ¬å‘¨è¿›åº¦è·Ÿè¿›"
                color = "orange"
                # å‘¨å››åªæ˜¾ç¤ºæœªå®Œæˆçš„
                tasks = [t for t in tasks if t['status'] != 'å·²å®Œæˆ']
            else:
                title = "ðŸ“… æœ¬å‘¨å¾…åŠžäº‹é¡¹"
                color = "blue"

            # æž„å»ºå¡ç‰‡å†…å®¹
            elements = []

            if tasks:
                for i, task in enumerate(tasks, 1):
                    priority_text = {
                        'é«˜': 'ðŸ”´ é«˜ä¼˜å…ˆçº§',
                        'ä¸­': 'ðŸŸ¡ ä¸­ä¼˜å…ˆçº§',
                        'ä½Ž': 'ðŸŸ¢ ä½Žä¼˜å…ˆçº§'
                    }.get(task['priority'], 'âšª æ™®é€š')

                    deadline_str = task['deadline'].strftime('%mæœˆ%dæ—¥ %H:%M')

                    elements.append({
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**{i}. {task['name']}**"
                        }
                    })

                    elements.append({
                        "tag": "div",
                        "fields": [
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**ä¼˜å…ˆçº§**\n{priority_text}"
                                }
                            },
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**æˆªæ­¢æ—¶é—´**\n{deadline_str}"
                                }
                            },
                            {
                                "is_short": True,
                                "text": {
                                    "tag": "lark_md",
                                    "content": f"**çŠ¶æ€**\n{task['status']}"
                                }
                            }
                        ]
                    })

                    if task.get('description'):
                        elements.append({
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": f"ðŸ“ {task['description']}"
                            }
                        })

                    if i < len(tasks):
                        elements.append({"tag": "hr"})
            else:
                elements.append({
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "æš‚æ— å¾…åŠžä»»åŠ¡ âœ…"
                    }
                })

            # æž„å»ºå®Œæ•´å¡ç‰‡
            card = {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": color,
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    }
                },
                "elements": elements
            }

            # å‘é€æ¶ˆæ¯
            request = CreateMessageRequest.builder() \
                .receive_id_type("chat_id") \
                .request_body(CreateMessageRequestBody.builder()
                              .receive_id(self.chat_id)
                              .msg_type("interactive")
                              .content(json.dumps(card, ensure_ascii=False))
                              .build()) \
                .build()

            response = self.client.im.v1.message.create(request)

            if response.success():
                print(f"âœ… æé†’å‘é€æˆåŠŸï¼")
                return True
            else:
                print(f"âŒ å‘é€å¤±è´¥: {response.msg}")
                return False

        except Exception as e:
            print(f"âŒ å‘é€å¼‚å¸¸: {e}")
            return False


def main():
    """ä¸»å‡½æ•°"""
    print("="*60)
    print("é¡¹ç›®ç®¡ç†Agent - è‡ªåŠ¨æé†’")
    print("="*60)

    # åˆ¤æ–­ä»Šå¤©æ˜¯æ˜ŸæœŸå‡ 
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)
    weekday = now.weekday()  # 0=å‘¨ä¸€, 3=å‘¨å››
    is_thursday = (weekday == 3)

    print(f"å½“å‰æ—¶é—´: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"æ˜ŸæœŸ: {'ä¸€äºŒä¸‰å››äº”å…­æ—¥'[weekday]}")
    print()

    # åˆ›å»ºæé†’å™¨
    reminder = FeishuReminder()

    # èŽ·å–æœ¬å‘¨ä»»åŠ¡
    print("æ­£åœ¨èŽ·å–æœ¬å‘¨ä»»åŠ¡...")
    tasks = reminder.get_weekly_tasks()

    # å‘é€æé†’
    if tasks or not is_thursday:  # å‘¨ä¸€æ€»æ˜¯å‘é€ï¼Œå‘¨å››åªåœ¨æœ‰ä»»åŠ¡æ—¶å‘é€
        print()
        print("æ­£åœ¨å‘é€æé†’...")
        success = reminder.send_task_card(tasks, is_thursday=is_thursday)

        if success:
            print()
            print("="*60)
            print("âœ… ä»»åŠ¡å®Œæˆï¼")
            print("="*60)
        else:
            print()
            print("="*60)
            print("âŒ å‘é€å¤±è´¥ï¼Œè¯·æ£€æŸ¥é…ç½®")
            print("="*60)
            sys.exit(1)
    else:
        print("å‘¨å››æ— å¾…åŠžä»»åŠ¡ï¼Œè·³è¿‡å‘é€")


if __name__ == '__main__':
    main()

