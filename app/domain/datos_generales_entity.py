from app.domain.base_entity import BaseEntity

# class DatosGeneralesEntity(BaseEntity):
#     def __init__(
#             self,
#             identificacion:str,
#             nombres_ciudadano:str,
#             lugar_nacimiento:str,
#             fecha_nacimiento:str,
#             sexo:str,
#             domicilio:str,
#             calles:str,
#             instruccion:str,
#             condicion_ciudadano:str,
#             nacionalidad:str,
#             estado_civil:str,
#             numero_casa:str,
#             profesion:str
#             ):

#         super().__init__()
#         self.identificacion = identificacion
#         self.nombres_ciudadano = nombres_ciudadano
#         self.lugar_nacimiento = lugar_nacimiento
#         self.fecha_nacimiento = fecha_nacimiento
#         self.sexo = sexo
#         self.domicilio = domicilio
#         self.calles = calles
#         self.instruccion = instruccion
#         self.condicion_ciudadano = condicion_ciudadano
#         self.nacionalidad = nacionalidad
#         self.estado_civil = estado_civil
#         self.numero_casa = numero_casa
# #         self.profesion = profesion


class DatosGeneralesEntity(BaseEntity):
    def __init__(self,numero_cedula:str,nombres:str,nacionalidad:str,lugar_ins_nacimiento:str,disabled:bool,condicion_cedulado:str) -> None:
        self.numero_cedula = numero_cedula
        self.nombres = nombres
        self.nacionalidad = nacionalidad
        self.lugar_ins_nacimiento = lugar_ins_nacimiento
        self.disabled = disabled
        self.condicion_cedulado = condicion_cedulado    