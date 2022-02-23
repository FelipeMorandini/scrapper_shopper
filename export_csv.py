import requests
import csv
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
    
    '''
    f = open('./assortment.csv', 'w', newline="")
    writer = csv.writer(f)
    writer.writerow(headers)
    for i in range(len(rows)):
        writer.writerow(rows[i])
    f.close()
    '''
    
main()