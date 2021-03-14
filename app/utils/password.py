class Password:
    @staticmethod
    def gen_hash(password: str) -> str:
        if not password:
            raise Exception("Password is NULL")
        # TODO Implement hashing
        _hashed = password
        return _hashed

    def verify_password(password, hashed) -> bool:
        # TODO
        is_correct = password == hashed
        return is_correct
