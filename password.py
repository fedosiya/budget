import bcrypt


class Password:

    def __init__(self):
        self.__hashed_password = None

    def set_password(self, raw_password):
        self.__hashed_password = self.__encrypt_password(raw_password)

    def get_hashed_password(self) -> bytes:
        return self.__hashed_password

    def check_password(self, pass_raw: bytes, pass_hashed: bytes):
        if bcrypt.checkpw(pass_raw, pass_hashed):
            return True
        else:
            return False

    def __encrypt_password(self, value_to_encrypt):
        hashed_password = bcrypt.hashpw(bytes(value_to_encrypt, 'utf-8'), bcrypt.gensalt())
        return hashed_password