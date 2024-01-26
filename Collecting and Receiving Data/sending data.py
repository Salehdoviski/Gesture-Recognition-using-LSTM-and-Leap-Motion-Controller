import time
import csv
import Leap
import threading
import os

class LeapMotionListener(Leap.Listener):
    headers = ['Palm_X', 'Palm_Y', 'Palm_Z',
               'Thumb_Type', 'Thumb_X', 'Thumb_Y', 'Thumb_Z', 'Thumb_Extended',
               'Index_Type', 'Index_X', 'Index_Y', 'Index_Z', 'Index_Extended',
               'Middle_Type', 'Middle_X', 'Middle_Y', 'Middle_Z', 'Middle_Extended',
               'Ring_Type', 'Ring_X', 'Ring_Y', 'Ring_Z', 'Ring_Extended',
               'Pinky_Type', 'Pinky_X', 'Pinky_Y', 'Pinky_Z', 'Pinky_Extended',
               'Gesture', 'Sample_Number']

    def __init__(self, csv_filename):
        super(LeapMotionListener, self).__init__()
        self.csv_filename = csv_filename
        self.counter = 0
        with open(self.csv_filename, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(self.headers)

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty and self.counter < 60:
            hand = frame.hands[0]
            fingers_data = []
            for finger in hand.fingers:
                finger_data = [
                    finger.type,
                    finger.tip_position.x,
                    finger.tip_position.y,
                    finger.tip_position.z,
                    finger.is_extended
                ]
                fingers_data.extend(finger_data)

            palm_data = [
                hand.palm_position.x,
                hand.palm_position.y,
                hand.palm_position.z
            ]

            gesture = 'unknown'
            with open(self.csv_filename, 'ab') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(palm_data + fingers_data + [gesture, self.counter])

            self.counter += 1

            if self.counter == 60:
                time.sleep(5)
                self.counter = 0

def read_csv(csv_filename):
    last_processed_line = 0
    while True:
        with open(csv_filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            all_rows = list(reader)
            total_rows = len(all_rows)

            # Process in chunks of 60, if available
            while last_processed_line + 60 <= total_rows:
                chunk = all_rows[last_processed_line:last_processed_line+60]
                process_chunk(chunk)
                last_processed_line += 60

        time.sleep(2)

def process_chunk(chunk):
    # Process the chunk of 60 rows
    print("Processing chunk")

if __name__ == "__main__":
    csv_filename = 'data_to_send4.csv'

    if os.path.exists(csv_filename):
        os.remove(csv_filename)

    controller = Leap.Controller()
    listener = LeapMotionListener(csv_filename)
    controller.add_listener(listener)

    read_thread = threading.Thread(target=read_csv, args=(csv_filename,))
    read_thread.start()

    print("Capturing live data. Press Enter to quit...")
    try:
        raw_input()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)
        read_thread.join()
