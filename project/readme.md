Proyecto de compiladores
========================
Realizado por Kevin Contreras - A01635597

Estructura
----------
**LexerParser**
Archivo que contiene las reglas de produccion y los tokens, ademas aqui mismo verifica tipos 
usando diferentes expresiones para reconocer primitivos

**semanticanalize**
Su principal funcion es realizar verificacion del uso de variables enter scopes

**tac**
genera el codigo de tres direcciones

Features y consideraciones
--------------------------
las formas de expresar los primitivos son las sigueintes:
integer : int
float: float
string: string
boolean : boolean

Los strings deben ir entre comillas dobles ("ejemplo")
Los booleanos basico van en minuscula (true, false)

Estructura del arbol
--------------------

Ver imagen "abstract tree estructura.png"

Notas o comentarios
-------------------
Profe por cuestiones de tiempo y otras materias no alcanze a terminar
Esta cada feture en un archivo pero no se mezclan bien
La parte de scopes y tac las hice con un arbol generado de prueba