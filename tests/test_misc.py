import asyncio
from subprocess import STDOUT, TimeoutExpired
from unittest import TestCase

import nest_asyncio  # type: ignore
from supertokens_python.ingredients.emaildelivery.services.smtp import (
    GetContentResult, SMTPServiceConfig, SMTPServiceConfigFrom, Transporter)


class TransporterTests(TestCase):
    def test_transporter(self):  # pylint: disable=no-self-use
        local_insecure_smtpd_config_without_auth = SMTPServiceConfig(
            host="localhost",
            from_=SMTPServiceConfigFrom("Foo bar", "foo@example.com"),
            port=1025,
            secure=False,
        )

        transporter = Transporter(
            smtp_settings=local_insecure_smtpd_config_without_auth,
        )

        content = GetContentResult(
            body="<h1>Hello world</h1>",
            subject='Greetings',
            to_email='bar@example.com',
            is_html=True,
        )

        import time
        from subprocess import PIPE, Popen

        command = "python -m smtpd -c DebuggingServer -n localhost:1025"
        proc = Popen(command.split(), stdout=PIPE, stderr=STDOUT)  # Starts a SMTP daemon

        is_sent = False

        def send_email():
            nonlocal is_sent
            loop = asyncio.get_event_loop()
            nest_asyncio.apply(loop)  # type: ignore
            loop.run_until_complete(transporter.send_email(content, {}))
            is_sent = True

        try:
            time.sleep(0.2)
            send_email()
            while not is_sent:
                continue
        finally:
            proc.terminate()
            try:
                out, _ = proc.communicate(timeout=0.2)
                out = out.decode('utf-8').replace("\\n", "\n")
                assert out != ""
                assert out == """---------- MESSAGE FOLLOWS ----------
b'Content-Type: text/html; charset="us-ascii"'
b'MIME-Version: 1.0'
b'Content-Transfer-Encoding: 7bit'
b'From: Foo bar <foo@example.com>'
b'To: bar@example.com'
b'Subject: Greetings'
b'X-Peer: 127.0.0.1'
b''
b'<h1>Hello world</h1>'
------------ END MESSAGE ------------
"""
            except TimeoutExpired:
                raise Exception('subprocess did not terminate in time')
