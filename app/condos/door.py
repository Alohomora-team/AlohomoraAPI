"Creates class Door so there's no need to save on db"
class Door:
    """Class responsible for saying if the door is open or not"""

    def __init__(self, value):
        """Inits Class Door with value"""
        self.value = value

door_instance = Door(False)
