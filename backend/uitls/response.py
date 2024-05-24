from django.http import JsonResponse


class Response:
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    @staticmethod
    def ok(data, status=200):
        return JsonResponse({"code": "success", "data": convert_dict_keys_to_camel_case(data)}, status=status)

    @staticmethod
    def fail(msg, status=400):
        return JsonResponse({"code": "fail", "data": {"code": 0, "msg": msg}}, status=status)


def convert_dict_keys_to_camel_case(d):
    return {snake_to_camel(k): v if not isinstance(v, dict) else convert_dict_keys_to_camel_case(v) for k, v in
            d.items()}


def convert_array_keys_to_camel_case(arr):
    return [convert_dict_keys_to_camel_case(i) for i in arr]


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
