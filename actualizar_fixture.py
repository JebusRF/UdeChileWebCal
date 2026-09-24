from icalendar import Calendar, Event
from datetime import datetime, timedelta
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TORNEOS = [
    "chi.1",
    "chi.copa_chi",
    "chi.super_cup",
    "conmebol.libertadores",
    "conmebol.sudamericana",
    "fifa.friendly"
]


def obtener_eventos():

    eventos_unicos = {}

    for torneo in TORNEOS:

        pagina = 1

        while True:

            url = (
                "https://sports.core.api.espn.com/v2/"
                f"sports/soccer/leagues/{torneo}/"
                f"seasons/2026/teams/2688/events"
                f"?page={pagina}"
            )

            respuesta = requests.get(
                url,
                headers=HEADERS,
                timeout=30
            )

            if respuesta.status_code != 200:
                break

            datos = respuesta.json()

            for item in datos.get("items", []):
                eventos_unicos[item["$ref"]] = torneo

            if pagina >= datos.get("pageCount", 1):
                break

            pagina += 1

    return eventos_unicos


def obtener_detalle_evento(url):

    url = url.replace("http://", "https://")

    respuesta = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    respuesta.raise_for_status()

    return respuesta.json()


def obtener_nombre_torneo(slug):

    nombres = {
        "chi.1": "Primera División de Chile",
        "chi.copa_chi": "Copa Chile",
        "chi.super_cup": "Supercopa de Chile",
        "conmebol.libertadores": "CONMEBOL Libertadores",
        "conmebol.sudamericana": "CONMEBOL Sudamericana",
        "fifa.friendly": "Amistoso"
    }

    return nombres.get(slug, slug)


def crear_calendario():

    calendario = Calendar()

    calendario.add(
        "prodid",
        "-//JebusRF Colo-Colo WebCal//"
    )

    calendario.add(
        "version",
        "2.0"
    )

    eventos_ref = obtener_eventos()

    total = 0
    uids_agregados = set()

    for ref, torneo_slug in eventos_ref.items():

        try:

            partido = obtener_detalle_evento(ref)

            uid = f"{partido['id']}@jebusrf"

            if uid in uids_agregados:
                continue

            uids_agregados.add(uid)

            fecha = partido["date"]

            nombre = partido["name"]

            if " at " in nombre:
                visitante, local = nombre.split(" at ")
                titulo = f"{local} vs {visitante}"
            else:
                titulo = nombre

            inicio = datetime.fromisoformat(
                fecha.replace("Z", "+00:00")
            )

            termino = inicio + timedelta(hours=2)

            estadio = "Por confirmar"

            try:
                estadio = (
                    partido["competitions"][0]
                    ["venue"]
                    ["fullName"]
                )
            except Exception:
                pass

            torneo = obtener_nombre_torneo(torneo_slug)

            evento = Event()

            evento.add("uid", uid)
            evento.add("summary", titulo)
            evento.add("location", estadio)

            descripcion = (
                f"Club: Colo-Colo\r\n"
                f"\r\n"
                f"Torneo: {torneo}\r\n"
                f"\r\n"
                f"Estadio: {estadio}\r\n"
                f"\r\n"
                f"Fuente: ESPN Core API\r\n"
                f"\r\n"
                f"https://jebusrf.github.io/Colo-ColoWebCal/"
            )

            evento.add(
                "description",
                descripcion
            )

            evento.add("dtstart", inicio)
            evento.add("dtend", termino)

            calendario.add_component(evento)

            total += 1

        except Exception as e:

            print(f"ERROR EN EVENTO: {ref}")
            print(e)

    with open(
        "docs/colocolo.ics",
        "wb"
    ) as archivo:

        archivo.write(
            calendario.to_ical()
        )

    print("CALENDARIO GENERADO CORRECTAMENTE")
    print(f"PARTIDOS GENERADOS: {total}")


if __name__ == "__main__":
    crear_calendario()
