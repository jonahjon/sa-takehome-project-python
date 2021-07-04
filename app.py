import os
import stripe

from flask import Flask, request, render_template

#Publishable Key
stripe.api_key = "sk_test_1234"

app = Flask(__name__,
  static_url_path='',
  template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "views"),
  static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))

# Home route
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# Checkout route
@app.route('/checkout', methods=['GET'])
def checkout():
  title, amount = getItem(request.values.get('item'))
  return render_template('checkout.html', title=title, amount=amount)

# Success/Charge route
@app.route('/charge', methods=['POST'])
def charge():
  title, amount = getItem(request.values.get('item'))
  name=request.values.get('name')
  metadata = {"name":name}
  charge = stripe.Charge.create(
    amount=amount,
    currency="usd",
    description=title,
    receipt_email=request.values.get('email'),
    metadata=metadata,
    source=request.values.get('stripeToken'),
  )
  return render_template(
    'success.html', 
    currency=charge.currency,
    amount=centstodollars(amount),
    description=charge.description,
    name=charge.metadata.name,
    email=charge.receipt_email,
    chargeId=charge.id,
    receipt_url=charge.receipt_url
  )

def centstodollars(cents: int) -> float:
    dollar = float(cents) / 100
    return dollar

def getItem(item: str) -> tuple[str, int]:
  title = None
  amount = None
  error = None

  if item == '1':
    title = 'The Art of Doing Science and Engineering'
    amount = 2300
  elif item == '2':
    title = 'The Making of Prince of Persia: Journals 1985-1993'
    amount = 2500
  elif item == '3':
    title = 'Working in Public: The Making and Maintenance of Open Source'
    amount = 2800
  return title, amount



if __name__ == '__main__':
  app.run(port=5000, host='0.0.0.0', debug=True)
