from enum import Enum
from abc import ABCMeta, abstractmethod
from typing import Any

# -----------------------
# EXCEPCIONES
# -----------------------
class ErrorEnDepartamento(Exception):
    pass

class ErrorEnMiembro(Exception):
    pass

class ErrorEnEstudiante(Exception):
    pass

class ErrorEnAsignatura(Exception):
    pass

class ErrorEnProfesor(Exception):
    pass

class ErrorEnSexo(Exception): 
    pass


# -----------------------
# ENUMERADOS
# -----------------------
class Sexo(Enum):
    V = 0
    M = 1

class Departamentos(Enum):
    DIIC = 0
    DITEC = 1
    DIS = 2


# -----------------------
# CLASES
# -----------------------
class Persona(metaclass = ABCMeta) :
    @abstractmethod
    def __init__(self,nombre,dni,direccion,sexo) :
        self.nombre = nombre  
        self.dni = dni
        self.direccion = direccion
        self.sexo=sexo
            
    def devolverDatos(self) :
        pass

"""
Para la clase Persona, al ser una clase abstracta, en ella no implementamos ningún método,
únicamente definimos los atributos de las instancias (los cuales se crean en las clases ProfesorAsociado, 
ProfesorTitular, Investigador, Estudiante, que heredan de esta).

Para el atributo "sexo", hemos utilizado una enumeración, donde el usuario introduce Sexo.V o Sexo.M.


"""

class MiembroDepartamento :
    def __init__(self,departamento,persona) :
        if not isinstance(departamento,Departamentos) :
            print("El departamento debe ser DIIC, DITEC O DIS, y debe pertenecer a la clase (enumeración) <Departamentos>")
            raise ErrorEnDepartamento
        if isinstance(persona,ProfesorTitular) or isinstance(persona,ProfesorAsociado) or isinstance(persona,Investigador) :
            self.departamento =departamento
            self.persona = persona
        else :
            print("La persona debe ser o Profesor Titular o Profesor Asociado o Investigador")
            raise ErrorEnMiembro
       
    def __del__(self) :
        pass

    def cambioDepartamento(self,departamento) :
        if not isinstance(departamento,Departamentos) :
            print("El departamento debe ser DIIC, DITEC O DIS, y debe pertenecer a la clase (enumeración) <Departamentos>")
            raise ErrorEnDepartamento
        self.departamento = departamento

"""

Como esta clase mantiene una relación de composición con las clases ProfesorTitular, ProfesorAsociado e Investigador,
cualquier instancia de MiembroDepartamento se va a crear en base a las instancias creadas en ProfesorTitular, ProfesorAsociado e Investigador.
Es a través de la clase Universidad donde el usuario (con el método 'añadirMiembro') crea una instancia de MiembroDepartamento a partir de las 
instancias de las otras tres clases.

Esta clase cuenta con un único método (de instancia), 'cambioDepartamento', que es llamado por el método 'cambioDepartamento' en la clase Universidad 
(es el usuario quien solicita a la Universidad el cambio de departamento de un profesor/investigador determinado).


"""


class Investigador(Persona) :
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion):
        if not isinstance(sexo,Sexo) :
            print("El sexo debe pertenecer a la clase (enumeración) <Sexo>.")
            raise ErrorEnSexo
        super().__init__(nombre, dni, direccion, sexo)
        self.area_investigacion=area_investigacion

    def __del__(self) :
        pass

    def devolverDatos(self) :
        print("Datos del Investigador/a : \n\t| Nombre: {} |\n\t| DNI: {} |\n\t| Direccion: {} |\n\t| Sexo: {} |".format(self.nombre,self.dni,self.direccion,self.sexo.name))
        return


"""
La clase Investigador hereda de persona, y como tal, hereda sus atributos y métodos. Al ser una clase abstracta,
se debe implementar el método "devolverDatos".

"""



class Universidad :
    def __init__(self,nombre,direccion,estudiantes=None,miembrosDep=None,asignaturas=None) :
        self.nombre=nombre
        self.direccion=direccion
        self._estudiantes = estudiantes if estudiantes is not None else {}
        self._miembrosDep = miembrosDep if miembrosDep is not None else {'DIIC':{},'DITEC':{},'DIS':{}}
        self._asignaturas = asignaturas if asignaturas is not None else {}
   
    def __del__(self) :
        pass

    def añadirMiembro(self,departamento,persona) :
        if not isinstance(departamento,Departamentos) :
            print("El departamento debe ser DIIC, DITEC O DIS, y debe pertenecer a la clase (enumeración) <Departamentos>")
            raise ErrorEnDepartamento
        if self.es_miembro(persona) : #El error relacionado con el objeto 'persona' ya es tratado en el método 'es_miembro' 
            print("La persona ya es miembro de departamento.") 
            raise ErrorEnMiembro
        miembro = MiembroDepartamento(departamento,persona)#Se crea la instancia de MiembroDepartamento. 
        self._miembrosDep[miembro.departamento.name][miembro.persona.dni] = miembro

        

    def añadirEstudiante(self,nombre, dni, direccion, sexo, asignaturas= None) :
        if not isinstance(sexo,Sexo) :
            print("El sexo debe pertenecer a la clase (enumeración) <Sexo>.")
            raise ErrorEnSexo
        if dni not in self._estudiantes.keys() : #ERROR: CUANDO YA EL ESTUDIANTE ESTÉ EN DICT
            estudiante = Estudiante(nombre,dni,direccion,sexo,asignaturas) #se crea la instancia de Estudiante
            self._estudiantes[estudiante.dni] = estudiante #se añade al diccionario 'estudiantes'
        else :
            print("Esta persona ya es estudiante de la Universidad")
            raise ErrorEnEstudiante


    def eliminarMiembro(self,dni) :
        #primero, utilizamos el método definido en esta clase: 'busquedaMiembro', para obtener el objeto
        miembro = self.busquedaMiembro(dni)
        if not isinstance(miembro,MiembroDepartamento) :#significa que nos ha devuelto la cadena de '--->La persona con dicho DNI no pertenece a ningún departamento.'
            print("No se puede eliminar un miembro que no existe")
            raise ErrorEnMiembro
        self._miembrosDep[miembro.departamento.name].pop(miembro.persona.dni) #dicho objeto 'miembro' es utilizado para eliminar en el diccionario 'miembrosDep'


    def eliminarEstudiante(self,dni) :
        if dni in self._estudiantes.keys() :
            estudiante = self._estudiantes[dni] #localizamos el objeto a través del dni
            self._estudiantes.pop(estudiante.dni) #lo eliminamos del diccionario
        else:
            print("No se puede eliminar un estudiante que no existe")
            raise ErrorEnEstudiante
        #ERROR: CUANDO EL ESTUDIANTE NO ESTÉ EN DICT 


    def mostrarMiembros(self) :
        return self._miembrosDep 
    

    def cambioDepartamento(self,departamento,persona):
        if not isinstance(departamento,Departamentos) :
            print("El departamento debe ser DIIC, DITEC O DIS, y debe pertenecer a la clase (enumeración) <Departamentos>")
            raise ErrorEnDepartamento
        #ERROR, QUE LA PERSONA NO SEA MIEMBRO DE DEPARTAMENTO
        if self.es_miembro(persona) :
            depar = self.devolverDepartamento(persona)
            if depar != departamento.name : #ERROR: SI CAMBIAMOS LA PERSONA AL MISMO DEPARTAMENTO EN EL QUE YA SE ENCONTRABA
                #obtenemos el objeto de miembroDepartamento a través del diccionario
                miembro = self._miembrosDep[depar][persona.dni]
                #eliminamos a la persona de su antiguo departamento
                self.eliminarMiembro(persona.dni)
                miembro.cambioDepartamento(departamento)
                #añadimos a la persona al nuevo departamento
                self.añadirMiembro(departamento,persona)
            else :
                print("La persona ya se encuentra en dicho departamento")
                raise ErrorEnDepartamento
        else :
            print("La persona no es miembro de departamento")
            raise ErrorEnMiembro


    def busquedaEstudiante(self,dni) :
        if dni in self._estudiantes.keys() :
            estudiante = self._estudiantes[dni]
            return estudiante
        else :
            t = "--> La persona con dicho DNI no es estudiante de esta universidad"
            return t
        #ERROR SI NO SE ENCUENTRA DICHO DNI


    def busquedaMiembro(self,dni) :
        if dni in self._miembrosDep['DIIC'].keys() :
            miembro = self._miembrosDep['DIIC'][dni]
        elif dni in self._miembrosDep['DITEC'].keys() :
            miembro = self._miembrosDep['DITEC'][dni]
        elif dni in self._miembrosDep['DIS'].keys() :
            miembro = self._miembrosDep['DIS'][dni]
        else :
            t = '--->La persona con dicho DNI no pertenece a ningún departamento.'
            return t
        return miembro
        #ERROR: NO SE ENCUENTRA DICHO MIEMBRO
            
        

    def mostrarEstudiantes(self) :
        return self._estudiantes 
    
    
    def añadirAsignaturaEstudiante(self,asignatura_nombre,dni_estudiante) :
        #ERROR: asignatura NO SEA OBJETO DE ASIGNATURA
        #ERROR, DICHO DNI NO ESTÁ EN EL DICCIONARIO (NO ES ESTUDIANTE)
        asignatura = self.devolverAsignatura(asignatura_nombre) #No hace falta implementar el error de asignatura aquí porque ya está implementado en el método 'devolverAsignatura'
        if dni_estudiante in self._estudiantes.keys() :
            estudiante = self._estudiantes[dni_estudiante]
            asignatura.añadirEstudiante(estudiante)
        else :
            print("No se encuentra estudiante con dicho DNI")
            raise ErrorEnEstudiante

    def eliminarAsignaturaEstudiante(self,asignatura_nombre,dni_estudiante) :
        #ERROR: QUE asignatura NO SEA OBJETO DE ASIGNATURA
        #ERROR, DICHO DNI NO ESTÁ EN EL DICCIONARIO, NO ES ESTUDIANTE DE LA UNIVERSIDAD
        asignatura = self.devolverAsignatura(asignatura_nombre)
        if dni_estudiante in self._estudiantes.keys() :
            estudiante = self._estudiantes[dni_estudiante]
            asignatura.eliminarEstudiante(estudiante)
        else :
            print("No se encuentra estudiante con dicho DNI")
            raise ErrorEnEstudiante
    
    def añadirAsignaturaProfesor(self,asignatura_nombre,profesor) :
        #ERROR: QUE asignatura NO SEA OBJETO DE ASIGNATURA
        #ERROR: QUE EL OBJETO profesor NO SEA O ProfesorAsociado o ProfesorTitular
        #Suponemos que el profesor NO tiene que ser miembro de departamento para impartir asignaturas
        asignatura = self.devolverAsignatura(asignatura_nombre)
        if isinstance(profesor,ProfesorTitular) or isinstance(profesor,ProfesorAsociado) :
            asignatura.añadirProfesor(profesor)
        else :
            print("Profesor debe ser objeto de la clase <ProfesorTitular> o <ProfesorAsociado>")
            raise ErrorEnProfesor

    def eliminarAsignaturaProfesor(self,asignatura_nombre, profesor) : 
        #ERROR: QUE asignatura NO SEA OBJETO DE ASIGNATURA
        #ERROR: QUE EL OBJETO profesor NO SEA O ProfesorAsociado o ProfesorTitular
        asignatura = self.devolverAsignatura(asignatura_nombre)
        if isinstance(profesor,ProfesorTitular) or isinstance(profesor,ProfesorAsociado) :
            asignatura.eliminarProfesor(profesor)
        else :
            print("Profesor debe ser objeto de la clase <ProfesorTitular> o <ProfesorAsociado>")
            raise ErrorEnProfesor

    def mostrarAsignaturas(self) :
        return self._asignaturas
    
    def es_miembro(self,persona) :
        if isinstance(persona,ProfesorTitular) or isinstance(persona,ProfesorAsociado) or isinstance(persona,Investigador) :
            for miembro in self._miembrosDep['DIIC'].values() :
                if persona == miembro.persona :
                    return True
            for miembro in self._miembrosDep['DITEC'].values() :
                if persona == miembro.persona :
                    return True
            for miembro in self._miembrosDep['DIS'].values() :
                if persona == miembro.persona :
                    return True
            return False
        else :
            print("La persona debe ser o Profesor Titular, o Profesor Asociado o Investigador para ser miembro de departamento.")
            raise ErrorEnMiembro
    

    def devolverDepartamento(self,persona) :
        if isinstance(persona,ProfesorTitular) or isinstance(persona,ProfesorAsociado) or isinstance(persona,Investigador) :
            if self.es_miembro(persona) :
                miembro = self.busquedaMiembro(persona.dni)
                return miembro.departamento.name
            else :
                t = '----> La persona no es miembro de ningún departamento.'
                return t
        else :
            print("La persona debe ser o Profesor Titular, o Profesor Asociado o Investigador para ser miembro de departamento.")
            raise ErrorEnMiembro
        

    def añadirAsignatura(self,nombre,profesores=None,estudiantes=None) :
        if nombre not in self._asignaturas.keys() : #ERROR: CUANDO YA LA ASIGNATURA ESTÉ EN DICT
            asignatura = Asignatura(nombre,profesores,estudiantes) #se crea la instancia de Asignatura
            self._asignaturas[asignatura.nombre] = asignatura #se añade al diccionario 'asignaturas'
        else :
            print("Esta asignatura ya se encuentra en la Universidad")
            raise ErrorEnAsignatura
        

    def devolverAsignatura(self,nombre) :
        if nombre in self._asignaturas.keys() :
            asignatura = self._asignaturas[nombre]
            return asignatura
        else :
            print("Dicha asignatura no se encuentra en la Universidad")
            raise ErrorEnAsignatura
        

    def eliminarAsignatura(self,nombre) :
        if nombre in self._asignaturas.keys() :
            self._asignaturas.pop(nombre)
        else :
            print("La asignatura no se encuentra registrada en la Universidad")
            raise ErrorEnAsignatura
        



                
      

"""
La clase Universidad es el eje central de todo nuestro código. El usuario
a través de ella puede añadir y eliminar estudiantes, miembros de departamento, y asignaturas, además
de otros métodos.
En cuanto a los atributos de instancia, cabe destacar la estructura del diccionario de 'miembrosDep',
que a su vez contiene otros diccionarios que tienen como claves los DNI y como valores los objetos de la clase MiembroDepartamento.

"""

    



class ProfesorTitular(Investigador) :
    def __init__(self, nombre, dni, direccion, sexo,area_investigacion,asignaturas=None):
        if not isinstance(sexo,Sexo) :
            print("El sexo debe pertenecer a la clase (enumeración) <Sexo>.")
            raise ErrorEnSexo
        Investigador.__init__(self,nombre,dni,direccion,sexo,area_investigacion)
        self.asignaturas=asignaturas if asignaturas is not None else {}

    def __del__(self) :
        pass

    def devolverDatos(self) :  #sobrecarga del método devolverDatos de la clase Investigador de la que hereda
        print("Datos del Profesor/a Titular : \n\t| Nombre: {} |\n\t| DNI: {} |\n\t| Direccion: {} |\n\t| Sexo: {} |".format(self.nombre,self.dni,self.direccion,self.sexo.name))
        return
     

    def añadirAsignatura(self,asignatura) : #No implementamos el error relacionado con asignatura, porque ese error ya es tratado por los métodos 'añadirProfesor','eliminarProfesor' de Asignatura, que llaman a estos.
        self.asignaturas[asignatura.nombre] = asignatura   

    def eliminarAsignatura(self,asignatura) :
        self.asignaturas.pop(asignatura.nombre)
    
    def imparteProfesor(self,asignatura) : #objeto asignatura
        if not isinstance(asignatura,Asignatura) :
            print("Asignatura debe ser un objeto de la clase <Asignatura>")
            raise ErrorEnAsignatura
        if self.dni in asignatura.profesores.keys() :
            return True
        return False





"""
La clase ProfesorTitular hereda de Persona, y por tanto, hereda sus métodos y atributos, que al ser clase abstracta,
el método 'devolverDatos' debe de ser implementado aquí. 
Además, también hereda de la clase Investigador. Esta herencia es en esa dirección (ProfesorTitular hereda de Investigador) 
porque, cualquier instancia de la clase ProfesorTitular, es instancia a su vez de la clase Investigador 
(y de esta hereda sus atributos y métodos), y no al revés, ya que no todas las instancias de Investigador son instancias de ProfesorTitular
(todos los profesores titulares son investigadores pero no todos los investigadores son profesores titulares).


Se implementan dos métodos, 'añadirAsignatura' y 'eliminarAsignatura', que son llamados por los métodos
'añadirProfesor' y 'eliminarProfesor' de la clase Asignatura.

Y por último, el método 'imparteProfesor', que comprueba si dicho profesor está impartiendo una asignatura concreta.
"""



class ProfesorAsociado(Persona) :
    def __init__(self, nombre, dni, direccion, sexo,asignaturas=None):
        if not isinstance(sexo,Sexo) :
            print("El sexo debe pertenecer a la clase (enumeración) <Sexo>.")
            raise ErrorEnSexo
        super().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = asignaturas if asignaturas is not None else {}

    def __del__(self) :
        pass

    def devolverDatos(self) :
        print("Datos del Profesor/a Asociado/a : \n\t| Nombre: {} |\n\t| DNI: {} |\n\t| Direccion: {} |\n\t| Sexo: {} |".format(self.nombre,self.dni,self.direccion,self.sexo.name))
        return


    def añadirAsignatura(self,asignatura) : #No implementamos el error relacionado con asignatura, porque ese error ya es tratado por los métodos 'añadirProfesor','eliminarProfesor' de Asignatura, que llaman a estos.
        self.asignaturas[asignatura.nombre] = asignatura

    def eliminarAsignatura(self,asignatura) :
        self.asignaturas.pop(asignatura.nombre)
    
    def imparteProfesor(self,asignatura) : #objeto asignatura
        if not isinstance(asignatura,Asignatura) :
            print("Asignatura debe ser un objeto de la clase <Asignatura>")
            raise ErrorEnAsignatura
        if self.dni in asignatura.profesores.keys() :
            return True
        return False


"""
La clase ProfesorAsociado es muy parecida a la de ProfesorTitular, la única diferencia
es que no hereda de Investigador (solo de persona).

"""


class Estudiante(Persona): 
    def __init__(self, nombre, dni, direccion, sexo,asignaturas=None): #no implementamos el error en relación al atributo 'sexo' porque ya lo hemos tratado en el método 'añadirEstudiante' en Universidad, que es por donde el usuario añadirá o eliminará los estudiantes
        super().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = asignaturas if asignaturas is not None else {}

    def __del__(self) :
        pass


    def añadirAsignatura(self,asignatura) : #No implementamos el error relacionado con asignatura, porque ese error ya es tratado por los métodos 'añadirEstudiante','eliminarEstudiante' de Asignatura, que llaman a estos.
        self.asignaturas[asignatura.nombre] = asignatura

    def eliminarAsignatura(self,asignatura) :
        self.asignaturas.pop(asignatura.nombre)

    def devolverDatos(self) :
        print("Datos del Estudiante : \n\t| Nombre: {} |\n\t| DNI: {} |\n\t| Direccion: {} |\n\t| Sexo: {} |".format(self.nombre,self.dni,self.direccion,self.sexo.name))
        return
    
    def matriculadoEstudiante(self,asignatura) : #objeto asignatura
        if not isinstance(asignatura,Asignatura) :
            print("Asignatura debe ser un objeto de la clase <Asignatura>")
            raise ErrorEnAsignatura
        if self.dni in asignatura.estudiantes.keys() :
            return True
        return False


"""
En cuanto a los métodos relacionados con las asignaturas, 
estos métodos son llamados por los métodos de "añadirEstudiante" y "eliminarEstudiante" de la 
clase Asignatura.

Para el método 'matriculadoEstudiante' se comprueba si el alumno está matriculado en una asignatura concreta, 
comprobando si se encuentra en el diccionario 'estudiantes' en la clase Asignatura.

"""

class Asignatura :
    def __init__(self,nombre,profesores = None, estudiantes = None) :
        self.nombre = nombre
        self.profesores = profesores if profesores is not None else {}
        self.estudiantes = estudiantes if estudiantes is not None else {}

    def __del__(self) :
        pass

    def añadirEstudiante(self,estudiante) : #No implementamos el error en el objeto 'estudiante', porque ya se comprueba en el método 'añadirAsignaturaEstudiante' en Universidad, que llama a este método.
        if estudiante.dni in self.estudiantes.keys() :
            print("El estudiante ya se encuentra matriculado en dicha asignatura")
            raise ErrorEnEstudiante
        self.estudiantes[estudiante.dni] = estudiante 
        estudiante.añadirAsignatura(self)

    def eliminarEstudiante(self,estudiante) :
        if estudiante.dni not in self.estudiantes.keys() :
            print("El estudiante no se encuentra matriculado en dicha asignatura")
            raise ErrorEnEstudiante
        self.estudiantes.pop(estudiante.dni)
        estudiante.eliminarAsignatura(self)

    def añadirProfesor(self,profesor) :  # ------------------>no hace falta distinguir entre profesor titular o profesor asociado porque ambos cuentan con el mismo atributo 'asignaturas'
        if profesor.dni in self.profesores.keys() :
            print("El profesor ya se encuentra impartiendo la asignatura")
            raise ErrorEnProfesor
        self.profesores[profesor.dni] = profesor
        profesor.añadirAsignatura(self)

    def eliminarProfesor(self,profesor) :
        if profesor.dni not in self.profesores.keys() :
            print("El profesor no se encuentra impartiendo la asignatura")
            raise ErrorEnProfesor
        self.profesores.pop(profesor.dni)
        profesor.eliminarAsignatura(self)

    
"""
La clase Asignatura es la encargada por tanto (a través de la clase Universidad) de la gestión de asignaturas entre profesores
y estudiantes. La clase Universidad es la encargada de llamar a los métodos de la clase Asignatura, y esta a su vez llama a los métodos en las clases Estudiante, ProfesorAsociado y ProfesorTitular,
para añadir o quitar estudiantes y profesores (además de añadirlos y eliminarlos del diccionario de 'estudiantes' y 'profesores').
Las claves de estos diccionarios son los DNI.
También en esta clase se gestiona los posibles errores relacionados con añadir o eliminar
estudiantes o profesores que ya se encuentran en el diccionario de "estudiantes" y "profesores",
respectivamente.


"""


    


if __name__ == '__main__' :  

    Uni = Universidad('UM','C/89')
    
    Uni.añadirAsignatura('Matematicas')
    asignatura1 = Uni.devolverAsignatura('Matematicas')
    Uni.añadirAsignatura('Fisica I')
    asignatura2= Uni.devolverAsignatura('Fisica I')
    Uni.añadirAsignatura('Programacion')
    asignatura3 = Uni.devolverAsignatura('Programacion')
    
    Uni.añadirEstudiante('Luis','266Q','C/66',Sexo.V)
    estudiante1 = Uni.busquedaEstudiante('266Q')
    estudiante1.devolverDatos()
    Uni.añadirAsignaturaEstudiante('Matematicas','266Q')
    Uni.añadirEstudiante('Alicia','432L','C/22',Sexo.M)
    estudiante2 = Uni.busquedaEstudiante('432L')
    Uni.añadirAsignaturaEstudiante('Fisica I','432L')
    Uni.añadirAsignaturaEstudiante('Matematicas','432L')
    
    profesor1 = ProfesorAsociado('Pepe','111T','C/1',Sexo.V)
    Uni.añadirMiembro(Departamentos.DIIC,profesor1)
    profesor2 = ProfesorTitular('Alfonso','112R','C/12',Sexo.V,'Tecnologia')
    Uni.añadirMiembro(Departamentos.DIS,profesor2) 
    Uni.añadirAsignaturaProfesor('Matematicas',profesor1)
    
    invest = Investigador('Paula','890S','C/21',Sexo.M,'area 1')
    invest.devolverDatos()
    


    # Algunos ERRORES

    #Añadir un miembro del departamento DIIC al departamento DIS
    try :
        Uni.añadirMiembro(Departamentos.DIS,profesor1)
    except Exception as e :
        print("Excepción recibida: ", e) #informamos del error (no re-lanzamos)
     
    # Eliminar un estudiante que no está matriculado en dicha asignatura
    try :
        Uni.eliminarAsignaturaEstudiante('Programacion','266Q')
    except Exception as e:
        print ("Excepción recibida: ",e)  #informamos del error (no re-lanzamos)
     
    # Estudiante se matricula en una asignatura que ya tiene
    try :
        Uni.añadirAsignaturaEstudiante('Fisica I','432L')
    except Exception as e:
        print ("Excepción recibida:",e) #informamos del error (no re-lanzamos)
    
    # Añadir asignatura profesor donde, en vez de ser profesor, es a un alumno
    try :
        Uni.añadirAsignaturaProfesor('Fisica I','266Q')
    except Exception as e:
        print ("Excepción recibida: ",e)  #informamos del error (no re-lanzamos)
    
    # Añadir una asignatura que ya se encuentra en la universidad
    try :
        Uni.añadirAsignatura('Fisica I')
    except Exception as e:
        print ("Excepción recibida: ",e)  #informamos del error (no re-lanzamos)
    
    # Cambiar un profesor a un departamento que no existe
    try :
        Uni.cambioDepartamento('DIIS',profesor2)
    except Exception as e:
        print ("Excepción recibida: ",e)  #informamos del error (no re-lanzamos)



    print(estudiante1.matriculadoEstudiante(asignatura1))
    Uni.eliminarAsignaturaEstudiante('Matematicas','266Q')
    print(estudiante1.matriculadoEstudiante(asignatura1))
    Uni.eliminarMiembro('112R')
    print(Uni.es_miembro(profesor2))
    print(profesor1.imparteProfesor(asignatura1))
    Uni.eliminarAsignaturaProfesor('Matematicas',profesor1)
    print(profesor1.imparteProfesor(asignatura1))
    Uni.eliminarEstudiante('432L')
    print(Uni.mostrarEstudiantes().keys())
    Uni.eliminarAsignatura('Matematicas')
    print(Uni.mostrarAsignaturas().keys())
    