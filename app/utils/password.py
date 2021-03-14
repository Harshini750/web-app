from extensions import bcrypt
class Password:
    @staticmethod
    def gen_hash(password: str) -> str:
        if not password:
            raise Exception("Password is NULL")
        _hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        return _hashed

    def verify_password(password, hashed) -> bool:
        is_correct = bcrypt.check_password_hash(hashed, password)
        return is_correct
