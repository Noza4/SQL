from db import c

"""
PK - Primary Key
"""


class Employee(object):
    def __init__(self, name, surname, age, pk=None):
        self.id = pk
        self.name = name
        self.surname = surname
        self.age = age

    @classmethod
    def get(cls, pk):
        result = c.execute("SELECT * FROM employee WHERE id = ?", (pk,))
        values = result.fetchone()
        if values is None:
            return None
        employee = Employee(values["name"], values["surname"], values["age"], values["id"])
        return employee

    @classmethod
    def get_ls(cls, **kwargs):
        employee_ls = []
        conditions = []
        values = []

        for key, value in kwargs.items():
            conditions.append(f"{key} = ?")
            values.append(value)

        condition_str = " AND ".join(conditions)
        sql_query = f"SELECT * FROM employee WHERE {condition_str}"

        result = c.execute(sql_query, tuple(values))
        for row in result.fetchall():
            employee_ls.append(dict(row))

        return employee_ls

    def __repr__(self):
        return "<Employee {}>".format(self.name)

    def update(self):
        c.execute("UPDATE employee SET name = ?, surname = ?, age = ? WHERE id = ?",
                  (self.name, self.surname, self.age, self.id))

    def create(self):
        c.execute("INSERT INTO employee (name, surname, age) VALUES (?, ?, ?)", (self.name, self.surname, self.age))
        self.id = c.lastrowid

    @staticmethod
    def rec_delete(rec_id):
        c.execute("DELETE FROM employee WHERE id = ?", (rec_id,))

    def __gt__(self, other):
        if self.age > other.age:
            return f"{self.name} {self.surname} {self.age}"
        else:
            return f"{other.name} {other.surname} {other.age}"

    def __eq__(self, other):
        if self.age == other.age:
            return "They Hava The Same Age"

    def save(self):
        if self.id is not None:
            self.update()
        else:
            self.create()
        return self
