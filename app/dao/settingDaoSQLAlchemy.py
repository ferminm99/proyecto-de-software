from app.models.setting import Setting
from app.db import db

class SettingDao:

    @classmethod
    def getByType(cls, type):
        """Devuelte el Setting de acuerdo al tipo 

        Args:
            type (string): tipo de configuracion

        Returns:
            Setting: El primero que cumple con la condicion
        """
        return Setting.query.filter_by(type=type).first()
    
    @classmethod
    def getAll(cls):
        """Retorna todas las configuraciones

        Returns:
            List: listado de configuraciones
        """
        return Setting.query.all()