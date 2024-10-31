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
    print(f"Total quantity for the Stock in Dhan is 0. Deleting it from database")
    doc_ref = db.collection('stocks').document(stock_symbol)
    doc_ref.delete()


def get_blocklist_stocks(db):
    # Reference to the blocklist collection in Firestore
    blocklist_ref = db.collection('stock_blocklist')
    blocklist_stocks = []

    # Fetch all documents in the blocklist collection
    docs = blocklist_ref.stream()

    for doc in docs:
        # Assuming the document ID is the stock symbol
        blocklist_stocks.append(doc.id)

    return blocklist_stocks