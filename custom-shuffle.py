#!/usr/bin/env python3

import json
import sys
import urllib.request
import ssl
from datetime import datetime


def main():
    """
    Wazuh custom integration script for sending JSON alerts to a Shuffle webhook.

    Expected Wazuh integration arguments:
      argv[1] = alert file path
      argv[2] = api key / reserved argument from Wazuh
      argv[3] = hook URL

    Example Wazuh ossec.conf block:

    <integration>
      <name>custom-shuffle.py</name>
      <hook_url>https://<SHUFFLE_VM_IP>:3443/api/v1/hooks/<WEBHOOK_ID></hook_url>
      <level>10</level>
      <alert_format>json</alert_format>
    </integration>
    """

    if len(sys.argv) < 4:
        print("Usage: custom-shuffle.py <alert_file> <api_key> <hook_url>")
        sys.exit(1)

    alert_file = sys.argv[1]
    hook_url = sys.argv[3]

    with open(alert_file, "r", encoding="utf-8") as f:
        alert = json.load(f)

    payload = {
        "source": "wazuh",
        "integration": "custom-shuffle",
        "sent_at": datetime.utcnow().isoformat() + "Z",
        "alert": alert
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        hook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    # Shuffle's local HTTPS listener may use a self-signed certificate in a lab.
    # This disables SSL verification for that lab setup.
    context = ssl._create_unverified_context()

    try:
        with urllib.request.urlopen(request, context=context, timeout=10) as response:
            print(response.read().decode("utf-8"))
    except Exception as e:
        print(f"Error sending alert to Shuffle: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
