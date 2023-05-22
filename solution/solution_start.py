import csv
import json

def process_data():
    # Load customers, transactions, and products data
    customers = load_customers()
    transactions = load_transactions()
    products = load_products()

    # Create a dictionary to store the processed data
    processed_data = {}

    # Iterate over transactions
    for transaction in transactions:
        customer_id = transaction['customer_id']
        product_id = transaction['product_id']

        # Check if the customer exists in the processed data dictionary
        if customer_id not in processed_data:
            processed_data[customer_id] = {
                'customer_id': customer_id,
                'loyalty_score': customers[customer_id]['loyalty_score'],
                'purchases': {}
            }

        # Check if the product exists in the processed data dictionary
        if product_id not in processed_data[customer_id]['purchases']:
            product = products[product_id]
            processed_data[customer_id]['purchases'][product_id] = {
                'product_id': product_id,
                'product_category': product['product_category'],
                'purchase_count': 0
            }

        # Increment the purchase count for the product
        processed_data[customer_id]['purchases'][product_id]['purchase_count'] += 1

    # Convert the processed data dictionary to a list of customer records
    processed_data_list = list(processed_data.values())

    # Write the processed data to an output JSON file
    with open('output.json', 'w') as output_file:
        json.dump(processed_data_list, output_file)

def load_customers():
    customers = {}
    with open('customers.csv', 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            customers[row['customer_id']] = {
                'customer_id': row['customer_id'],
                'loyalty_score': int(row['loyalty_score'])
            }
    return customers

def load_transactions():
    transactions = []
    with open('transactions.jsonl', 'r') as transactions_file:
        for line in transactions_file:
            transaction = json.loads(line)
            transactions.append(transaction)
    return transactions

def load_products():
    products = {}
    with open('products.csv', 'r') as products_file:
        reader = csv.DictReader(products_file)
        for row in reader:
            products[row['product_id']] = {
                'product_id': row['product_id'],
                'product_category': row['product_category']
            }
    return products

if __name__ == '__main__':
    process_data()