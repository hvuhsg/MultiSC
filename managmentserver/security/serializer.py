import json


class de_serializer:
    def de_json(self, request) -> dict:
        try:
            dict_request = json.loads(s=request)
        except json.decoder.JSONDecodeError:
            dict_request = request
        return dict_request

    def __call__(self, data):
        return self.de_json(data)


class serializer:
    def to_json(self, request) -> json:
        json_obj = json.dumps(request).encode()
        return json_obj

    def __call__(self, data):
        return self.to_json(data)
