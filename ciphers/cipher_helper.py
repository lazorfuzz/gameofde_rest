from ciphers.CaesarDecipher import decrypt


# The CaesarController calls this function in controllers.mainControllers.CaesarController
def decipher(cipher, lang):
    encryptedMessage = decrypt(cipher, lang)
    return encryptedMessage