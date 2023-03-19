# Specification

1- Diseñar los niveles
2- Metodologia para el desarrollo (tareas, etc...)

TODO
[x] Generacion procedural con ruido en vez de salas individuales. (Suso)
[x] Buscar sprites - Suelo nave - Pared nave - Arma - Protagonista - Proyectiles (bolas de plasma) - Enemigos (dos tipos)

IDEAS

Decoracion del suelo/pared con ruido? Decidir donde van las tiles con ruido.
Dificultad de enemigos segun el color, que no sea aleatorio

Un par de enemigos parametrizados (podrían ser con efectos random etc)

Que haya un par de enemigos por mapa,

Area de iluminacion alrededor del protagonista (visibilidad reducida,
para dar ambiente)

Upgrades tecnologicas te las encuentras dropeadas
Upgrades mágicas al subir de nivel, te cambian las propiedades
del disparo y

Obstaculos (que se puedan romper)

Municion infinita

## Tecnologias

Triple disparo, disparo cargado, mucha cadencia

## Magias

Modifican el proyectil, se consiguen al subir de nivel al matar enemigos

## Implementacion

Arbol de clases

Entidades, que tengan cosas en comun

Y se van especializacion

- Entidad
  - Living entity
    - Player
    - Aliens
  - No living
    - proyectiles
    - xp
- Clase del nivel, instanciadas con distintos parametros
  para cada nivel

- Clase para las upgrades,

## Documentacion

<https://www.pygame.org/docs/tut/SpriteIntro.html>

Mirar la sección de grupos, es importante. Creo que tenemos que usar RenderPlain porque cambiamos el fondo en cada frame cuando movemos al player.

## Notes

- Usar spritecollide para detectar los disparos al player
- Usar groupcollide para detectar los disparos a los enemigos

usar cooldown para disparos y tener en cuenta el elapsed time

## Scene Manager

Fade entre escenas? Crear una escena que se encargue del fade y se modifique
el alpha al llamar a update

## Diseño engine

- Modelo

  - Items Jugador (upgrades)
  - Piso en el que estas
  - Vida
  - Experiencia
  - (nivel maybe)

- Entidades (para dentro de las escenas)

- Sistema controles

- Audio

## Sistema de entidades

Las living tienen que tener para hacerles dano. Las de proyectil ya

## Movimiento camara

Utilizar un singleton para la camara, que se mueva con el player.
Y crear un nuevo metodo/clase que cambie el codigo del draw del grupo
para que en el blit, se convierta la posicion de la entidad en la posicion
de la camara.

Crear folder `camera`, y crear un singleton que se encargue de la camara. Y un grupo
ScrollingGroup que se encargue de hacer el blit de las entidades con el rectangulo
modificado segun la camara.

## Scroll parallax y background

poner un background grande, rollo espacio. Y los huecos del mapa que no sean nave,
que por ejemplo sea una imagen del espacio y asteroides grande, y que se mueva el
scroll más despacio que con la cámara del personaje

## Modelo

Donde se hace la inialización del Model? en el init del game? al darle
a start?

## HUD

barra de vida encima/debajo de los enemigos?

Barra de vida del player en una esquina, o encima del player?

## Upgrades

De momento modelarlas solo en código.

Magicas -> Lista de efectos a aplicar ordenada. Cuando se ejecute alguna accion, por ejemplo la muerte, se itera sobre las upgrades

Las upgrades tecnológicas, si no se guardan, el orden en el que se obtienen afecta. Deberíamos tener esto en cuenta, y recalcular
cada vez que se modifica el arma todo, o simplemente nos da igual?

Usar patrón decorador en upgrades tecnológicas/mágicas?

Efecto de jitter en el disparo, parecido al spread pero aleatorio

# Notas para la entrega

En el director usamos el patrón plantilla (y el composite?)

## Menu de pausa

en vez de pintar de negro sobre la escena anterior, pinta una cortina con cierto alpha,
y después pintar la pantall de pausa por encima

## misc

Usar librería abstract class python para forzar implementacion de metodos

Patron fachada para ocultar la lógica de negocio. Sirve para encapsular cualquier tipo de comportamiento
Así desacoplo la lógica del menu de la parte del director
Se usa en los metodos propios del menu: salirPrograma, ejecutarJuego, etc...

## Minimapa

Añadir minimapa con lo de clipping de los apuntes

## Mejoras mágicas

Que se haga más grande el disparo, se puede hacer con un apply upgrade, pero las balas tienen que guardar una referencia a la gun, que tiene las upgrades y se pueden aplicar sobre el proyectil en el init por ejemplo.

Crear metodos setup y oncollide en las balas...

Puedo tener 3 listas con los distintos tipos de las updates,

Que las updates tengan un metodo attach al player, y tener una jerarquia de clases de forma que cada tipo de update, en su attach al player, llame
al append de la lista correspondiente

##

Justificar patron visitador para el jugador en el minimapa, igual es mejor usar el observer? Para los enemigos igual es mejor el observer
Igual va mejor el patrón observer

Para la barra de vida usar un observer

##

Idea para que sea más entretenido volver a jugar: Un timer que cuente el tiempo que llevas jugando. Guardar el mejor tiempo o

##

Justificar en la memoria por qué el sistema de upgrades es un singleton externo y no se gestiona dentro del player

# Bugs

Balas en la nave atraviesan esquinas

# Repartir

Jan Balance

Suso acabarlo

Román Descripcion (2.1)

En descripcion global de cada escena explicar el generador

Diagrama de flujo -> Jorge

Diagrama de arquitectura que dice como se comunican los sistemas, y después un diagrama de clases para cada uno de cada sistema


Diagramas-> Jorge