# Function to fetch stock details from Firebase
def fetch_stock_details_from_db(db, stock_symbol):
    doc_ref = db.collection('stocks').document(stock_symbol)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None


# Function to update stock details in Firebase
def update_stock_in_db(db, stock_symbol, data):
    doc_ref = db.collection('stocks').document(stock_symbol)
    doc_ref.set(data)


# Function to delete stock details from Firebase
def delete_stock_from_db(db, stock_symbol):
    doc_ref = db.collection('stocks').document(stock_symbol)
    doc_ref.delete()