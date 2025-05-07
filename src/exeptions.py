from http.client import HTTPException


class EntityNotFoundException(Exception):
    def __init__(self, entity_name: str):
        self.entity_name = entity_name
        super().__init__(f"{entity_name} не найден")


class InvalidPasswordException(Exception):
    def __init__(self, email_value: str):
        super().__init__('Неверные учётные данные для входа в систему')


class ProfileAlreadyExistsException(Exception):
    def __init__(self, email_value: str):
        super().__init__('Профиль для данного аккаунта уже существует')


class UserEmailAlreadyRegisteredException(Exception):
    def __init__(self, email_value: str):
        super().__init__('Пользователь с таким email уже зарегистрирован')
        
    
class UnknownException(Exception):
    def __init__(self):
        super().__init__('Неизвестная ошибка')


        
    

