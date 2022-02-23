import requests
import pandas as pd

def main():
    response = requests.get('http://localhost:8000/products')
    products = response.json()
    
    headers = list(products[0].keys())
    rows = []
    for i in products:
        tup = tuple(i.values())
        rows.append(tup)
    
    df = pd.DataFrame(rows, columns=headers)
    
    df.to_csv('./assortment.csv', index=False)
    
main()