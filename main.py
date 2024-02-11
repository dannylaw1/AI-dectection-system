import json
from twilio.rest import Client
import cv2

# Twilio credentials
account_sid = 'ACOffd1d64949441e5afffbcbe60541945'
auth_token = '21e549586339b0191997e4415943dc4'
twilio_phone_number = '+12512902757'
recipient_number = '+2348144238320'
client = Client(account_sid, auth_token)

# Function to create and populate a JSON file
def create_json_file(data, filename='user_credentials.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f'The JSON file "{filename}" has been created and populated with user credentials.')

# Function to check user login
def check_login(username, password, filename='user_credentials.json'):
    with open(filename, 'r') as file:
        user_credentials = json.load(file)
    if username in user_credentials and user_credentials[username] == password:
        return True
    else:
        return False
user_credentials = {
    'vaina': 'lol1234',
    'shed': 'lol12345',
    'onuoha': 'lol123456'
}

# Call the function to create the JSON file
create_json_file(user_credentials)

# Login attempt
login_username = input('Enter your username: ')
login_password = input('Enter your password: ')

# Check the login
if check_login(login_username, login_password):
    print('Login successful!')

    # Initialize the video capture (use the appropriate camera index)
    cap = cv2.VideoCapture(0)

    # Load pre-trained person detection model (Haarcascades)
    cascade_path = 'haarcascade_fullbody.xml'
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert the frame to grayscale for better detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect persons in the frame
        bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Check if persons are detected
        if len(bodies) > 0:


            print("Person detected!")
            print("All vaults locked")

            # Send Text message using Twilio
            message = client.messages.create(
                body="A person has passed by! Lock the Vault.",
                from_=twilio_phone_number,
                to=recipient_number
            )

            print("Text message sent!")
            # Break the loop after sending the message
            break

        # Display the frame
        cv2.imshow('Frame', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

else:
    print('Login failed. Please check your username and password.')
