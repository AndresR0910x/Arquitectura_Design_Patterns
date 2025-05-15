from abc import ABC, abstractmethod
from datetime import date
from typing import List
import copy

# Interface for Prototype pattern
class Prototype(ABC):
    @abstractmethod
    def clone(self) -> 'DocumentoTransaccion':
        pass

# Paciente class
class Paciente:
    def __init__(self, id: int, nombre: str, historial: str):
        self.id = id
        self.nombre = nombre
        self.historial = historial

# Abstract base class for DocumentoTransaccion
class DocumentoTransaccion(Prototype, ABC):
    def __init__(self, nro: int, fecha: date, valor: float):
        self.nro = nro
        self.fecha = fecha
        self.valor = valor
        self.lineas: List[LineaDocTransaccion] = []

    @abstractmethod
    def clone(self) -> 'DocumentoTransaccion':
        pass

# Factura class
class Factura(DocumentoTransaccion):
    def clone(self) -> 'DocumentoTransaccion':
        return copy.deepcopy(self)

# Descargo class
class Descargo(DocumentoTransaccion):
    def agregar_servicio(self, servicio: 'Servicio') -> None:
        linea = LineaDocTransaccion(1, servicio.get_precio(), servicio)
        self.lineas.append(linea)
        self.valor += linea.calcular_subtotal()

    def clone(self) -> 'DocumentoTransaccion':
        return copy.deepcopy(self)

# LineaDocTransaccion class
class LineaDocTransaccion:
    def __init__(self, cantidad: int, precio_unitario: float, servicio: 'Servicio'):
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.servicio = servicio

    def calcular_subtotal(self) -> float:
        return self.cantidad * self.precio_unitario

# Abstract Servicio class
class Servicio(ABC):
    def __init__(self, id: int, descripcion: str, precio: float):
        self.id = id
        self.descripcion = descripcion
        self._precio = precio

    @abstractmethod
    def registrar_servicio(self) -> None:
        pass

    def get_precio(self) -> float:
        return self._precio

# Concrete Servicio classes
class AtencionMedica(Servicio):
    def registrar_servicio(self) -> None:
        print(f"Registrando atención médica: {self.descripcion}")

class ExamenLab(Servicio):
    def registrar_servicio(self) -> None:
        print(f"Registrando examen de laboratorio: {self.descripcion}")

class ImagenRayosX(Servicio):
    def registrar_servicio(self) -> None:
        print(f"Registrando imagen de rayos X: {self.descripcion}")

class SuministroMedicamento(Servicio):
    def registrar_servicio(self) -> None:
        print(f"Registrando suministro de medicamento: {self.descripcion}")

class ProcedimientoMedico(Servicio):
    def registrar_servicio(self) -> None:
        print(f"Registrando procedimiento médico: {self.descripcion}")

# Example usage
if __name__ == "__main__":
    # Create a patient
    paciente = Paciente(1, "Juan Pérez", "Historial médico del paciente")

    # Create a Descargo document
    descargo = Descargo(101, date.today(), 0.0)
    
    # Add services to Descargo
    servicio1 = AtencionMedica(1, "Consulta general", 50.0)
    servicio2 = ExamenLab(2, "Análisis de sangre", 30.0)
    
    descargo.agregar_servicio(servicio1)
    descargo.agregar_servicio(servicio2)
    
    print(f"Valor total del descargo: {descargo.valor}")
    
    # Clone the Descargo
    descargo_clonado = descargo.clone()
    print(f"Valor total del descargo clonado: {descargo_clonado.valor}")
    
    # Verify cloning
    servicio3 = ImagenRayosX(3, "Radiografía de tórax", 100.0)
    descargo_clonado.agregar_servicio(servicio3)
    
    print(f"Valor descargo original tras clonación: {descargo.valor}")
    print(f"Valor descargo clonado tras agregar servicio: {descargo_clonado.valor}")