class DatosGeneralesFactPresenters:

    def __init__(self,numero_cedula:str,nombres:str,nacionalidad:str,lugar_ins_nacimiento:str,disabled:str,condicion_cedulado:str)-> None:
        self.numero_cedula = numero_cedula
        self.nacionalidad = nacionalidad
        self.nombres = nombres
        self.lugar_ins_nacimiento = lugar_ins_nacimiento
        self.disabled = disabled
        self.condicion_cedulado = condicion_cedulado    
        