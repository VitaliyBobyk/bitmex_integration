from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.core.exceptions import ObjectDoesNotExist


from . import api_descriptions

from api_gateway.services import BitmexClient
from api_gateway.models import Account, Order
from api_gateway.renderers import CustomJsonRender
from api_gateway.serializers import AccountSerializer, OrderSerializer, OrderDetailSerializer


@api_view(('GET',))
def hello_world(request):
    """
    Hello world view
    """
    return Response({"hello": "world"}, status.HTTP_200_OK)


class AccountCreateVIew(APIView):

    @swagger_auto_schema(
        request_body=AccountSerializer,
        responses={
            status.HTTP_200_OK: api_descriptions.BOOL_RESPONSE,
            status.HTTP_400_BAD_REQUEST: api_descriptions.BAD_SERIALIZER_VALIDATION_RESPONSES
        }
    )
    def post(self, request):
        """
            Create new account
        """
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersView(APIView):
    renderer_classes = (CustomJsonRender,)

    @swagger_auto_schema(
        manual_parameters=[api_descriptions.ACCOUNT_PARAMETER],
        responses={
            200: OrderSerializer(many=True)
        }
    )
    def get(self, request):
        """
        Get all Orders for current user
        """
        try:
            account = Account.objects.get(name=request.headers.get('account'))
            orders = Order.objects.filter(account=account)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        manual_parameters=[api_descriptions.ACCOUNT_PARAMETER],
        responses={
            status.HTTP_200_OK: api_descriptions.BOOL_RESPONSE,
            status.HTTP_400_BAD_REQUEST: api_descriptions.BAD_SERIALIZER_VALIDATION_RESPONSES

        }
    )
    def post(self, request):
        """
        Create new order
        """
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            account = Account.objects.get(name=request.headers.get('account'))
            serializer.save(account=account)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    renderer_classes = (CustomJsonRender,)

    @swagger_auto_schema(
        manual_parameters=[api_descriptions.ACCOUNT_PARAMETER],
        responses={
            status.HTTP_200_OK: OrderDetailSerializer(many=False),
            status.HTTP_400_BAD_REQUEST: api_descriptions.BOOL_RESPONSE
        }
    )
    def get(self, request, pk):
        """
        Get order by order id
        """
        try:
            account = request.headers.get('account')
            order = Order.objects.get(account=account, order_id=pk)
            serializer = OrderDetailSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[api_descriptions.ACCOUNT_PARAMETER],
        responses={
            status.HTTP_200_OK: api_descriptions.BOOL_RESPONSE,
            status.HTTP_400_BAD_REQUEST: api_descriptions.BOOL_RESPONSE
        }
    )
    def delete(self, request, pk):
        """
        Delete order by order id
        """
        try:
            account = request.headers.get('account')
            order = Order.objects.get(account=account, order_id=pk)
            bitmex = BitmexClient(
                order.account.api_key,
                order.account.api_secret,
            )
            bitmex.delete_order(order_id=str(order.order_id))
            order.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

