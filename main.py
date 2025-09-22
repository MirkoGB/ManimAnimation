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


class PrimoAnnoMatematica(Scene):
    def construct(self):
        self.show_title()
        self.introduce_natural_numbers()
        self.explore_number_line()
        self.highlight_operations()
        self.present_properties()
        self.explain_fractions()
        self.conclusion()

    def show_title(self):
        title = Text("Matematica di Prima Superiore", font_size=60, weight=BOLD)
        subtitle = Text("Numeri, operazioni e primi ragionamenti", font_size=36)
        subtitle.next_to(title, DOWN)
        intro_group = VGroup(title, subtitle).move_to(ORIGIN)

        self.play(FadeIn(title, shift=UP * 0.5))
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(intro_group, shift=UP))

    def introduce_natural_numbers(self):
        section_title = Text("Numeri naturali", font_size=48).to_edge(UP)
        natural_set = MathTex(r"\mathbb{N} = \{0, 1, 2, 3, \ldots\}", font_size=60)
        natural_set.next_to(section_title, DOWN, buff=0.5)
        description = Tex("Sono i numeri che usiamo per contare gli oggetti.", font_size=36)
        description.next_to(natural_set, DOWN)

        numbers = [MathTex(str(n), font_size=48) for n in range(5)]
        numbers.append(MathTex("\\cdots", font_size=48))
        natural_examples = VGroup(*numbers).arrange(RIGHT, buff=0.7)
        natural_examples.next_to(description, DOWN, buff=0.8)

        self.play(Write(section_title))
        self.play(Write(natural_set))
        self.play(FadeIn(description, shift=UP * 0.3))
        self.play(LaggedStart(*[FadeIn(num, shift=UP * 0.4) for num in natural_examples], lag_ratio=0.25))
        self.wait(1.5)

        highlight_box = SurroundingRectangle(natural_examples[0], buff=0.2, color=YELLOW)
        self.play(Create(highlight_box))
        comment = Tex("Lo zero rappresenta l'assenza di oggetti.", font_size=34, color=YELLOW)
        comment.next_to(highlight_box, DOWN, buff=0.3)
        self.play(Write(comment))
        self.wait(2)

        self.play(FadeOut(VGroup(section_title, natural_set, description, natural_examples, highlight_box, comment)))

    def explore_number_line(self):
        title = Text("La retta dei numeri", font_size=48).to_edge(UP)
        number_line = NumberLine(x_range=[-5, 7, 1], include_numbers=True, length=10)
        number_line.shift(DOWN * 0.5)

        self.play(FadeIn(title, shift=UP * 0.3))
        self.play(Create(number_line))

        positive_brace = BraceBetweenPoints(number_line.n2p(0), number_line.n2p(5), direction=UP)
        positive_label = positive_brace.get_text("Numeri naturali e interi positivi", font_size=32)
        negative_brace = BraceBetweenPoints(number_line.n2p(-4), number_line.n2p(0), direction=DOWN)
        negative_label = negative_brace.get_text("Interi negativi", font_size=32)

        self.play(GrowFromCenter(positive_brace), FadeIn(positive_label, shift=UP * 0.2))
        self.play(GrowFromCenter(negative_brace), FadeIn(negative_label, shift=DOWN * 0.2))
        self.wait(2)

        self.number_line_group = VGroup(title, number_line, positive_brace, positive_label, negative_brace, negative_label)

    def highlight_operations(self):
        title, number_line, *_ = self.number_line_group
        add_title = Text("Addizione: spostarsi verso destra", font_size=40).to_edge(UP)
        self.play(Transform(title, add_title))

        start_value = 2
        step = 3
        start_dot = Dot(number_line.n2p(start_value), color=BLUE)
        self.play(FadeIn(start_dot))

        arrow = Arrow(number_line.n2p(start_value), number_line.n2p(start_value + step), buff=0, color=BLUE)
        addition_equation = MathTex(f"{start_value} + {step} = {start_value + step}", font_size=54)
        addition_equation.next_to(title, DOWN)

        self.play(GrowArrow(arrow))
        self.play(start_dot.animate.move_to(number_line.n2p(start_value + step)))
        self.play(Write(addition_equation))
        self.wait(1.5)

        sub_title = Text("Sottrazione: tornare indietro", font_size=40).to_edge(UP)
        self.play(Transform(title, sub_title))

        new_start = 4
        shift = 3
        self.play(start_dot.animate.move_to(number_line.n2p(new_start)))
        self.play(FadeOut(arrow), FadeOut(addition_equation))

        sub_arrow = Arrow(number_line.n2p(new_start), number_line.n2p(new_start - shift), buff=0, color=RED)
        subtraction_equation = MathTex(f"{new_start} - {shift} = {new_start - shift}", font_size=54)
        subtraction_equation.next_to(title, DOWN)

        self.play(GrowArrow(sub_arrow))
        self.play(start_dot.animate.move_to(number_line.n2p(new_start - shift)))
        self.play(Write(subtraction_equation))
        self.wait(2)

        self.play(FadeOut(VGroup(start_dot, sub_arrow, subtraction_equation)))
        self.current_title = title

    def present_properties(self):
        title = self.current_title
        properties_title = Text("Proprietà fondamentali", font_size=44).to_edge(UP)
        self.play(Transform(title, properties_title))

        _, number_line, positive_brace, positive_label, negative_brace, negative_label = self.number_line_group
        self.play(FadeOut(VGroup(number_line, positive_brace, positive_label, negative_brace, negative_label)))

        properties = VGroup(
            Tex(r"Commutativa: $a + b = b + a$", font_size=38, color=BLUE),
            Tex(r"Associativa: $(a + b) + c = a + (b + c)$", font_size=38, color=GREEN),
            Tex(r"Elemento neutro: $a + 0 = a$", font_size=38, color=YELLOW),
            Tex(r"Distributiva: $a \cdot (b + c) = a b + a c$", font_size=38, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        properties.move_to(DOWN * 0.5)

        box = SurroundingRectangle(properties, buff=0.5, color=WHITE)

        self.play(Create(box))
        self.play(LaggedStart(*[Write(prop) for prop in properties], lag_ratio=0.3))
        self.wait(2)
        self.play(FadeOut(VGroup(box, properties)))

        self.current_title = title

    def explain_fractions(self):
        title = self.current_title
        fraction_title = Text("Frazioni: dividere l'intero", font_size=44).to_edge(UP)
        self.play(Transform(title, fraction_title))

        fraction_tex = MathTex(r"\frac{3}{4}", font_size=78, color=YELLOW)
        fraction_tex.to_edge(RIGHT, buff=1.5)

        sectors = VGroup()
        colors = [BLUE, BLUE, BLUE, GREY]
        for i in range(4):
            sector = Sector(
                outer_radius=1.7,
                start_angle=i * PI / 2,
                angle=PI / 2,
                color=colors[i],
                fill_opacity=0.6 if i < 3 else 0.15,
                stroke_width=2,
            )
            sectors.add(sector)
        sectors.shift(LEFT * 3)

        circle_outline = Circle(radius=1.7, color=WHITE, stroke_width=2).move_to(sectors)
        labels = VGroup(
            Tex("4 parti uguali", font_size=32).next_to(circle_outline, DOWN),
            Tex("Ne coloriamo 3: otteniamo i 3/4", font_size=32).next_to(fraction_tex, DOWN),
        )

        self.play(FadeIn(sectors))
        self.play(Create(circle_outline))
        self.play(Write(fraction_tex))
        self.play(LaggedStart(*[FadeIn(label, shift=UP * 0.3) for label in labels], lag_ratio=0.2))
        self.wait(1.5)

        fraction_line = NumberLine(x_range=[0, 1, 0.25], include_numbers=True, length=8)
        fraction_line.next_to(labels[0], DOWN, buff=1.2)

        brace = BraceBetweenPoints(fraction_line.n2p(0), fraction_line.n2p(0.75), direction=UP)
        brace_text = brace.get_text("Tre quarti sulla retta", font_size=32)
        point = Dot(fraction_line.n2p(0.75), color=YELLOW)

        self.play(Create(fraction_line))
        self.play(GrowFromCenter(brace), FadeIn(brace_text))
        self.play(FadeIn(point))
        self.wait(2)

        self.play(FadeOut(VGroup(sectors, circle_outline, fraction_tex, labels, fraction_line, brace, brace_text, point)))
        self.current_title = title

    def conclusion(self):
        title = self.current_title
        summary_title = Text("Cosa portare con sé", font_size=44).to_edge(UP)
        self.play(Transform(title, summary_title))

        raw_points = [
            "Contare con i numeri naturali.",
            "Rappresentare i numeri sulla retta.",
            "Capire addizione e sottrazione come movimenti.",
            "Dividere un intero in parti uguali con le frazioni.",
        ]
        summary_pairs = VGroup()
        for text in raw_points:
            checkmark = Tex("\\checkmark", font_size=36, color=GREEN)
            point_text = Tex(text, font_size=36)
            pair = VGroup(checkmark, point_text).arrange(RIGHT, buff=0.3, aligned_edge=UP)
            summary_pairs.add(pair)

        summary_pairs.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        summary_pairs.move_to(DOWN * 0.5)

        self.play(LaggedStart(*[FadeIn(pair, shift=RIGHT * 0.2) for pair in summary_pairs], lag_ratio=0.2))
        self.wait(2)
        closing = Text("Pronti per le prossime scoperte?", font_size=42, color=YELLOW)
        closing.next_to(summary_pairs, DOWN, buff=0.8)
        self.play(Write(closing))
        self.wait(2.5)
