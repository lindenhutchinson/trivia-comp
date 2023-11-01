import requests

def check_param_for_none(param):
    if param == 'any':
        return None
    return param

class OpenTriviaAPI:
    BASE_URL = "https://opentdb.com/api.php"

    def __init__(self):
        self.session_token = None

    def fetch_questions(self, num_questions, category, difficulty, question_type):
        
        category = check_param_for_none(category)
        difficulty = check_param_for_none(difficulty)
        question_type = check_param_for_none(question_type)
        
        params = {
            "amount": num_questions,
            **({'category': category} if category is not None else {}),
            **({'difficulty': difficulty} if difficulty is not None else {}),
            **({'type': question_type} if question_type is not None else {}),
            "token": self.session_token,
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        response_code = data.get("response_code", 0)

        if response_code == 0:
            return data.get("results", [])
        elif response_code == 1:
            raise Exception("API doesn't have enough questions for your query.")
        elif response_code == 2:
            
            raise Exception(f"Invalid parameter: Arguments passed in aren't valid. - {params}")
        elif response_code == 3:
            raise Exception("Session Token does not exist.")
        elif response_code == 4:
            raise Exception(
                "Session Token has returned all possible questions for the specified query. Reset the Token."
            )

    def retrieve_session_token(self):
        response = requests.get(f"{self.BASE_URL}?command=request")
        data = response.json()

        self.session_token = data.get("token", None)
        return self.session_token

    def reset_session_token(self):
        if self.session_token:
            requests.get(f"{self.BASE_URL}?command=reset&token={self.session_token}")
            self.session_token = None