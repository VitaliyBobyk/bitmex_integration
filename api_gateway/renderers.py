from rest_framework.renderers import JSONRenderer


class CustomJsonRender(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            request = renderer_context['request']
            response = renderer_context['response']
            if 'account' not in request.path:
                if 'account' not in request.headers:
                    response.status_code = 400
                    res = {
                        'missing': '"account" header'
                    }
                    return super().render(res, accepted_media_type, renderer_context)
            return super().render(data, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)