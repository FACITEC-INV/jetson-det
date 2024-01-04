from peewee import *

db = SqliteDatabase('contador_mapy.db')

class Detection(Model):
    zona = IntegerField()
    clase = CharField()
    fecha = DateTimeField()
    enviado = BooleanField()

    class Meta:
        database = db 
        primary_key = False

db.connect()
db.create_tables([Detection])
