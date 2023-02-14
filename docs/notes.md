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

# Tecnologias

Triple disparo, disparo cargado, mucha cadencia

# Magias

Modifican el proyectil, se consiguen al subir de nivel al matar enemigos

# Implementacion

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

# Documentacion

https://www.pygame.org/docs/tut/SpriteIntro.html

Mirar la sección de grupos, es importante. Creo que tenemos que usar RenderPlain porque cambiamos el fondo en cada frame cuando movemos al player.

# Notes

- Usar spritecollide para detectar los disparos al player
- Usar groupcollide para detectar los disparos a los enemigos

usar cooldown para disparos y tener en cuenta el elapsed time

# Escene Manager

Fade entre escenas? Crear una escena que se encargue del fade y se modifique
el alpha al llamar a update

# Diseño engine

- Modelo

  - Items Jugador (upgrades)
  - Piso en el que estas
  - Vida
  - Experiencia
  - (nivel maybe)

- Entidades (para dentro de las escenas)

- Sistema controles

- Audio

# Sistema de entidades

Las living tienen que tener para hacerles dano. Las de proyectil ya

# Movimiento camara

Utilizar un singleton para la camara, que se mueva con el player.
Y crear un nuevo metodo/clase que cambie el codigo del draw del grupo
para que en el blit, se convierta la posicion de la entidad en la posicion
de la camara.

Crear folder `camera`, y crear un singleton que se encargue de la camara. Y un grupo
ScrollingGroup que se encargue de hacer el blit de las entidades con el rectangulo
modificado segun la camara.
