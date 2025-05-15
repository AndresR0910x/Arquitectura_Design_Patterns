from abc import ABC, abstractmethod

# Interface for EstadoPaciente
class EstadoPaciente(ABC):
    @abstractmethod
    def manejarEstado(self, paciente: 'Paciente') -> None:
        pass

# Concrete state: Registrado
class Registrado(EstadoPaciente):
    def manejarEstado(self, paciente: 'Paciente') -> None:
        print(f"Paciente {paciente.nombre} está registrado. Cambiando a estado EnConsulta.")
        paciente.setEstado(EnConsulta())

# Concrete state: EnConsulta
class EnConsulta(EstadoPaciente):
    def manejarEstado(self, paciente: 'Paciente') -> None:
        print(f"Paciente {paciente.nombre} está en consulta. Cambiando a estado EnTratamiento o Alta.")
        # For simplicity, assume transition to EnTratamiento
        paciente.setEstado(EnTratamiento())

# Concrete state: EnTratamiento
class EnTratamiento(EstadoPaciente):
    def manejarEstado(self, paciente: 'Paciente') -> None:
        print(f"Paciente {paciente.nombre} está en tratamiento. Cambiando a estado Alta.")
        paciente.setEstado(Alta())

# Concrete state: Alta
class Alta(EstadoPaciente):
    def manejarEstado(self, paciente: 'Paciente') -> None:
        print(f"Paciente {paciente.nombre} ha recibido el alta. No hay más transiciones.")

# Context: Paciente
class Paciente:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.estado: EstadoPaciente = Registrado()  # Initial state

    def setEstado(self, estado: EstadoPaciente) -> None:
        self.estado = estado

    def manejar(self) -> None:
        self.estado.manejarEstado(self)

# Example usage
if __name__ == "__main__":
    paciente = Paciente("Juan Pérez")
    
    print("Estado inicial:")
    paciente.manejar()  # Registrado -> EnConsulta
    
    print("\nSiguiente estado:")
    paciente.manejar()  # EnConsulta -> EnTratamiento
    
    print("\nSiguiente estado:")
    paciente.manejar()  # EnTratamiento -> Alta
    
    print("\nSiguiente estado:")
    paciente.manejar()  # Alta (no further transitions)