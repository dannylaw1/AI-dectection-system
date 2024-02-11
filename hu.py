import json
import hashlib
import cv2

print("Hello Welcome To TrueSight")
print("To Create an Admin press 1")
print("If you already Have an account press 2")
Login_opp = int(input('....'))

if Login_opp == 1:
    # Function to create a JSON file with initial empty user data
    def create_user_data(filename='user_data.json'):
        data = {}
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f'The JSON file "{filename}" has been created.')

    # Function to register a new user
    def register(username, password, filename='user_data.json'):
        with open(filename, 'r') as file:
            user_data = json.load(file)

        # Check if the username already exists
        if username in user_data:
            print('Username already exists. Please choose another username.')
        else:
            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Store username and hashed password
            user_data[username] = hashed_password

            # Save updated user data to the JSON file
            with open(filename, 'w') as file:
                json.dump(user_data, file, indent=4)
            print('Registration successful.')

    # Create initial user data file
    create_user_data()

    # Test registration and login
    register(input("Enter a username:"), input("\nCreate a new password:"))

if Login_opp == 2:
    # Function to check user login
    def login(username, password, filename='user_data.json'):
        with open(filename, 'r') as file:
            user_data = json.load(file)

        # Check if the username exists
        if username in user_data:
            # Hash the entered password and compare with the stored hashed password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user_data[username] == hashed_password:
                print('Login successful.')

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

                        # Break the loop after detection
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
                print('Invalid password. Please try again.')
        else:
            print('Username does not exist.')

    login(input("Enter your username:"), input("\nInput existing username password:"))
