from typing import Any, Dict

from httpx import AsyncClient


DEV_OAUTH_CLIENT_IDS = [
    "1060725074195-kmeum4crr01uirfl2op9kd5acmi9jutn.apps.googleusercontent.com",
    # google client id
    "467101b197249757c71f",  # github client id
]
DEV_KEY_IDENTIFIER = "4398792-"
DEV_OAUTH_AUTHORIZATION_URL = "https://supertokens.io/dev/oauth/redirect-to-provider"
DEV_OAUTH_REDIRECT_URL = "https://supertokens.io/dev/oauth/redirect-to-app"


def is_using_oauth_development_client_id(client_id: str):
    return client_id.startswith(DEV_KEY_IDENTIFIER) or client_id in DEV_OAUTH_CLIENT_IDS


def get_actual_client_id_from_development_client_id(client_id: str):
    if client_id.startswith(DEV_KEY_IDENTIFIER):
        return client_id.split(DEV_KEY_IDENTIFIER, 1)[1]
    return client_id


async def do_get_request(
    url: str, query_params: Dict[str, str] = {}, headers: Dict[str, str] = {}
) -> Dict[str, Any]:
    # TODO logging

    async with AsyncClient() as client:
        return (
            await client.get(url, params=query_params, headers=headers)  # type:ignore
        ).json()


async def do_post_request(
    url: str, body_params: Dict[str, str] = {}, headers: Dict[str, str] = {}
) -> Dict[str, Any]:
    if not headers:
        headers = {}

    headers["content-type"] = "application/x-www-form-urlencoded"
    headers["accept"] = "application/json"

    # TODO logging

    async with AsyncClient() as client:
        return (
            await client.post(url, data=body_params, headers=headers)  # type:ignore
        ).json()
