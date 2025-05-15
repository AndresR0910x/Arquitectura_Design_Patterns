from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

# Interfaz Observador
class Observador(ABC):
    @abstractmethod
    def actualizar(self, sujeto) -> None:
        pass

# Interfaz Sujeto
class Sujeto(ABC):
    @abstractmethod
    def adjuntar(self, observador: Observador) -> None:
        pass

    @abstractmethod
    def desadjuntar(self, observador: Observador) -> None:
        pass

    @abstractmethod
    def notificar(self) -> None:
        pass

# Sujeto Concreto - Cuenta de Paciente
class CuentaPaciente(Sujeto):
    def __init__(self, id_paciente: str, nombre_paciente: str):
        self._id_paciente = id_paciente
        self._nombre_paciente = nombre_paciente
        self._observadores: List[Observador] = []
        self._servicios: List[dict] = []
        self._monto_total: float = 0.0

    def adjuntar(self, observador: Observador) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desadjuntar(self, observador: Observador) -> None:
        self._observadores.remove(observador)

    def notificar(self) -> None:
        for observador in self._observadores:
            observador.actualizar(self)

    def agregar_servicio(self, tipo_servicio: str, descripcion: str, monto: float) -> None:
        servicio = {
            'tipo': tipo_servicio,
            'descripcion': descripcion,
            'monto': monto,
            'fecha_hora': datetime.now()
        }
        self._servicios.append(servicio)
        self._monto_total += monto
        self.notificar()

    def obtener_servicios(self) -> List[dict]:
        return self._servicios

    def obtener_monto_total(self) -> float:
        return self._monto_total

    def obtener_info_paciente(self) -> dict:
        return {
            'id_paciente': self._id_paciente,
            'nombre_paciente': self._nombre_paciente
        }

# Observador Concreto - Departamento de Facturación
class DepartamentoFacturacion(Observador):
    def __init__(self, nombre_departamento: str):
        self._nombre_departamento = nombre_departamento

    def actualizar(self, sujeto: CuentaPaciente) -> None:
        print(f"\nDepartamento de Facturación {self._nombre_departamento} notificado:")
        print(f"Paciente: {sujeto.obtener_info_paciente()['nombre_paciente']}")
        print(f"Monto Total: ${sujeto.obtener_monto_total():.2f}")
        print("Servicios Recientes:")
        for servicio in sujeto.obtener_servicios()[-3:]:  # Mostrar últimos 3 servicios
            print(f"- {servicio['tipo']}: {servicio['descripcion']} (${servicio['monto']:.2f})")

# Observador Concreto - Departamento de Inventario
class DepartamentoInventario(Observador):
    def __init__(self, nombre_departamento: str):
        self._nombre_departamento = nombre_departamento

    def actualizar(self, sujeto: CuentaPaciente) -> None:
        print(f"\nDepartamento de Inventario {self._nombre_departamento} notificado:")
        print(f"Paciente: {sujeto.obtener_info_paciente()['nombre_paciente']}")
        print("Servicios recientes que requieren verificación de inventario:")
        for servicio in sujeto.obtener_servicios()[-3:]:
            if servicio['tipo'] in ['medicamento', 'suministros']:
                print(f"- {servicio['tipo']}: {servicio['descripcion']}")

# Ejemplo de uso
def main():
    # Crear una cuenta de paciente
    paciente = CuentaPaciente("P001", "Juan Pérez")

    # Crear observadores
    facturacion = DepartamentoFacturacion("Principal")
    inventario = DepartamentoInventario("Central")

    # Adjuntar observadores a la cuenta del paciente
    paciente.adjuntar(facturacion)
    paciente.adjuntar(inventario)

    # Agregar algunos servicios
    paciente.agregar_servicio("consulta", "Consulta inicial con el doctor", 150.00)
    paciente.agregar_servicio("medicamento", "Antibióticos", 75.50)
    paciente.agregar_servicio("laboratorio", "Análisis de sangre", 200.00)
    paciente.agregar_servicio("rayos_x", "Radiografía de tórax", 120.00)
    paciente.agregar_servicio("suministros", "Suministros médicos", 45.00)

if __name__ == "__main__":
    main()