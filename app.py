import os
import stripe

from flask import Flask, request, render_template

#Publishable Key
stripe.api_key = "sk_test_123456"

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
  email=request.values.get('email')
  address=request.values.get('address')
  city=request.values.get('city')
  state=request.values.get('state')
  postal_code=request.values.get('postal_code')
  country=request.values.get('country')
  shipping={
    "address":{
      "city": city,
      "country": country,
      "line1": address,
      "postal_code": postal_code,
      "state": state
    },
    "name":name
  }
  fomatted_address=f'{address}, {city}, {state}, {postal_code}, {country}'
  metadata = {"name":name}
  charge = stripe.Charge.create(
    amount=amount,
    currency="usd",
    description=title,
    shipping=shipping,
    receipt_email=email,
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
    address=fomatted_address,
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
