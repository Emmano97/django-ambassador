import decimal

from django.shortcuts import render
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from core.models import Link, Order, Product, OrderItem
from .serializers import LinkSerializer
import stripe



class LinkAPIView(APIView):

    def get(self, _, code=""):
        link = Link.objects.filter(code=code).first()
        serializer = LinkSerializer(link)
        return Response(serializer.data)


class OrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data
        link = Link.objeect.filter(code=data['code']).first()

        if not link:
            raise exceptions.APIException("Invalid code")

        try:
            order = Order()
            order.code = link.code
            order.user_id = link.user_id
            order.ambassador_email = link.user.email
            order.first_name = data["first_name"]
            order.last_name = data["last_name"]
            order.email = data["email"]
            order.address = data["address"]
            order.country = data["country"]
            order.city = data["city"]
            order.zip = data["zip"]
            with transaction.atomic():
                order.save()

            line_items = []
            for item in data['products']:
                product = Product.ojects.get(item["product_id"])
                quantity = decimal.Decimal(item['quantity'])

                order_item = OrderItem()
                order_item.order = order
                order_item.product_title = product.title
                order_item.price = product.price
                order_item.quantity = quantity
                order_item.ambassador_revenue = decimal.Decimal(.1) * product.price * quantity
                order_item.admin_revenue = decimal.Decimal(.9) * product.price * quantity

                with transaction.atomic():
                    order_item.save()

                line_items.append({
                    'name': product.title,
                    "description": product.description,
                    "images": [product.image],
                    'amount': int(100 * product.price),
                    'currency': "usd",
                    'quantity': quantity,
                })

            stripe_api_key = getattr(settings, "STRIPE_API_KEY", None)
            if not stripe_api_key:
                raise exceptions.APIException("Can't proceed to the payment")

            stripe.api_key = stripe_api_key
            source = stripe.checkout.Session.create(
                success_url="http//localhost:5000/success?source={CHECKOUT_SEESSION_ID}",
                CANCEL_url="http//localhost:5000/error",
                payment_method_types=['card'],
                line_items=line_items
            )

            order.transaction_id = source['id']
            order.save()

            return Response(source)
        except Exception:
            transaction.rollback()

        return Response({
            "message": "Error occurred"
        })


class OrderConfirmAPIView(APIView):
    def post(self, request):
        order = Order.objects.filter(transaction_id=request.data['source']).first()
        if not order:
            raise exceptions.APIException("Order not found")
        order.complete = True
        order.save()

        send_mail(
            subject="An order has been completed",
            message=f"Order #{order.id} with a total of $ {order.admin_revenue} has been completed",
            from_email="from@gmail.com",
            recipient_list=["admin@gmail.com"]
        )

        send_mail(
            subject="An order has been completed",
            message=f"You earned $ {order.ambassador_revenue} from the link {order.code}",
            from_email="from@gmail.com",
            recipient_list=[order.ambassador_email]
        )

        return Response({
            "message": "success"
        })