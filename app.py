# Flask backend server 
# Create a Checkout Session in setup mode
# Serve success and cancel pages

import os
import stripe
from dotenv import load_dotenv
from flask import Flask, redirect, request, render_template

# Load env vars
load_dotenv()

app = Flask(__name__)

# Stripe keys
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
DOMAIN = os.getenv('DOMAIN')

@app.route('/', methods=['GET'])
def home():
    return '<h1>Reserve Your Spot!</h1><a href="/create-checkout-session">Save Your Spot</a>'

@app.route('/create-checkout-session', methods=['GET'])
def create_checkout_session():
    # Optionally, create customer dynamically here
    customer = stripe.Customer.create()

    # Create Checkout Session in SETUP mode
    checkout_session = stripe.checkout.Session.create(
        customer=customer.id,
        payment_method_types=['card'],
        mode='setup',
        success_url=DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=DOMAIN + '/cancel',
    )
    return redirect(checkout_session.url, code=303)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(port=4242)
