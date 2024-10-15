from config.dhan_init import init_dhan
from config.firebase_init import init_firebase
from services.stoploss_service import process_stoploss_placement

def main():
    dhan = init_dhan()
    db = init_firebase()
    process_stoploss_placement(dhan, db)

if __name__ == '__main__':
    main()