"""
Placeholder for smarter secret management.
"""
import os



def get_pico_token():
    tk = os.environ.get('PICO_TOKEN', None)
    assert tk is not None, \
        'Get token from https://picovoice.ai/docs/quick-start/porcupine-python/#picovoice-account--accesskey and assign it to "PICO_TOKEN"'
    return tk
