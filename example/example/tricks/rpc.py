from djangorpc import RpcRouter, Error, Msg, RpcHttpResponse
from djangorpc.decorators import add_request_to_kwargs, login_required
from djangorpc.exceptions import RpcExceptionEvent


class TricksApiClass(object):

    def func1(self, user, request):
        return Msg('func1')


class TricksOneApiClass(object):

    def func2(self, val, **kwargs):
        return Msg('func2')


class TricksTwoApiClass(object):

    def func3(self, user, request):
        return Msg('func3')

    def _extra_kwargs(self, request, *args, **kwargs):
        return {
            'request': request,
            'user': request.user
        }


def extra_kwargs(request, *args, **kwargs):
    return {
        'request': request,
        'user': request.user
    }


class TricksThreeApiClass(object):

    def func4(self, user, request):
        return Msg('func4')

    func4._extra_kwargs = extra_kwargs

    @add_request_to_kwargs
    def func5(self, user, request):
        return Msg('func5')

    def func6(self, user):
        if not user.is_authenticated():
            raise RpcExceptionEvent('Login please!')

    @login_required
    def func7(self, user):
        pass

    def set_cookie(self, user):
        response = RpcHttpResponse({'msg': 'Hello!'})
        response.set_cookie('rpccookie', '123456')
        return response


class CustomRouter(RpcRouter):

    def extra_kwargs(self, request, *args, **kwargs):
        return {
            'request': request,
            'user': request.user
        }


custom_router = CustomRouter(
    {
        'TricksApi': TricksApiClass(),
        'TricksOneApi': TricksOneApiClass()
    },
    url_namespace='tricks:custom_rpc')

custom_router_one = RpcRouter(
    {
        'TricksTwoApi': TricksTwoApiClass(),
        'TricksThreeApi': TricksThreeApiClass()
    },
    url_namespace='tricks:custom_rpc_one')
