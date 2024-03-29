import threading
import time
from connection import initialize_firebase
from system_info import get_system_information
from usb_check import is_usb_plugged_in
from scan import update_scan_status
from file_count import countfiles

def update_usb_status(db_instance):
    while True:
        usb_status = is_usb_plugged_in()
        db_instance.child('usb_status').set(usb_status)
        time.sleep(1)

def main():
    # Step 1: Call Connection.py
    db_instance = initialize_firebase()

    # Step 2: Update USB Status to Firebase Realtime Database
    t1 = threading.Thread(target=update_usb_status, args=(db_instance,))
    t1.start()

    # Step 3: Update system information to Firebase Realtime Database
    system_info = get_system_information()

    # Update File Count
    file_count = countfiles()

    # Update system information to Firebase Realtime Database
    db_instance.child('system_info').set(system_info)
    db_instance.child('totalFile').set(file_count)

    # Step 4: Call Scan
    # Add your scan code here
    usb_status = is_usb_plugged_in()
    if usb_status['status'] == 'true':
        update_scan_status(db_instance)
    else:
        print("Please Plug In Usb")

    # Main thread waits for the update_usb_status thread to finish
    t1.join()

    # Done

if __name__ == "__main__":
    main()
