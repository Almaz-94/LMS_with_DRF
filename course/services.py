import os

import stripe

from course.models import Payment


def create_stripe_session(obj: Payment):
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    product_title = obj.course or obj.lesson
    product = stripe.Product.create(name=product_title)
    price = stripe.Price.create(
        unit_amount=obj.sum,
        currency='usd',
        product=product.id
    )
    stripe_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': price.id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/success',
        customer_email=f'{obj.client.email}'
    )
    return stripe_session


def get_session(stripe_session_id):
    stripe.api_key = os.getenv('STRIPE_API_KEY')
    return stripe.checkout.Session.retrieve(stripe_session_id)
