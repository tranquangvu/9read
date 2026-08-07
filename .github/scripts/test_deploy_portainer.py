import os
import unittest
from unittest import mock

import deploy_portainer


class DeployPortainerTest(unittest.TestCase):
    @mock.patch.dict(os.environ, {
        "PORTAINER_URL": "https://portainer.example.com/api",
        "PORTAINER_API_KEY": "test-key",
        "PORTAINER_ENDPOINT_ID": "3",
        "PORTAINER_STACK_ID": "42",
    })
    @mock.patch("deploy_portainer.requests.put")
    @mock.patch("deploy_portainer.requests.get")
    def test_main_triggers_stack_update_with_pull_image(self, mock_get, mock_put):
        stack_response = mock.Mock()
        stack_response.json.return_value = {"Env": [{"name": "APP_PORT", "value": "9146"}]}
        stack_response.raise_for_status.return_value = None

        file_response = mock.Mock()
        file_response.json.return_value = {
            "StackFileContent": "services:\n  app:\n    image: ghcr.io/tranquangvu/9read:latest\n"
        }
        file_response.raise_for_status.return_value = None

        mock_get.side_effect = [stack_response, file_response]

        put_response = mock.Mock()
        put_response.status_code = 200
        put_response.raise_for_status.return_value = None
        mock_put.return_value = put_response

        deploy_portainer.main()

        mock_get.assert_any_call(
            "https://portainer.example.com/api/stacks/42",
            headers={"X-API-Key": "test-key"},
        )
        mock_get.assert_any_call(
            "https://portainer.example.com/api/stacks/42/file",
            headers={"X-API-Key": "test-key"},
        )

        put_call = mock_put.call_args
        self.assertEqual(put_call.args[0], "https://portainer.example.com/api/stacks/42")
        self.assertEqual(put_call.kwargs["params"], {"endpointId": "3"})
        payload = put_call.kwargs["json"]
        self.assertTrue(payload["PullImage"])
        self.assertFalse(payload["Prune"])
        self.assertEqual(payload["Env"], [{"name": "APP_PORT", "value": "9146"}])
        self.assertIn("ghcr.io/tranquangvu/9read:latest", payload["StackFileContent"])


if __name__ == "__main__":
    unittest.main()
