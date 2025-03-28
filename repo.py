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
                                    description text)""")

            self.cursor.execute("""create table if not exists drone_characteristic(
                                    id_drone_characteristics serial primary key,
                                    name text)""")
                                    
            self.cursor.execute("""create table if not exists drone_characteristics_type(
                                    id_drone_characteristics_type serial primary key,
                                    id_drone_type int references drone_type,
                                    id_drone_characteristics int references drone_characteristic,
                                    is_mandatory bool)""")

            self.cursor.execute("""create table if not exists drone_characteristic_value(
                                    id_drone_characteristics_value serial primary key,
                                    value text,
                                    id_drones int references drone,
                                    id_drone_type int references drone_type,
                                    id_characteristics int references drone_characteristic)""")
            
            self.cursor.execute("""create table if not exists picture(
                                    id serial primary key,
                                    blob text,
                                    id_drone int references drone)""")
            
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
        
    def get_characteristics_template(self, type: int) -> list[str]:
        try:
            characteristics_template = []
            sql = """select d_c.name from drone_characteristic d_c
                                join drone_characteristics_type d_c_t on d_c_t.id_drone_characteristics = d_c.id_drone_characteristics 
                                join drone_type d_t on d_c_t.id_drone_type = d_t.id_drone_type
                                where d_t.id_drone_type = %s""" %type
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for name in rows:
                 characteristics_template.append(name)
            return characteristics_template
        except Exception as e:
            raise Exception(e)

    def get_characteristics_values(self, drone_id: int) -> list[str]:
        try:
            characteristics_values = []
            sql = """select dcv.value from drone_characteristic_value dcv
                        join drone d on d.id_drone = dcv.id_drones
                        where d.id_drone = %s"""%drone_id
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            for value in rows:
                characteristics_values.append(value)
            return(characteristics_values)
        except Exception as e:
            raise Exception(e)
        pass
    
    def create_characteristics_template(self, characteristics: list, type: int):
        try:
            sql = 'insert into drone_characteristics(name) values'
            self.cursor.executemany
            pass
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
print(repo.get_characteristics_template(0))
print(repo.get_characteristics_values(0))