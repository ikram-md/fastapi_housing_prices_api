from passlib.context import CryptContext

# setting the default hashing algo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def hash_password(password: str):
    """_summary_

    Args:
        password (str): _description_

    Returns:
        _type_: _description_
    """
    return pwd_context.hash(password)


def verify(password: str, hashed_password: str):
    """_summary_

    Args:
        password (str): _description_
        hashed_password (str): _description_

    Returns:
        _type_: _description_
    """
    return pwd_context.verify(password, hashed_password)
