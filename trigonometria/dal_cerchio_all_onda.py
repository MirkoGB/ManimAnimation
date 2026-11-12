"""Dal cerchio all'onda: la curva del seno nasce dal moto di un punto sulla circonferenza.

Usa i moduli di supporto di elementi.py (stessa cartella).
Render di prova:
    manim -ql trigonometria\\dal_cerchio_all_onda.py DalCerchioAllOnda
"""
from manim import *
import numpy as np

from elementi import *

CENTRO = np.array([-4.5, 0, 0])
R = 1.6
ORIGINE_GRAFICO = np.array([-2.2, 0, 0])


def angolo_onda(theta: ValueTracker) -> float:
    """Angolo usato dal grafico: dopo 2*PI ricomincia dal primo giro."""
    return angolo_ridotto(theta.get_value())


class DalCerchioAllOnda(Scene):
    def construct(self):
        # 1. Titolo
        titolo = Text("Dal cerchio all'onda", font_size=56)
        self.play(Write(titolo))
        self.wait(1)
        self.play(FadeOut(titolo))

        # 2. Cerchio, elementi dinamici e pannello dei valori
        theta = ValueTracker(0)
        cerchio = crea_cerchio(CENTRO, R)
        self.play(Create(cerchio), run_time=1.5)

        dinamici = crea_elementi_dinamici(theta, CENTRO, R)
        self.play(
            FadeIn(dinamici["raggio"]),
            FadeIn(dinamici["punto"]),
            FadeIn(dinamici["arco"]),
            FadeIn(dinamici["etichetta_theta"]),
        )
        self.add(dinamici["coseno"], dinamici["seno"])

        pannello = crea_pannello_valori(theta)
        pannello.to_corner(DL, buff=0.5)
        if pannello.get_top()[1] > -R - 0.1:  # troppo alto: toccherebbe il cerchio
            pannello.scale(0.8)
            pannello.to_corner(DL, buff=0.5)
        self.play(FadeIn(pannello))

        # 3. Esplorazione: il seno è l'altezza del punto
        self.play(theta.animate.set_value(PI / 3), run_time=3)
        self.wait(1)

        didascalia = Text(
            "Il seno è l'altezza del punto",
            font_size=34,
            t2c={"seno": COLORE_SENO},
        ).to_edge(UP)
        self.play(FadeIn(didascalia))
        # Circumscribe e non Indicate: Indicate modificherebbe il segmento
        # dinamico, che poi viene ridisegnato ogni frame dall'updater.
        self.play(Circumscribe(dinamici["seno"], color=COLORE_SENO))
        self.wait(2)
        self.play(theta.animate.set_value(5 * PI / 6), run_time=2)
        self.wait(1)
        self.play(theta.animate.set_value(0), run_time=2.5)
        self.play(FadeOut(didascalia))

        # 4. Grafico dell'onda
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1, 1, 1],
            x_length=7.2,
            y_length=2 * R,
            tips=False,
            axis_config={"color": GREY_B},
        )
        axes.shift(ORIGINE_GRAFICO - axes.c2p(0, 0))

        etichette_x = VGroup(
            *[
                MathTex(tex, font_size=28).next_to(axes.c2p(x, 0), DOWN, buff=0.35)
                for x, tex in [
                    (PI / 2, r"\frac{\pi}{2}"),
                    (PI, r"\pi"),
                    (3 * PI / 2, r"\frac{3\pi}{2}"),
                    (2 * PI, r"2\pi"),
                ]
            ]
        )
        self.play(Create(axes), FadeIn(etichette_x), run_time=2)

        didascalia = Text(
            "Registriamo l'altezza mentre l'angolo cresce", font_size=34
        ).to_edge(UP)
        self.play(FadeIn(didascalia))

        def punto_onda_func():
            t = angolo_onda(theta)
            return Dot(axes.c2p(t, np.sin(t)), color=COLORE_SENO, radius=0.08)

        def collegamento_func():
            t = angolo_onda(theta)
            return DashedLine(
                punto_sul_cerchio(theta.get_value(), CENTRO, R),
                axes.c2p(t, np.sin(t)),
                color=GREY_A,
                stroke_width=2,
                dash_length=0.1,
            )

        punto_onda = always_redraw(punto_onda_func)
        collegamento = always_redraw(collegamento_func)
        self.add(collegamento, punto_onda)

        # La traccia parte solo ora: theta è 0, quindi nasce dall'origine del grafico.
        onda = TracedPath(punto_onda.get_center, stroke_color=COLORE_SENO, stroke_width=5)
        self.add(onda)

        # 5. Il giro: 4 quarti di 2.5 s ciascuno, con un lampo a π/2 e 3π/2
        self.play(theta.animate.set_value(PI / 2), run_time=2.5, rate_func=linear)
        formula = MathTex(r"\sin\frac{\pi}{2} = 1", color=COLORE_SENO, font_size=32)
        formula.next_to(punto_onda, UP, buff=0.3)
        self.play(Flash(punto_onda, color=COLORE_SENO), FadeIn(formula))
        self.wait(0.8)
        self.play(FadeOut(formula))

        self.play(theta.animate.set_value(PI), run_time=2.5, rate_func=linear)
        self.play(theta.animate.set_value(3 * PI / 2), run_time=2.5, rate_func=linear)
        formula = MathTex(r"\sin\frac{3\pi}{2} = -1", color=COLORE_SENO, font_size=32)
        formula.next_to(punto_onda, DOWN, buff=0.3)
        self.play(Flash(punto_onda, color=COLORE_SENO), FadeIn(formula))
        self.wait(0.8)
        self.play(FadeOut(formula))

        self.play(theta.animate.set_value(2 * PI), run_time=2.5, rate_func=linear)

        # 6. Rivelazione: la curva esatta del seno
        self.play(FadeOut(didascalia))
        curva = axes.plot(np.sin, x_range=[0, 2 * PI], color=WHITE, stroke_width=2)
        curva_tratteggiata = DashedVMobject(curva, num_dashes=60)
        self.play(Create(curva_tratteggiata), run_time=2)

        etichetta = MathTex(r"y = \sin x", color=COLORE_SENO, font_size=44)
        etichetta.move_to(axes.c2p(2 * PI - 0.9, 1.2))
        self.play(Write(etichetta))

        didascalia = Text(
            "L'onda è il seno dell'angolo!",
            font_size=40,
            t2c={"seno": COLORE_SENO},
        ).to_edge(UP)
        self.play(FadeIn(didascalia))
        self.wait(1)

        # 7. Secondo giro: l'asse arriva solo a 2π, quindi la traccia gialla si toglie
        self.play(FadeOut(onda), run_time=0.5)
        self.play(theta.animate.set_value(4 * PI), run_time=6, rate_func=linear)

        # 8. Chiusura: si tolgono gli updater, così anche gli elementi dinamici sfumano
        self.wait(1)
        for mob in self.mobjects:
            mob.clear_updaters()
        self.play(FadeOut(*self.mobjects), run_time=1.5)
