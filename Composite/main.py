from abc import ABC, abstractmethod
from datetime import date
from typing import List

class IDocumento(ABC):
    @abstractmethod
    def calcular_subtotal(self) -> float:
        pass

    @abstractmethod
    def clone(self):
        pass

class Servicio(ABC):
    def __init__(self, id: int, descripcion: str, precio: float):
        self.id = id
        self.descripcion = descripcion
        self.precio = precio

    def registrar_servicio(self):
        print(f"Servicio registrado: {self.descripcion} (${self.precio})")

class AtencionMedica(Servicio): pass
class ExamenLab(Servicio): pass
class ImagenRayosX(Servicio): pass
class SuministroMedicamento(Servicio): pass
class ProcedimientoMedico(Servicio): pass

class LineaDocTransaccion(IDocumento):
    def __init__(self, cantidad: int, precio_unitario: float, servicio):
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.servicio = servicio

    def calcular_subtotal(self) -> float:
        return self.cantidad * self.precio_unitario

    def clone(self):
        return LineaDocTransaccion(self.cantidad, self.precio_unitario, self.servicio)

class DocumentoTransaccion(IDocumento):
    def __init__(self, nro: int, fecha: date):
        self.nro = nro
        self.fecha = fecha
        self.valor = 0.0
        self.componentes: List[IDocumento] = []

    def agregar(self, componente: IDocumento):
        self.componentes.append(componente)

    def remover(self, componente: IDocumento):
        self.componentes.remove(componente)

    def calcular_subtotal(self) -> float:
        self.valor = sum(comp.calcular_subtotal() for comp in self.componentes)
        return self.valor

    def clone(self):
        nuevo = DocumentoTransaccion(self.nro, self.fecha)
        nuevo.componentes = [comp.clone() for comp in self.componentes]
        return nuevo

class Factura(DocumentoTransaccion):
    def clone(self):
        return super().clone()

class Descargo(DocumentoTransaccion):
    def agregar_servicio(self, servicio):
        linea = LineaDocTransaccion(cantidad=1, precio_unitario=servicio.precio, servicio=servicio)
        self.agregar(linea)

    def clone(self):
        return super().clone()

class Paciente:
    def __init__(self, id: int, nombre: str, historial: str):
        self.id = id
        self.nombre = nombre
        self.historial = historial
        self.documentos: List[DocumentoTransaccion] = []

    def agregar_documento(self, doc: DocumentoTransaccion):
        self.documentos.append(doc)

# === Ejecución principal ===
if __name__ == "__main__":
    paciente = Paciente(1, "Juan Pérez", "Historial H001")

    consulta = AtencionMedica(1, "Consulta médica", 40.0)
    rayosx = ImagenRayosX(2, "Radiografía", 100.0)

    doc = Descargo(101, date.today())
    doc.agregar_servicio(consulta)
    doc.agregar_servicio(rayosx)

    print(f"Subtotal del descargo: ${doc.calcular_subtotal():.2f}")
    paciente.agregar_documento(doc)
