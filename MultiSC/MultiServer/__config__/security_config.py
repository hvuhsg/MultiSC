SECURITY = True

CHECK_MESSAGE = "check"

keys_path = r"__config__/keys/"

KEY_PATH = keys_path + r"private_key.rsa"
VERIFY_PUBLIC_KEY_PATH = keys_path + r"public_verify_key.rsa"  # use on the client
SIGN_PRIVATE_KEY_PATH = keys_path + r"private_verify_key.rsa"
PUB_KEY_PATH = keys_path + r"public_key.rsa"
