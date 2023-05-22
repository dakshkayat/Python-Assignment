import csv
import json
import glob
import os
from typing import List, Dict


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
        basket = transaction['basket']

        # Check if the customer exists in the processed data dictionary
        if customer_id not in processed_data:
            processed_data[customer_id] = {
                'customer_id': customer_id,
                'loyalty_score': customers[customer_id]['loyalty_score'],
                'purchases': {}
            }

        # Iterate over the products in the basket
        for product in basket:
            product_id = product['product_id']

            # Check if the product exists in the processed data dictionary
            if product_id not in processed_data[customer_id]['purchases']:
                product_category = products[product_id]['product_category']
                processed_data[customer_id]['purchases'][product_id] = {
                    'product_id': product_id,
                    'product_category': product_category,
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
    with open(r'C:\Users\91639\OneDrive\Desktop\Revolve solution\Revolve  Python\python-assignment\input_data\starter\customers.csv', 'r') as customers_file:
        reader = csv.DictReader(customers_file)
        for row in reader:
            customers[row['customer_id']] = {
                'customer_id': row['customer_id'],
                'loyalty_score': int(row['loyalty_score'])
            }
    return customers


def load_transactions() -> List[Dict[str, str]]:
    transactions = []
    folder_path = 'C:/Users/91639/OneDrive/Desktop/Revolve solution/Revolve  Python/python-assignment/input_data/starter/transactions/'

    # Iterate over monthly folders
    for month_folder in os.listdir(folder_path):
        month_folder_path = os.path.join(folder_path, month_folder)

        # Check if it's a directory
        if os.path.isdir(month_folder_path):
            json_file_path = os.path.join(month_folder_path, 'transactions.json')

            # Check if the JSON file exists
            if os.path.isfile(json_file_path):
                with open(json_file_path, 'r') as transactions_file:
                    for line in transactions_file:
                        transaction = json.loads(line)
                        transactions.append(transaction)

    return transactions


def load_products():
    products = {}
    with open(r"C:\Users\91639\OneDrive\Desktop\Revolve solution\Revolve  Python\python-assignment\input_data\starter\products.csv", 'r') as products_file:
        reader = csv.DictReader(products_file)
        for row in reader:
            products[row['product_id']] = {
                'product_id': row['product_id'],
                'product_category': row['product_category']
            }
    return products

if __name__ == '__main__':
    process_data()