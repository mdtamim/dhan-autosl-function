from config.dhan_init import init_dhan
from config.firebase_init import init_firebase
from services.stoploss_service import process_stoploss_placement

# When Cloud Scheduler involes cloud function it passes argument.do it is added
# in function definition
def main(request):
    dhan = init_dhan()
    db = init_firebase()
    process_stoploss_placement(dhan, db)

    return "Task completed successfully", 200

if __name__ == '__main__':
    main(None)