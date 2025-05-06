from utils.token_utils import generate_signed_feedback_url

# Pick an encounter ID you know exists in your DB
url = generate_signed_feedback_url("e1001")
print("Test feedback link:", url)
