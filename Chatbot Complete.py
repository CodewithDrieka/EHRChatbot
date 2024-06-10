import json

class HealthRecordsChatbot:
    def __init__(self, db_file='ehr_db.json'):
        self.db_file = db_file
        self.patients_collection = self.load_database(db_file)

    def load_database(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def save_database(self):
        with open(self.db_file, 'w') as file:
            json.dump(self.patients_collection, file, indent=4)

    def greet_user(self):
        greeting_message = "Welcome to our Health Records System Chatbot! I'd be happy to assist you today!"
        print(greeting_message)

    def store_user_info(self, patient_id: str, name: str, date_of_birth: str, gender: str, contact: str, address: str):
        user_info = {
            "_id": {"$oid": ""},
            "name": name,
            "Date of Birth": date_of_birth,
            "Gender": gender,
            "Contact": contact,
            "Address": address,
            "Medical History": [],
            "Prescriptions": []
        }
        self.patients_collection[patient_id] = user_info  # Add the user info to the patients collection
        self.save_database()

    def retrieve_patient_info(self, patient_id):
        return self.patients_collection.get(patient_id)

    def calculate_bmi(self, weight: float, height: float) -> float:
        bmi = (weight / (height ** 2)) * 703
        return bmi

    def generate_bmi_response(self, weight: float, height: float) -> str:
        bmi = self.calculate_bmi(weight, height)
        response = f"Your BMI (Body Mass Index) is {bmi:.2f}. "
        if bmi < 18.5:
            response += "The patient is underweight."
        elif 18.5 <= bmi < 25:
            response += "The patient's weight is normal."
        elif 25 <= bmi < 30:
            response += "The patient is overweight."
        else:
            response += "The patient is obese."
        return response

    def suggest_weight_management(self, goal: str) -> str:
        if goal == "maintain":
            return ("To maintain your current weight, try to balance your calorie intake with your calorie expenditure. "
                    "Eat a balanced diet and engage in regular physical activity.")
        elif goal == "gain":
            return ("To gain weight, focus on consuming more calories than you burn. Consider increasing your portion sizes "
                    "and adding healthy, calorie-dense foods to your diet. Also, incorporate strength training exercises to build muscle mass.")
        elif goal == "lose":
            return ("To lose weight, aim to create a calorie deficit by consuming fewer calories than you burn. Focus on eating "
                    "a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Additionally, incorporate "
                    "regular aerobic exercise into your routine to burn calories and promote weight loss.")
        else:
            return "I'm sorry, I didn't understand your request. Please specify whether you want to maintain, gain, or lose weight."

    def assist_user(self):
        self.greet_user()
        patient_id = input("What is the patient's ID? ")

        patient_info = self.retrieve_patient_info(patient_id)
        if not patient_info:
            print(f"Patient '{patient_id}' not found. Let's create a new record.")
            name = input("What is the patient's name? ")
            date_of_birth = input("What is the patient's date of birth (YYYY-MM-DD)? ")
            gender = input("What is the patient's gender? ")
            contact = input("What is the patient's contact number? ")
            address = input("What is the patient's address? ")
            self.store_user_info(patient_id, name, date_of_birth, gender, contact, address)
        else:
            print(f"Patient '{patient_info['name']}' found.")

        while True:
            query = input("What would you like to know? (e.g., BMI, lose, maintain, gain, medical history, prescriptions) ")
            query_lower = query.lower()
            if query_lower == "bmi":
                weight = float(input("What is the patient's weight in pounds? "))
                height = float(input("What is the patient's height in inches? "))
                print(self.generate_bmi_response(weight, height))
            elif query_lower in ["lose", "maintain", "gain"]:
                print(self.suggest_weight_management(query_lower))
            elif query_lower == "medical history":
                print(patient_info.get("Medical History", "Medical history not available."))
            elif query_lower == "prescriptions":
                print(patient_info.get("Prescriptions", "Prescription information not available."))
            else:
                print("I'm sorry, I couldn't understand your request.")

            another_query = input("Would you like to know anything else? (Type 'Y' or 'N'): ")
            if another_query.lower() != 'y':
                print("Thank you for using the Health Records System Chatbot. Goodbye!")
                break

# Example usage:
chatbot = HealthRecordsChatbot()
chatbot.assist_user()













