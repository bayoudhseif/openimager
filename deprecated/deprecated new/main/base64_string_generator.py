import base64

# Encode balance.png
with open("source/images/balance.png", "rb") as img_file:
    balance_encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

# Print the encoded strings
print("Encoded string for balance.png:")
print(balance_encoded_string)
