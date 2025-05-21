class User:
    def __init__(self, user_id, username, role):
        self.__user_id = user_id
        self.username = username  
        self.__role = role

    @property
    def user_id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if not value:
            raise ValueError("Username tidak boleh kosong")
        if len(value) < 3:
            raise ValueError("Username minimal 3 karakter")
        self.__username = value

    @property
    def role(self):
        return self.__role

    def get_info(self):
        return f"{self.username} ({self.role})"


class Admin(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "admin")

    def manage_system(self):
        return "Mengatur sistem."


class SiswaBiasa(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "siswa_biasa")

    def akses_fitur(self):
        return "Akses terbatas."


class SiswaSuper(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "siswa_super")

    def akses_fitur(self):
        return "Akses penuh."
