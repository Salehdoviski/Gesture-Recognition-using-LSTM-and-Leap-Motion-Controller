import time
import csv
import Leap

class LeapMotionListener(Leap.Listener):
    def __init__(self):
        super(LeapMotionListener, self).__init__()

        # Define headers including gesture names
        self.headers = ['Palm_X', 'Palm_Y', 'Palm_Z',
                        'Thumb_Type', 'Thumb_X', 'Thumb_Y', 'Thumb_Z', 'Thumb_Extended',
                        'Index_Type', 'Index_X', 'Index_Y', 'Index_Z', 'Index_Extended',
                        'Middle_Type', 'Middle_X', 'Middle_Y', 'Middle_Z', 'Middle_Extended',
                        'Ring_Type', 'Ring_X', 'Ring_Y', 'Ring_Z', 'Ring_Extended',
                        'Pinky_Type', 'Pinky_X', 'Pinky_Y', 'Pinky_Z', 'Pinky_Extended',
                        'Gesture', 'Sample_Number']

        # Open the file with write mode and write the headers
        with open('leap_motion_data.csv', 'wb') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(self.headers)

        # Initialize counters for each gesture and sample number
        self.gestures = ['no', 'thanks', 'hello','boy','wrong','cat','milk']
        self.current_gesture = 'no'
        self.sample_counter = 0
        self.sample_number = 0

        # Set the desired capture rate (frames per second)
        self.capture_rate = 60

        # Set the duration for each sample in seconds
        self.sample_duration = 3

        # Calculate the total number of frames to capture for each sample
        self.total_frames = int(self.capture_rate * self.sample_duration)

        # Set the total number of samples for each gesture
        self.total_samples_per_gesture = 60

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty:
            hand = frame.hands[0]  # Assuming there is at least one hand in the frame

            # Extract finger data
            fingers_data = []
            for finger in hand.fingers:
                finger_data = [
                    finger.type,  # Finger type
                    finger.tip_position.x,
                    finger.tip_position.y,
                    finger.tip_position.z,
                    finger.is_extended  # Finger extended status
                ]
                fingers_data.extend(finger_data)

            # Extract palm data
            palm_data = [
                hand.palm_position.x,
                hand.palm_position.y,
                hand.palm_position.z
            ]

            # Update the current gesture
            gesture = self.current_gesture

            # Update the sample number for the current gesture
            self.sample_number += 1

            # Save data to CSV file without rewriting the header
            with open('leap_motion_data.csv', 'ab') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(palm_data + fingers_data + [gesture, self.sample_number])

                # Print a message for each saved sample
                print("Saved sample {} for gesture {}".format(self.sample_number, gesture))

            # Update the counter for the current gesture
            self.sample_counter += 1

            # Check if we have collected the required number of samples for the current gesture
            if self.sample_counter >= self.total_samples_per_gesture:
                # Reset the counters for the next sample
                self.sample_counter = 0
                self.sample_number = 0

                # Print a message to indicate the end of collecting samples for the current gesture
                print("Finished collecting samples for gesture: {}".format(gesture))

                # Introduce a delay between gestures (2 seconds)
                time.sleep(2)

                # Switch to the next gesture
                self.current_gesture = self.next_gesture()

    def next_gesture(self):
        # Get the next gesture in sequence
        index = self.gestures.index(self.current_gesture)
        next_index = (index + 1) % len(self.gestures)
        return self.gestures[next_index]

def main():
    # Create a Leap Motion controller and add a listener
    controller = Leap.Controller()
    listener = LeapMotionListener()
    controller.add_listener(listener)

    print("Capturing 60 samples for each gesture in sequence with a 2-second delay between gestures. Press Enter to quit...")
    try:
        raw_input()  # Use input() in Python 3.x
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
