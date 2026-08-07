#!/usr/bin/env python3
"""Trigger a Portainer stack update: pulls the freshly-pushed ghcr.io image
and recreates the 9read container. One image, one service, one stack --
a simplified version of the multi-stack Portainer deploy pattern used
elsewhere.
"""
import os
import sys

import requests


def main():
    url = os.environ["PORTAINER_URL"].rstrip("/")
    api_key = os.environ["PORTAINER_API_KEY"]
    endpoint_id = os.environ["PORTAINER_ENDPOINT_ID"]
    stack_id = os.environ["PORTAINER_STACK_ID"]
    headers = {"X-API-Key": api_key}

    print("Fetching current stack config...")
    stack_resp = requests.get(f"{url}/stacks/{stack_id}", headers=headers)
    stack_resp.raise_for_status()
    stack = stack_resp.json()

    print("Fetching current stack file...")
    file_resp = requests.get(f"{url}/stacks/{stack_id}/file", headers=headers)
    file_resp.raise_for_status()
    stack_file_content = file_resp.json()["StackFileContent"]

    print("Updating stack and pulling latest image...")
    update_resp = requests.put(
        f"{url}/stacks/{stack_id}",
        params={"endpointId": endpoint_id},
        headers={**headers, "Content-Type": "application/json"},
        json={
            "StackFileContent": stack_file_content,
            "Env": stack.get("Env", []),
            "Prune": False,
            "PullImage": True,
        },
    )
    update_resp.raise_for_status()
    print(f"Stack update triggered: HTTP {update_resp.status_code}")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.RequestException as error:
        print(f"Failed: {error}", file=sys.stderr)
        sys.exit(1)
