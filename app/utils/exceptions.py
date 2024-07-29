class GroupNotFound(Exception):
    def __init__(self, group:str = ""):
        self.group = group
        self.message = f'Группа не найдена в JSON файле: "{group}"'
        super().__init__(self.message)

class PrepNotFound(Exception):
    def __init__(self, prep:str = ""):
        self.prep = prep
        self.message = f'Преподаватель не найден в JSON файле: "{prep}"'
        super().__init__(self.message)

class SubjNotFound(Exception):
    def __init__(self, subj:str = ""):
        self.subj = subj
        self.message = f'Предмет не найден в JSON файле: "{subj}"'
        super().__init__(self.message)

class WeekdayNotFound(Exception):
    def __init__(self, wkday:str = ""):
        self.wkday = wkday
        self.message = f'День недели не найден в JSON файле: "{wkday}"'
        super().__init__(self.message)