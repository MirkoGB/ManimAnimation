from manim import *
import numpy as np

COLORE_SENO = YELLOW
COLORE_COSENO = BLUE
COLORE_ANGOLO = GREEN
COLORE_RAGGIO = WHITE
COLORE_CERCHIO = GREY_B


def punto_sul_cerchio(angolo: float, centro: np.ndarray, raggio: float) -> np.ndarray:
    """Returns centro + raggio*(cos angolo, sin angolo, 0)."""
    return centro + raggio * np.array([np.cos(angolo), np.sin(angolo), 0.0])


def angolo_ridotto(angolo: float) -> float:
    """Riporta l'angolo in [0, 2π]; 2π esatto resta 2π (fine del primo giro)."""
    return angolo if angolo <= 2 * PI + 1e-6 else angolo % (2 * PI)


def crea_cerchio(centro: np.ndarray, raggio: float) -> VGroup:
    """Static objects: the circle (COLORE_CERCHIO, stroke_width 3) plus two thin grey
    axis lines through the centre (horizontal and vertical), each extending 0.3 units
    beyond the circle on both sides (stroke_width 2, color GREY_D).
    Return VGroup(cerchio, asse_x, asse_y)."""
    cerchio = Circle(
        radius=raggio, arc_center=centro, color=COLORE_CERCHIO, stroke_width=3
    )
    estensione = raggio + 0.3
    asse_x = Line(
        centro + estensione * LEFT,
        centro + estensione * RIGHT,
        color=GREY_D,
        stroke_width=2,
    )
    asse_y = Line(
        centro + estensione * DOWN,
        centro + estensione * UP,
        color=GREY_D,
        stroke_width=2,
    )
    return VGroup(cerchio, asse_x, asse_y)


def crea_elementi_dinamici(
    theta: ValueTracker, centro: np.ndarray, raggio: float
) -> dict[str, Mobject]:
    """Every value is an always_redraw(...) mobject reading theta.get_value() (radians).
    Keys (exact):
      "raggio":  Line from centro to the point, COLORE_RAGGIO, stroke_width 4
      "coseno":  Line from centro to (centro.x + raggio*cos θ, centro.y), COLORE_COSENO, stroke_width 6
      "seno":    Line from (centro.x + raggio*cos θ, centro.y) to the point, COLORE_SENO, stroke_width 6
      "arco":    Arc(radius=0.4, start_angle=0, angle=θ, arc_center=centro), COLORE_ANGOLO, stroke_width 4.
                 Guard: if θ < 0.01 use angle 0.01 so the Arc is never degenerate.
      "etichetta_theta": MathTex(r"\\theta", color=COLORE_ANGOLO, font_size=32) placed at
                 centro + 0.7*(cos(θ/2), sin(θ/2), 0)
      "punto":   Dot at the point on the circle, color WHITE, radius 0.08
    The value of θ may grow beyond 2π (several laps); everything must keep working.
    Note: when cos θ ≈ 0 or sin θ ≈ 0, a Line can have (almost) zero length; make sure
    that never raises an error (e.g. Manim Line with identical endpoints is OK, but verify)."""

    def punto():
        return punto_sul_cerchio(theta.get_value(), centro, raggio)

    def proiezione():
        # Proiezione del punto sull'asse orizzontale: (centro.x + raggio*cos θ, centro.y)
        x = centro[0] + raggio * np.cos(theta.get_value())
        return np.array([x, centro[1], centro[2]])

    def raggio_fn():
        return Line(centro, punto(), color=COLORE_RAGGIO, stroke_width=4)

    def coseno_fn():
        return Line(centro, proiezione(), color=COLORE_COSENO, stroke_width=6)

    def seno_fn():
        return Line(proiezione(), punto(), color=COLORE_SENO, stroke_width=6)

    def arco_fn():
        t = angolo_ridotto(theta.get_value())
        angolo = t if t >= 0.01 else 0.01
        return Arc(
            radius=0.4,
            start_angle=0,
            angle=angolo,
            arc_center=centro,
            color=COLORE_ANGOLO,
            stroke_width=4,
        )

    def etichetta_fn():
        t = angolo_ridotto(theta.get_value())
        posizione = centro + 0.7 * np.array([np.cos(t / 2), np.sin(t / 2), 0.0])
        return MathTex(r"\theta", color=COLORE_ANGOLO, font_size=32).move_to(posizione)

    def punto_fn():
        return Dot(point=punto(), radius=0.08, color=WHITE)

    return {
        "raggio": always_redraw(raggio_fn),
        "coseno": always_redraw(coseno_fn),
        "seno": always_redraw(seno_fn),
        "arco": always_redraw(arco_fn),
        "etichetta_theta": always_redraw(etichetta_fn),
        "punto": always_redraw(punto_fn),
    }


def crea_pannello_valori(theta: ValueTracker) -> VGroup:
    """A 3-row live panel, NOT positioned (the scene positions it). Rows:
         θ = 1.05        (label color COLORE_ANGOLO)
         sin θ = 0.87    (label color COLORE_SENO)
         cos θ = 0.50    (label color COLORE_COSENO)
    Each row = VGroup(MathTex label, DecimalNumber), number placed to the right of the
    label with buff 0.15. Numbers update via add_updater (set_value, then re-align).
    Rows arranged DOWN, aligned LEFT (arrange(DOWN, aligned_edge=LEFT, buff=0.25)).
    Return VGroup(row_theta, row_sin, row_cos)."""

    def riga(etichetta_tex: str, colore, funzione, con_segno: bool = True) -> VGroup:
        etichetta = MathTex(etichetta_tex, color=colore, font_size=36)
        numero = DecimalNumber(
            funzione(theta.get_value()),
            num_decimal_places=2,
            include_sign=con_segno,
            font_size=36,
            color=colore,
        )
        numero.next_to(etichetta, RIGHT, buff=0.15)

        def aggiorna(mob):
            mob.set_value(funzione(theta.get_value()))
            mob.next_to(etichetta, RIGHT, buff=0.15)

        numero.add_updater(aggiorna)
        return VGroup(etichetta, numero)

    row_theta = riga(r"\theta =", COLORE_ANGOLO, angolo_ridotto, con_segno=False)
    row_sin = riga(r"\sin\theta =", COLORE_SENO, np.sin)
    row_cos = riga(r"\cos\theta =", COLORE_COSENO, np.cos)

    pannello = VGroup(row_theta, row_sin, row_cos)
    pannello.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    return pannello
