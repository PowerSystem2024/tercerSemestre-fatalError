class NumerosIgualesEx (Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.message = mensaje