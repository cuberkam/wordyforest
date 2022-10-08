import json


class MessageTags:
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"


class HtmxMessage:
    HEADER = "HX-Trigger"

    def info(message):
        return json.dumps(
            {
                "showMessage": {
                    "level": MessageTags.INFO,
                    "message": message,
                }
            }
        )

    def success(message):
        return json.dumps(
            {
                "showMessage": {
                    "level": MessageTags.SUCCESS,
                    "message": message,
                }
            }
        )

    def error(message):
        return json.dumps(
            {
                "showMessage": {
                    "level": MessageTags.ERROR,
                    "message": message,
                }
            }
        )
