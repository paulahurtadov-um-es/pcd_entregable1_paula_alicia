import entrega_prac_ESTA_1 as e

import pytest

@pytest.fixture
def universidad():
    # Creamos una instancia de la universidad para usarla en nuestras pruebas
    return e.Universidad("UM", "/Murcia")



def test_añadir_miembro_departamento(universidad):

    # Creamos un profesor asociado para añadir a la universidad
    profesor1 = e.ProfesorAsociado("Juan", "1111", "C/Flores", e.Sexo.V)

    # Añadimos el profesor al departamento DIIC
    universidad.añadirMiembro(e.Departamentos.DIIC, profesor1)

    #Comprobamos el método 'busquedaMiembro'
    miembro = universidad.busquedaMiembro('1111')
    assert isinstance(miembro,e.MiembroDepartamento)

    #comprobamos el método 'es_miembro'
    c = universidad.es_miembro(profesor1)
    assert c == True
    # Comprobamos si el profesor está en el diccionario de miembros del departamento DIIC
    assert profesor1.dni in universidad.mostrarMiembros()[e.Departamentos.DIIC.name].keys()

    # Comprobamos que el profesor añadido es el mismo que creamos
    assert universidad.mostrarMiembros()[e.Departamentos.DIIC.name][profesor1.dni].persona == profesor1




def test_eliminar_miembro_departamento_no_miembro(universidad) :
    universidad.añadirEstudiante('Luisa','2222','C/Paz',e.Sexo.M)
    with pytest.raises(e.ErrorEnMiembro):
        universidad.eliminarMiembro('2222')




def test_añadir_miembro_no_miembro(universidad) :
    miembro_incorrecto = e.Estudiante('Luis','222','C/Lilas',e.Sexo.V)
    with  pytest.raises(e.ErrorEnMiembro):  #debemos comprobar que el error se resuelve correctamente con ErrorEnMiembro
        universidad.añadirMiembro(e.Departamentos.DIIC, miembro_incorrecto)  




def test_añadir_estudiante_no_sexo(universidad) :
    with pytest.raises(e.ErrorEnSexo) :
        universidad.añadirEstudiante('Pepe','3333','C/Color',123456)





def test_eliminar_miembro_no_existente(universidad) :
    with pytest.raises(e.ErrorEnMiembro) :
        universidad.eliminarMiembro('1234')




def test_eliminar_miembro_correcto(universidad) :
    profesor3 = e.ProfesorAsociado('Pepe','4444','C/Flores',e.Sexo.V)
    universidad.añadirMiembro(e.Departamentos.DIS,profesor3)
    #comprobamos primero que lo ha añadido correctemente
    assert profesor3.dni in universidad.mostrarMiembros()[e.Departamentos.DIS.name].keys()
    #comprobamos que lo ha eliminado correctemente 
    universidad.eliminarMiembro('4444')
    assert profesor3.dni not in universidad.mostrarMiembros()[e.Departamentos.DIS.name].keys()



def test_añadir_estudiante_ya_existente(universidad) :
    universidad.añadirEstudiante('Luis','222','C/Lilas',e.Sexo.V)
    with pytest.raises(e.ErrorEnEstudiante) :
        universidad.añadirEstudiante('Luis','222','C/Lilas',e.Sexo.V)



def test_eliminar_estudiante_ya_existente(universidad) :
    with pytest.raises(e.ErrorEnEstudiante) :
        universidad.eliminarEstudiante('99999999')



def test_cambio_departamento_no_departamento(universidad) :
    investigador1 = e.Investigador('Lola','5555','C/Flores',e.Sexo.M,'area 1')
    with pytest.raises(e.ErrorEnDepartamento) :
        universidad.cambioDepartamento(123456,investigador1)


def test_cambio_departamento_correcto(universidad) :
    investigador2 = e.Investigador('Lola','6666','C/Flores',e.Sexo.M,'area 1')
    universidad.añadirMiembro(e.Departamentos.DIIC,investigador2) #vamos a añadir a la investigadora al departamento DIIC, para luego cambiarla a DIS
    miembro = universidad.busquedaMiembro('6666')
    assert miembro.departamento.name == 'DIIC'
    assert investigador2.dni in universidad.mostrarMiembros()[e.Departamentos.DIIC.name].keys()
    universidad.cambioDepartamento(e.Departamentos.DIS,investigador2)
    assert investigador2.dni not in universidad.mostrarMiembros()[e.Departamentos.DIIC.name].keys()
    assert investigador2.dni in universidad.mostrarMiembros()[e.Departamentos.DIS.name].keys()
    assert miembro.departamento.name == 'DIS'


def test_cambio_departamento_mismo_departamento(universidad) :
    investigador3 = e.Investigador('José','7777','C/Flores',e.Sexo.V,'area 1')
    universidad.añadirMiembro(e.Departamentos.DITEC,investigador3)
    with pytest.raises(e.ErrorEnDepartamento) :
        universidad.cambioDepartamento(e.Departamentos.DITEC,investigador3)


def test_añadir_asignatura_estudiante(universidad) :
    universidad.añadirEstudiante('María','8888','C/Flores',e.Sexo.M)
    #comprobamos que el estudiante creado es una instancia de la clase <Estudiante>, utilizando el método de busquedaEstudiante
    estudiante3 = universidad.busquedaEstudiante('8888')
    assert isinstance(estudiante3,e.Estudiante)
    #comprobamos también que se ha añadido al diccionario de 'estudiantes' en <Universidad>
    assert estudiante3.dni in universidad.mostrarEstudiantes().keys()
    universidad.añadirAsignatura('mates')
    universidad.añadirAsignaturaEstudiante('mates','8888')
    asignatura1 = universidad.devolverAsignatura('mates')
    assert isinstance(asignatura1,e.Asignatura) #comprobamos que se ha creado correctamente la asignatura
    #comprobamos que la asignatura se ha añadido correctamente al diccionario 'asignaturas' en <Universidad>
    assert asignatura1.nombre in universidad.mostrarAsignaturas().keys()
    #comprobamos que se ha añadido el estudiante a la asignatura
    assert estudiante3.dni in asignatura1.estudiantes.keys()
    #comprobamos que se ha añadido la asignatura en el estudiante
    assert asignatura1.nombre in estudiante3.asignaturas.keys()



def test_añadir_asignatura_estudiante_no_estudiante(universidad) :
    universidad.añadirAsignatura('programación')
    with pytest.raises(e.ErrorEnEstudiante) :
        universidad.añadirAsignaturaEstudiante('programación','123456789')



def test_añadir_asignatura_estudiante_no_asignatura(universidad) :
    universidad.añadirEstudiante('María','9999','C/Flores',e.Sexo.M)
    with pytest.raises(e.ErrorEnAsignatura) :
        universidad.añadirAsignaturaEstudiante('hola','9999')




def test_eliminar_asignatura_estudiante_no_estudiante(universidad) :
    universidad.añadirAsignatura('ml')
    with pytest.raises(e.ErrorEnEstudiante) :
        universidad.eliminarAsignaturaEstudiante('ml',88)


def test_eliminar_asignatura_estudiante_no_asignatura(universidad) :
    universidad.añadirEstudiante('Emilio','0010','C/Flores',e.Sexo.V)
    with pytest.raises(e.ErrorEnAsignatura) :
        universidad.eliminarAsignaturaEstudiante(99,'0010')





def test_eliminar_asignatura_estudiante(universidad) : #comprobamos con esto que, si añadimos dos estudiantes, y luego eliminamos solo uno, la asignatura no se elimina del diccionario 'asignaturas' en <Universidad>.
    universidad.añadirEstudiante('Luis','0000','C/Flores',e.Sexo.V)
    universidad.añadirEstudiante('Rosa','0100','C/Flores',e.Sexo.M)
    universidad.añadirAsignatura('estadística')
    asig3 = universidad.devolverAsignatura('estadística')
    universidad.añadirAsignaturaEstudiante('estadística','0000')
    universidad.añadirAsignaturaEstudiante('estadística','0100')
    assert asig3.nombre in universidad.mostrarAsignaturas().keys()
    estudiante4 = universidad.busquedaEstudiante('0000')
    estudiante5 = universidad.busquedaEstudiante('0100')
    assert estudiante4.dni in asig3.estudiantes.keys()
    assert estudiante5.dni in asig3.estudiantes.keys()
    assert asig3.nombre in estudiante4.asignaturas.keys()
    assert asig3.nombre in estudiante5.asignaturas.keys()
    #ahora eliminamos un estudiante
    universidad.eliminarAsignaturaEstudiante('estadística','0000')
    #comprobamos que se ha eliminado correctamente el estudiante, pero no la asignatura
    assert asig3.nombre in universidad.mostrarAsignaturas().keys()
    assert estudiante4.dni not in asig3.estudiantes.keys()
    assert estudiante5.dni in asig3.estudiantes.keys()
    assert asig3.nombre not in estudiante4.asignaturas.keys()
    assert asig3.nombre in estudiante5.asignaturas.keys()




def test_añadir_asignatura_profesor(universidad) :
    profesor5 = e.ProfesorAsociado('Pablo','0001','C/Flores',e.Sexo.V)
    universidad.añadirAsignatura('ia')
    universidad.añadirAsignaturaProfesor('ia',profesor5)
    asignatura = universidad.devolverAsignatura('ia')
    assert profesor5.dni in asignatura.profesores.keys()
    assert asignatura.nombre in profesor5.asignaturas.keys()





def test_añadir_asignatura_profesor_no_profesor(universidad):
    universidad.añadirAsignatura('ie')
    with pytest.raises(e.ErrorEnProfesor) :
        universidad.añadirAsignaturaProfesor('ie',777)




def test_eliminar_asignatura_profesor(universidad) :
    universidad.añadirAsignatura('oo')
    asig = universidad.devolverAsignatura('oo')
    profesor = e.ProfesorTitular('Javier','0200','C/Flores',e.Sexo.V,'area 1')
    universidad.añadirAsignaturaProfesor('oo',profesor)
    assert asig.nombre in universidad.mostrarAsignaturas().keys()
    universidad.eliminarAsignaturaProfesor('oo',profesor)
    assert profesor.nombre not in asig.profesores.keys()
    assert asig.nombre not in profesor.asignaturas.keys()


def test_eliminar_asignatura_profesor_no_profesor(universidad) :
    universidad.añadirAsignatura('pp')
    with pytest.raises(e.ErrorEnProfesor) :
        universidad.añadirAsignaturaProfesor('pp',989898898)



def test_asignatura_ya_existente(universidad) :
    universidad.añadirAsignatura('ii')
    with pytest.raises(e.ErrorEnAsignatura) :
        universidad.añadirAsignatura('ii')


def test_busqueda_asignatura_no_asignatura(universidad) :
    with pytest.raises(e.ErrorEnAsignatura) :
        universidad.devolverAsignatura(7777)


def test_añadir_miembro_repetido(universidad) :
    profesor=e.ProfesorTitular('Javier','0020','C/Flores',e.Sexo.V,'area 1')
    universidad.añadirMiembro(e.Departamentos.DIIC,profesor)
    with pytest.raises(e.ErrorEnMiembro) :
        universidad.añadirMiembro(e.Departamentos.DIIC,profesor)

def test_cambio_departamento_mismo_departamento(universidad):
    profesor=e.ProfesorTitular('Javier','0002','C/Flores',e.Sexo.V,'area 1')
    universidad.añadirMiembro(e.Departamentos.DIIC,profesor)
    with pytest.raises(e.ErrorEnDepartamento) :
        universidad.cambioDepartamento(e.Departamentos.DIIC,profesor)


def test_eliminar_asignatura_no_asignatura(universidad) :
    with pytest.raises(e.ErrorEnAsignatura) :
        universidad.eliminarAsignatura(9888888)


def test_devolver_departamento_no_profesor(universidad) :
    with pytest.raises(e.ErrorEnMiembro) :
        universidad.devolverDepartamento(9999)



"""
Al ejecutar pytest en nuestro terminal, podemos comprobar que todos los test pasan con éxito.

"""