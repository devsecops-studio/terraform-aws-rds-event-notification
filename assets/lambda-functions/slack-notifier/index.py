import base64
import json
import logging
import os

import requests

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger()
logger.setLevel(logging.getLevelName(LOG_LEVEL.upper()))

SLACK_WEBHOOK = base64.b64decode(os.environ["SLACK_WEBHOOK"])


def lambda_handler(event, context):
    logger.info(json.dumps(event))
    rds_event = json.loads(event["Records"][0]["Sns"]["Message"])
    return send_slack_message(rds_event)


def send_slack_message(event):
    logger.info(json.dumps(event))
    event_id = event["Event ID"].split("#")[1]
    data = {
        "attachments": [
            {
                "color": get_slack_color(event_id),
                "fallback": f"RDS Event",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*RDS Event*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{event['Event Message']}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Source ID:* {event['Source ID']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Event Time:* {event['Event Time']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Event Source:* {event['Event Source']}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Event ID:* {event_id}"
                            },
                        ]
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "image",
                                "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
                                "alt_text": "notifications warning icon"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"<{event["Identifier Link"]}|Affected resource>"
                            }
                        ]
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(SLACK_WEBHOOK, headers=headers, json=data)
    if r.status_code != 200:
        msg = f"Failed to sent message to Slack due to: {r.json()}"
        logger.error(msg)
        return False, msg


def get_slack_color(event_id: str) -> str:
    if event_id in ["RDS-EVENT-0170", "RDS-EVENT-0071", "RDS-EVENT-0181", "RDS-EVENT-0182", "RDS-EVENT-0184", "RDS-EVENT-0185", "RDS-EVENT-0238", "RDS-EVENT-0239", "RDS-EVENT-0241", "RDS-EVENT-0176", "RDS-EVENT-0289", "RDS-EVENT-0172", "RDS-EVENT-0002", "RDS-EVENT-0011", "RDS-EVENT-0014", "RDS-EVENT-0017", "RDS-EVENT-0025", "RDS-EVENT-0029", "RDS-EVENT-0032", "RDS-EVENT-0067", "RDS-EVENT-0092", "RDS-EVENT-0218", "RDS-EVENT-0296", "RDS-EVENT-0335", "RDS-EVENT-0005", "RDS-EVENT-0015", "RDS-EVENT-0049", "RDS-EVENT-0051", "RDS-EVENT-0065", "RDS-EVENT-0328", "RDS-EVENT-0353", "RDS-EVENT-0329", "RDS-EVENT-0027", "RDS-EVENT-0047", "RDS-EVENT-0265", "RDS-EVENT-0268"]:
        return "#2EB67D"  # green
    elif event_id in ["RDS-EVENT-0016", "RDS-EVENT-0069", "RDS-EVENT-0183", "RDS-EVENT-0187", "RDS-EVENT-0177", "RDS-EVENT-0004", "RDS-EVENT-0022", "RDS-EVENT-0221", "RDS-EVENT-0086", "RDS-EVENT-0016", "RDS-EVENT-0028", "RDS-EVENT-0003", "RDS-EVENT-0058", "RDS-EVENT-0079", "RDS-EVENT-0080", "RDS-EVENT-0081", "RDS-EVENT-0223", "RDS-EVENT-0278", "RDS-EVENT-0279", "RDS-EVENT-0266", "RDS-EVENT-0270"]:
        return "#E01E5A"  # red
    else:
        return "#C4A20E"  # yellow
