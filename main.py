from manim import *
import numpy as np

config.frame_rate = 60

class PompeiuTheorem(Scene):
    def __init__(self):
        super().__init__()
        self.camera.frame_width = 14
        self.camera.frame_height = 8

    def construct(self):
        self.camera.background_color = BLACK
        
        side_length = 3.0
        height = side_length * np.sqrt(3) / 2
        
        A = np.array([-side_length/2, -height/3, 0])
        B = np.array([side_length/2, -height/3, 0]) 
        C = np.array([0, 2*height/3, 0])
        
        triangle = Polygon(A, B, C, color=BLUE, stroke_width=4)
        
        circumcenter = np.array([0, 0, 0])
        circumradius = np.linalg.norm(A - circumcenter)
        
        circle = Circle(radius=circumradius, color=WHITE, stroke_width=3)
        circle.move_to(circumcenter)
        
        angle_A = np.arctan2(A[1], A[0])
        angle_B = np.arctan2(B[1], B[0])
        
        start_angle = (angle_A + angle_B) / 2
        
        P = circle.point_at_angle(start_angle)
        
        PA = Line(P, A, color=RED, stroke_width=4)
        PB = Line(P, B, color=GREEN, stroke_width=4)  
        PC = Line(P, C, color=YELLOW, stroke_width=4)
        
        dot_A = Dot(A, color=WHITE, radius=0.08)
        dot_B = Dot(B, color=WHITE, radius=0.08)
        dot_C = Dot(C, color=WHITE, radius=0.08)
        dot_P = Dot(P, color=WHITE, radius=0.1)
        
        label_A = Text("A", font_size=24, color=WHITE).next_to(A, LEFT+DOWN*0.25)
        label_B = Text("B", font_size=24, color=WHITE).next_to(B, RIGHT + DOWN*0.25)
        label_C = Text("C", font_size=24, color=WHITE).next_to(C, UP)
        
        self.play(Create(circle), run_time=1.5)
        self.play(Create(triangle), run_time=1.5)
        self.play(
            Create(dot_A), Write(label_A),
            Create(dot_B), Write(label_B), 
            Create(dot_C), Write(label_C),
            run_time=1
        )
        self.wait(1)
        
        self.play(Create(dot_P))
        self.play(
            Create(PA),
            Create(PB),
            Create(PC),
        )
        
        c_label = Text("c", font_size=20, color=YELLOW)
        a_label = Text("a", font_size=20, color=RED)
        b_label = Text("b", font_size=20, color=GREEN)
        
        def update_c_label(mob):
            center = PC.get_center()
            mob.move_to(center).shift(LEFT * 0.15)
        
        def update_a_label(mob):
            mob.move_to(PA.get_center()).shift(DOWN * 0.25)
        
        def update_b_label(mob):
            mob.move_to(PB.get_center()).shift(DOWN * 0.25)
        
        update_c_label(c_label)
        update_a_label(a_label)
        update_b_label(b_label)
        
        c_label.add_updater(update_c_label)
        a_label.add_updater(update_a_label)
        b_label.add_updater(update_b_label)
        
        self.play(Create(c_label), Create(a_label), Create(b_label))
        self.wait(2)
        
        theorem_text = MathTex("a+b=c", font_size=42, color=WHITE).next_to((A+B)/2, DOWN, buff=1.5)
        
        self.play(Write(theorem_text), run_time=1.5)
        self.wait(2)
        
        gap = 0.3
        
        if angle_A < angle_B:
            start_arc = angle_A + gap
            end_arc = angle_B - gap
        else:
            start_arc = angle_B + gap
            end_arc = angle_A - gap
        
        num_cycles = 3
        all_angles = np.array([])
        
        angles1 = np.linspace(start_angle, end_arc, 20)
        angles2 = np.linspace(end_arc, start_arc, 20)
        angles3 = np.linspace(start_arc, end_arc, 20)
        angles4 = np.linspace(end_arc, start_angle, 20)
        
        all_angles = np.concatenate([angles1, angles2, angles3, angles4])
        
        for new_angle in all_angles:
            new_P = circle.point_at_angle(new_angle)
            
            new_PA = Line(new_P, A, color=RED, stroke_width=4)
            new_PB = Line(new_P, B, color=GREEN, stroke_width=4)
            new_PC = Line(new_P, C, color=YELLOW, stroke_width=4)
            
            self.play(
                Transform(PA, new_PA),
                Transform(PB, new_PB),
                Transform(PC, new_PC),
                dot_P.animate.move_to(new_P),
                run_time=0.04
            )
        
        c_label.clear_updaters()
        a_label.clear_updaters()
        b_label.clear_updaters()

        theorem_box = SurroundingRectangle(theorem_text, color=WHITE, buff=0.3, stroke_width=3)
        self.play(Create(theorem_box))
        self.wait(3)

#manim main.py PompeiuTheorem -qh