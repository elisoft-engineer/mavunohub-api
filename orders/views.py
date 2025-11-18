from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import UserRole
from authentication.permissions import IsStaff

from .models import Order, OrderStatus
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderList(APIView):
    """
    Endpoint to handle both fetching all Orders and creating a new Order.
    """

    allowed_methods = ['GET', 'POST']
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get(self, request):
        """
        Get the Order list
        """
        orders = []
        if request.user.role == UserRole.FARMER:
            orders = Order.objects.filter(items__seller=request.user).distinct()
        else:
            orders = request.user.orders.all()
        serializer = self.get_serializer_class()(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new Order
        """
        serializer = self.get_serializer_class()(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderDetail(APIView):
    """
    Retrieve or update a Order.
    """

    allowed_methods = ['GET', 'PATCH']

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsStaff()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderSerializer
        return None

    def get_object(self, pk):
        obj = get_object_or_404(Order, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        """
        Get an Order's details
        """
        order = self.get_object(pk)
        serializer = self.get_serializer_class()(order)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Update an Order
        """
        order = self.get_object(pk)
        error_message = ""
        match order.status:
            case OrderStatus.PENDING:
                error_message = "Order is still pending"
            case OrderStatus.CONFIRMED:
                order.status = OrderStatus.PACKED
            case OrderStatus.PACKED:
                order.status = OrderStatus.SHIPPED
            case OrderStatus.SHIPPED:
                order.status = OrderStatus.COMPLETED
            case OrderStatus.CANCELLED:
                error_message = "Order is already cancelled"
            case _:
                pass
        order.save()

        if len(error_message) > 0:
            return Response({"detail": error_message}, status.HTTP_400_BAD_REQUEST)
        return Response({"detail": f"Order status set to {order.status.value}"}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Delete a Order
        """
        order = self.get_object(pk)
        order.delete()
        return Response({"detail": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
