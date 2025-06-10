import sqlite3
import base64
from droneDTO import DroneDTO


class Repository:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_db(self):
        try:
            self.cursor.execute("""create table if not exists drone_type(
                                            id_drone_type serial primary key,
                                            name text)""")

            self.cursor.execute("""create table if not exists drone(
                                    id_drone serial primary key,
                                    name text,
                                    id_drone_type int references drone_type,
                                    description text,
                                    pictures text)""")

            self.cursor.execute("""create table if not exists drone_characteristic(
                                    id_drone_characteristic serial primary key,
                                    name text)""")
                                    
            self.cursor.execute("""create table if not exists drone_characteristic_type(
                                    id_drone_characteristic_type serial primary key,
                                    id_drone_type int references drone_type,
                                    id_drone_characteristic int references drone_characteristic,
                                    is_mandatory bool)""")

            self.cursor.execute("""create table if not exists drone_characteristic_value(
                                    id_drone_characteristic_value serial primary key,
                                    value text,
                                    id_drones int references drone,
                                    id_drone_type int references drone_type,
                                    id_characteristic int references drone_characteristic)""")
            
            self.cursor.execute("""create table if not exists picture(
                                    id_picture serial primary key,
                                    blob text)""")
            
            self.cursor.execute("""insert into drone_type(name) values('Мультироторного типа(стабилизированные)'),
                                ('Мультироторного типа(FPV)'),
                                ('Самолетного типа'),
                                ('Летающее крыло')""")

            self.conn.commit()
        except Exception as e:
             raise Exception(e)
        
    def get_drone_types(self) -> list[str]:
        try:
            self.cursor.execute("""select name from drone_type""")
            rows = self.cursor.fetchall()
            result = []
            for type in rows:
                 result.append(type)
            return result
        except Exception as e:
            raise Exception(e)
        
    def get_characteristic_template(self, type: int) -> list[str]:
        try:
            characteristic_template = []
            sql = """select d_c.name from drone_characteristic d_c
                                join drone_characteristic_type d_c_t on d_c_t.id_drone_characteristic = d_c.id_drone_characteristic 
                                join drone_type d_t on d_c_t.id_drone_type = d_t.id_drone_type
                                where d_t.id_drone_type = %s""" %type
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for name in rows:
                 characteristic_template.append(name)
            return characteristic_template
        except Exception as e:
            raise Exception(e)

    def get_characteristic_values(self, drone_id: int) -> list[str]:
        try:
            characteristic_values = []
            sql = """select dcv.value from drone_characteristic_value dcv
                        join drone d on d.id_drone = dcv.id_drones
                        where d.id_drone = %s"""%drone_id
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for value in rows:
                characteristic_values.append(value)
            return(characteristic_values)
        except Exception as e:
            raise Exception(e)
    
    def create_type(self, characteristic: list, type_name: str):
        try:
            id_characteristic = []
            sql = 'insert into drone_type(name) values(\'%s\')'%type_name
            self.cursor.execute(sql)
            self.conn.commit()
            sql = 'select id_drone_type from drone_type where name = \'%s\''%type_name
            self.cursor.execute(sql)
            type = self.cursor.fetchone()
            for x in characteristic:
                sql = 'insert into drone_characteristic(name) values (\'%s\')'%x
                self.cursor.execute(sql)
                self.conn.commit()
                sql = 'select id_drone_characteristic from drone_characteristic where name like \'%s\''%x
                self.cursor.execute(sql)
                id_characteristic.append(self.cursor.fetchone())
            for x in id_characteristic:
                sql = 'insert into drone_characteristic_type(id_drone_type, id_drone_characteristic) values(\'%s\'),(\'%s\')'%type%x
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            raise Exception(e)

    def create_drone(self, drone: DroneDTO):
        try:
            pass
        except Exception as e:
            raise Exception(e)
        pass
#----------------------------------------------------------------
repo = Repository('C:\\Users\\user\\Documents\\data.db')
print(repo.get_drone_types())
print(repo.get_characteristic_template(0))
print(repo.get_characteristic_values(0))
repo.create_type(['хуета1'], 'хуета2')
print(print(repo.get_characteristic_template(3)))