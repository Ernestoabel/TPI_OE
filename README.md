# Trabajo Practico Integrador - Organizacion Empresarial

## Chatbot para gestion de viaticos

Este repositorio contiene un chatbot desarrollado como parte del Trabajo Practico Integrador de la materia Organizacion Empresarial de la Tecnicatura Universitaria en Programacion.

El proyecto simula la automatizacion de un proceso administrativo de solicitud de viaticos. El bot permite que un usuario inicie una solicitud, cargue destino, cantidad de dias y monto solicitado, y luego recibe una respuesta segun las reglas de negocio definidas.

## Proceso administrativo elegido

El proceso elegido es la gestion de viaticos dentro de una organizacion. En un escenario manual, el empleado solicita fondos para un viaje laboral y el area administrativa revisa si corresponde aprobar la solicitud y si existen fondos disponibles.

La propuesta del proyecto es automatizar ese flujo mediante un bot de Discord, dejando registro de las solicitudes en una base de datos simulada mediante un archivo CSV.

## Tecnologias utilizadas

- Python
- Discord API mediante la libreria `discord.py`
- CSV como base de datos simulada
- Bizagi para el modelado BPMN
- GitHub para control de versiones y entrega del codigo fuente

## Flujo principal del bot

1. El usuario inicia el proceso con el comando `!start`.
2. El bot pregunta si desea solicitar viaticos.
3. El usuario confirma la solicitud.
4. El bot solicita destino, cantidad de dias y monto.
5. El sistema registra la solicitud en `data/datos.csv`.
6. El bot evalua si el monto esta dentro del limite permitido.
7. El bot verifica si hay fondos disponibles.
8. El proceso finaliza con aprobacion, entrega de viaticos, rechazo o cancelacion.

## Comandos disponibles

| Comando | Descripcion |
| --- | --- |
| `!start` | Inicia una nueva solicitud de viaticos. |
| `!historial` | Muestra las ultimas solicitudes registradas en el CSV. |

## Configuracion y ejecucion

### 1. Instalar dependencias

```bash
pip install discord.py
```

### 2. Configurar el token de Discord

El bot utiliza una variable de entorno llamada `DISCORD_TOKEN`. No se debe escribir el token directamente dentro del codigo.

En PowerShell:

```powershell
$env:DISCORD_TOKEN="TU_TOKEN_DE_DISCORD"
```

### 3. Ejecutar el bot

Desde la raiz del repositorio:

```bash
python src/index.py
```

Si el token esta configurado correctamente, el bot se conectara a Discord y quedara listo para responder comandos.

## Persistencia de datos

Las solicitudes se guardan en el archivo:

```text
data/datos.csv
```

La estructura actual del archivo es:

| Campo | Descripcion | Ejemplo |
| --- | --- | --- |
| Usuario | Nombre del usuario que realiza la solicitud. | ernesto |
| Destino | Lugar al que viaja el empleado. | bariloche |
| Dias | Cantidad de dias solicitados. | 4 |
| Monto | Importe solicitado para viaticos. | 6000 |

## Relacion con la consigna

El proyecto cumple con los puntos principales solicitados para el Trabajo Practico Integrador:

- Modela un proceso administrativo mediante BPMN.
- Implementa un chatbot funcional para simular el proceso.
- Utiliza persistencia de datos mediante una base simulada en CSV.
- Incluye una maquina de estados para recordar en que paso se encuentra cada usuario.
- Contempla caminos felices e infelices, como datos invalidos, cancelacion o rechazo por monto elevado.

## Caminos contemplados

### Camino feliz

El usuario inicia la solicitud, carga datos validos, el monto esta dentro del limite y existen fondos disponibles. El bot registra la solicitud y confirma la entrega de viaticos.

### Caminos infelices

- El usuario cancela la solicitud.
- El usuario ingresa una cantidad de dias invalida.
- El usuario ingresa un monto invalido.
- El monto solicitado supera el limite permitido.
- No hay fondos disponibles para completar la entrega.

## Autores

Trabajo realizado en grupo para la materia Organizacion Empresarial.
Integrantes: 
            Ernesto Abel Fatala - Comisión 20
            Juan Amador Lizarrondo Buffa - Comisión 19
