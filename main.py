from manim import *
import math, random

class ApprossimazioneRadice(Scene):
    def construct(self):
        # STEP 1: Titolo e numero casuale
        title = Text("Approssimazione della radice", font_size=48)
        number = random.randint(1000, 9999)
        n_tex = MathTex(f"N = {number}", font_size=72)

        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))
        self.play(Write(n_tex))
        self.wait(1.5)
        self.play(FadeOut(n_tex))

        # STEP 2: Quadrati perfetti più vicini
        a = int(math.sqrt(number))
        if a * a > number:
            a -= 1
        b = a + 1
        low = a * a
        high = b * b

        squares = MathTex(
            f"{a}^2 = {low}", r"\quad", f"{b}^2 = {high}", font_size=72
        )
        self.play(Write(squares))
        self.wait(2)
        self.play(FadeOut(squares))

        # STEP 3: Differenze
        d1 = number - low
        d2 = high - number
        diff = MathTex(
            r"\Delta_1 = N - a^2 = " + f"{d1}",
            r"\quad\quad",
            r"\Delta_2 = b^2 - N = " + f"{d2}",
            font_size=60
        )
        self.play(Write(diff))
        self.wait(2)
        self.play(FadeOut(diff))

        # STEP 4: Frazione + Approssimazione
        denom = d1 + d2
        frac = d1 / denom if denom != 0 else 0
        approx = a + frac

        frac_tex = MathTex(
            r"\frac{\Delta_1}{\Delta_1 + \Delta_2} = " + f"{frac:.7f}",
            font_size=60
        )
        approx_tex = MathTex(
            r"\sqrt{" + f"{number}" + r"} \approx " +
            f"{a} + {frac:.7f} = {approx:.7f}",
            font_size=60
        )
        group = VGroup(frac_tex, approx_tex).arrange(DOWN, buff=0.7)
        self.play(Write(group))
        self.wait(3)
        self.play(FadeOut(group))

        # STEP 5: Valore reale e confronto
        actual = math.sqrt(number)
        error = abs(actual - approx)

        real_tex = MathTex(
            r"\text{Valore reale: } \sqrt{" + f"{number}" + r"} = " +
            f"{actual:.7f}",
            font_size=60
        )
        error_tex = MathTex(
            r"\text{Errore assoluto } = " + f"{error:.7f}",
            font_size=60
        )
        last_group = VGroup(real_tex, error_tex).arrange(DOWN, buff=0.7)
        self.play(Write(last_group))
        self.wait(3)
