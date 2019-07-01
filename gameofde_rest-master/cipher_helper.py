from CaesarDecipher import decrypt


# The CaesarController calls this function in models.mainControllers.CaesarController
def decipher(cipher, lang):
    encryptedMessage = decrypt(cipher, lang)
    return encryptedMessage