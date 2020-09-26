from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random

app = Flask(__name__)
database = {}
with open('customers.json') as fp:
    database = json.load(fp)


@app.route('/customers')
def show_customers():
    return render_template('customers.template.html', all_customers=database)


@app.route('/customers/add')
def show_add_customer():
    return render_template('add_customer.template.html')


@app.route('/customers/add', methods=["POST"])
def process_add_customer():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    if 'can_send' in request.form:
        can_send = True
    else:
        can_send = False

    database.append({
        'id': random.randint(10000, 99999),
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'send_marketing_material': can_send
    })

    with open('customers.json', 'w') as fp:
        json.dump(database, fp)

    return redirect(url_for('show_customers'))


@app.route('/customers/<int:customer_id>/edit')
def show_edit_customer(customer_id):
    # find the customer to edit
    customer_to_edit = None
    for customer in database:
        if customer["id"] == customer_id:
            customer_to_edit = customer

    # if the customer with the required id exists
    if customer_to_edit:
        return render_template('edit_customer.template.html',
                               customer=customer_to_edit)
    else:
        return f"Customer with id {customer_id} is not found"


@app.route('/customers/<int:customer_id>/edit', methods=["POST"])
def process_edit_customer(customer_id):
    # find the customer to edit
    customer_to_edit = None
    for customer in database:
        if customer["id"] == customer_id:
            customer_to_edit = customer

    # if the customer with the required id exists
    if customer_to_edit:

        # update the customer record
        customer_to_edit['first_name'] = request.form.get('first_name')
        customer_to_edit['last_name'] = request.form.get('last_name')
        customer_to_edit['email'] = request.form.get('email')
        if 'can_send' in request.form:
            customer_to_edit['send_marketing_material'] = True
        else:
            customer_to_edit['send_marketing_material'] = False

        # save back to the json file
        with open('customers.json', 'w') as fp:
            json.dump(database, fp)

        return redirect(url_for('show_customers'))
    else:
        return f"Customer with id {customer_id} is not found"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
