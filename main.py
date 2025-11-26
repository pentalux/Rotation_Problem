from manim import *
import numpy as np

config.frame_rate = 60

class GeometryProblem(Scene):
    def __init__(self):
        super().__init__()
        self.camera.frame_width = 24.5
        self.camera.frame_height = 14

    def construct(self):
        self.camera.background_color = BLACK
        
        # Создаем квадрат ABCD
        side_length = 5.0
        A = np.array([-side_length/2, side_length/2, 0])
        B = np.array([side_length/2, side_length/2, 0])
        C = np.array([side_length/2, -side_length/2, 0])
        D = np.array([-side_length/2, -side_length/2, 0])
        
        # Создаем квадрат
        square = Polygon(A, B, C, D, color=BLUE, stroke_width=4)
        
        # Добавляем точки F на DC и E на BC
        F_pos = D + 0.6 * (C - D)  # F находится на 60% от D к C
        E_pos = B + 0.4 * (C - B)  # E находится на 40% от B к C
        
        # Создаем отрезки из A в E и A в F
        AE = Line(A, E_pos, color=WHITE, stroke_width=4)
        AF = Line(A, F_pos, color=WHITE, stroke_width=4)
        
        # Создаем отрезок EF
        EF = Line(E_pos, F_pos, color=WHITE, stroke_width=4)
        
        # Создаем треугольник AEF
        triangle_AEF = Polygon(A, E_pos, F_pos, color=RED, stroke_width=4, fill_color=RED, fill_opacity=0.3)
        
        # Создаем треугольник ABE (белый без заливки)
        triangle_ABE = Polygon(A, B, E_pos, color=WHITE, stroke_width=4)
        
        # Создаем точки
        dot_A = Dot(A, color=WHITE, radius=0.08)
        dot_B = Dot(B, color=WHITE, radius=0.08)
        dot_C = Dot(C, color=WHITE, radius=0.08)
        dot_D = Dot(D, color=WHITE, radius=0.08)
        dot_E = Dot(E_pos, color=WHITE, radius=0.08)
        dot_F = Dot(F_pos, color=WHITE, radius=0.08)
        
        # Подписи точек
        label_A = Text("A", font_size=24, color=WHITE).next_to(A, UP + LEFT, buff=0.15)
        label_B = Text("B", font_size=24, color=WHITE).next_to(B, UP + RIGHT, buff=0.15)
        label_C = Text("C", font_size=24, color=WHITE).next_to(C, DOWN + RIGHT, buff=0.15)
        label_D = Text("D", font_size=24, color=WHITE).next_to(D, DOWN + LEFT, buff=0.15)
        label_E = Text("E", font_size=24, color=WHITE).next_to(E_pos, RIGHT, buff=0.15)
        label_F = Text("F", font_size=24, color=WHITE).next_to(F_pos, DOWN, buff=0.15)
        
        # === ПОСТРОЕНИЕ ГЕОМЕТРИИ ===
        self.play(Create(square))
        self.play(
            Create(dot_A), Write(label_A),
            Create(dot_B), Write(label_B),
            Create(dot_C), Write(label_C),
            Create(dot_D), Write(label_D)
        )
        self.wait(2)
        
        # Показываем точки E и F
        self.play(
            Create(dot_E), Write(label_E),
            Create(dot_F), Write(label_F)
        )
        self.wait(2)
        
        # Показываем отрезки из A в E и A в F одновременно
        self.play(
            Create(AE),
            Create(AF),
            Create(EF),
        )
        self.wait(2)
        
        # Показываем угол EAF = 45° - ПРАВИЛЬНАЯ ДУГА
        angle_radius = 0.8
        # Вычисляем углы для лучей AE и AF
        vector_AE = E_pos - A
        vector_AF = F_pos - A
        angle_AE = np.arctan2(vector_AE[1], vector_AE[0])
        angle_AF = np.arctan2(vector_AF[1], vector_AF[0])
        
        # Создаем правильную дугу угла
        angle_EAF = Arc(
            radius=angle_radius,
            start_angle=angle_AE,
            angle=angle_AF - angle_AE,
            color=YELLOW,
            stroke_width=4
        ).move_arc_center_to(A)
        
        self.play(Create(angle_EAF))
        self.wait(2)
        
        
        # === ЧИСЛЕННЫЕ ЗНАЧЕНИЯ ===
        
        # Длина EF = 17 (зеленый)
        EF_label = MathTex("17", font_size=24, color=WHITE)
        EF_label.next_to(EF.get_center(), DOWN+RIGHT)
        
        # Угол 45° (желтый)
        angle_label = MathTex("45^\\circ", font_size=24, color=YELLOW)
        # Размещаем метку угла на дуге
        mid_angle = (angle_AE + angle_AF) / 2
        angle_label.move_to(A + (angle_radius + 0.3) * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))
        
        # Площадь треугольника AEF = 170 (красный)
        area_label = MathTex("170", font_size=32, color=WHITE)
        area_label.move_to(triangle_AEF.get_center(), LEFT+UP)
        
        self.play(
        Write(EF_label),
        Write(angle_label),
        Write(area_label)
        )

        self.wait(2)

        # === УСЛОВИЕ ЗАДАЧИ СПРАВА ===
        conditions_text = VGroup(
            MathTex("\\angle FAE=45^\\circ"),
            MathTex("S_{\\triangle FAE}=170"), 
            MathTex("FE=17"),
            MathTex("AD-?", color = RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Позиционируем справа от отрезка BC
        conditions_text.next_to(B, RIGHT+DOWN*0.8, buff=2.0)

        # Fadeout численных значений и дуги угла, показ условия
        self.play(
            FadeOut(EF_label),
            FadeOut(angle_label), 
            FadeOut(area_label),
            FadeOut(angle_EAF),
            Write(conditions_text)
        )
        
        self.wait(2)
        
        # === ДОПОЛНИТЕЛЬНЫЕ УГЛЫ ===
        
        # Угол DAF (α) - оранжевый
        angle_DAF_radius = 1.4
        vector_AD = D - A
        vector_AF_2 = F_pos - A
        angle_AD = np.arctan2(vector_AD[1], vector_AD[0])
        angle_AF_2 = np.arctan2(vector_AF_2[1], vector_AF_2[0])
        
        angle_DAF = Arc(
            radius=angle_DAF_radius,
            start_angle=angle_AD,
            angle=angle_AF_2 - angle_AD,
            color=ORANGE,
            stroke_width=4
        ).move_arc_center_to(A)
        
        alpha_label = MathTex("\\alpha", font_size=36, color=ORANGE)
        alpha_mid_angle = (angle_AD + angle_AF_2) / 2
        alpha_label.move_to(A + (angle_DAF_radius + 0.3) * np.array([np.cos(alpha_mid_angle), np.sin(alpha_mid_angle), 0]))
        
        # Угол EAB (β) - фиолетовый
        angle_EAB_radius = 1.4
        vector_AB = B - A
        vector_AE_2 = E_pos - A
        angle_AB = np.arctan2(vector_AB[1], vector_AB[0])
        angle_AE_2 = np.arctan2(vector_AE_2[1], vector_AE_2[0])
        
        angle_EAB = Arc(
            radius=angle_EAB_radius,
            start_angle=angle_AB,
            angle=angle_AE_2 - angle_AB,
            color=PURPLE,
            stroke_width=4
        ).move_arc_center_to(A)
        
        beta_label = MathTex("\\beta", font_size=36, color=PURPLE)
        beta_mid_angle = (angle_AB + angle_AE_2) / 2
        beta_label.move_to(A + (angle_EAB_radius + 0.3) * np.array([np.cos(beta_mid_angle), np.sin(beta_mid_angle), 0]))
        
        self.play(
            Create(angle_DAF),
            Write(alpha_label),
            Create(angle_EAB),
            Write(beta_label)
        )
        
        self.wait(2)
        
        # === ВЫДЕЛЕНИЕ ТРЕУГОЛЬНИКА ABE ПУНКТИРОМ ===
        
        # Группируем все объекты кроме условия
        all_objects_except_conditions = VGroup(AE, AF, EF,
            dot_A, dot_B, dot_C, dot_D, dot_E, dot_F,
            label_A, label_B, label_C, label_D, label_E, label_F,
            angle_DAF, angle_EAB, alpha_label, beta_label
        )

        # Уменьшаем opacity до 30%
        self.play(
            all_objects_except_conditions.animate.set_opacity(0.3)
        )


        # Создаем пунктирную версию треугольника ABE
        triangle_ABE_dashed = DashedVMobject(
            Polygon(A, B, E_pos, color=RED, stroke_width=4),
            num_dashes=75
        )
        
        # Показываем треугольник ABE пунктиром
        self.play(Create(triangle_ABE_dashed))
        self.wait(2)
        
        # === АНИМАЦИЯ СТРЕЛКИ ВРАЩЕНИЯ ===
        
        # Создаем стрелку вращения
        arrow_radius = 1.2
        final_angle = -PI/2  # 90 градусов по часовой стрелке
        
        # Создаем финальную стрелку (дуга + стрелочка)
        rotation_arc = Arc(
            radius=arrow_radius,
            start_angle=0,
            angle=final_angle,
            color=YELLOW,
            stroke_width=5
        ).move_arc_center_to(A)
        
        rotation_arrow_tip = Triangle(color=YELLOW, fill_opacity=1, stroke_width=0)
        rotation_arrow_tip.set_height(0.2)
        rotation_arrow_tip.rotate(final_angle + PI/2)
        rotation_arrow_tip.move_to(A + arrow_radius * np.array([np.cos(final_angle), np.sin(final_angle), 0]))
        
        rotation_group = VGroup(rotation_arc, rotation_arrow_tip)
        
        
        # Показываем стрелку вращения
        self.play(
            Create(rotation_arc),
            Create(rotation_arrow_tip)
        )
        
        self.wait(2)
        
        # === АНИМАЦИЯ ПОВОРОТА ТРЕУГОЛЬНИКА ===
        
        rotation_text = MathTex("\\triangle ABE \\rightarrow \\triangle AE'B'", font_size=40, color=WHITE)
        rotation_text.next_to(square, DOWN, buff=0.8)

        # Убираем стрелку вращения
        self.play(
            FadeOut(rotation_group),    
            Write(rotation_text)
        )
        
        self.wait(2)

        # Поворачиваем пунктирный треугольник ABE
        self.play(
            Rotate(triangle_ABE_dashed, angle=-PI/2, about_point=A),

            )
        

        # Добавляем подписи B' и E' после поворота
        B_prime_label = Text("(B')", font_size=24, color=WHITE)
        E_prime_label = Text("E'", font_size=24, color=WHITE)
        
        # Вычисляем позиции после поворота
        def rotate_point(point, center, angle):
            translated = point - center
            rotated_x = translated[0] * np.cos(angle) - translated[1] * np.sin(angle)
            rotated_y = translated[0] * np.sin(angle) + translated[1] * np.cos(angle)
            return center + np.array([rotated_x, rotated_y, 0])
        
        B_rotated = rotate_point(B, A, -PI/2)
        E_rotated = rotate_point(E_pos, A, -PI/2)
        
        B_prime_label.next_to(label_D, RIGHT, buff = 0.15)
        E_prime_label.next_to(label_D, LEFT, buff = 1.75)
        
        def rotate_point(point, center, angle):
            translated = point - center
            rotated_x = translated[0] * np.cos(angle) - translated[1] * np.sin(angle)
            rotated_y = translated[0] * np.sin(angle) + translated[1] * np.cos(angle)
            return center + np.array([rotated_x, rotated_y, 0])

        B_rotated = rotate_point(B, A, -PI/2)
        E_rotated = rotate_point(E_pos, A, -PI/2)

        # Создаем белую пунктирную версию треугольника ABE с новыми координатами
        triangle_ABE_white_dashed = DashedVMobject(
            Polygon(A, B_rotated, E_rotated, color=WHITE, stroke_width=4),
            num_dashes=75
        )

        self.play(
            Transform(triangle_ABE_dashed, triangle_ABE_white_dashed),
            all_objects_except_conditions.animate.set_opacity(1.0),
            Write(B_prime_label),
            Write(E_prime_label)
        )
        
        self.wait(2)

        # Угол E'AD (β) - фиолетовый такой же как EAB
        angle_E_prime_AD_radius = 1.4
        vector_AD_2 = D - A
        vector_AE_prime = E_rotated - A
        angle_AD_2 = np.arctan2(vector_AD_2[1], vector_AD_2[0])
        angle_AE_prime = np.arctan2(vector_AE_prime[1], vector_AE_prime[0])

        angle_E_prime_AD = Arc(
            radius=angle_E_prime_AD_radius,
            start_angle=angle_AD_2,
            angle=angle_AE_prime - angle_AD_2,
            color=PURPLE,
            stroke_width=4
        ).move_arc_center_to(A)

        beta_prime_label = MathTex("\\beta", font_size=36, color=PURPLE)
        beta_prime_mid_angle = (angle_AD_2 + angle_AE_prime) / 2
        beta_prime_label.move_to(A + (angle_E_prime_AD_radius + 0.3) * np.array([np.cos(beta_prime_mid_angle), np.sin(beta_prime_mid_angle), 0]))

        self.play(
            Create(angle_E_prime_AD),
            Write(beta_prime_label)
        )

        
       # Отмечаем равенство сторон AE и AE' одной риской (поперек отрезков)
        # Рисуем риски перпендикулярно сторонам AE и AE'
        AE_midpoint = (A + E_pos) / 2
        AE_prime_midpoint = (A + E_rotated) / 2

        # Перпендикулярные векторы для рисок (разные для AE и AE')
        AE_direction = normalize(E_pos - A)
        AE_perpendicular = np.array([-AE_direction[1], AE_direction[0], 0]) * 0.15

        AE_prime_direction = normalize(E_rotated - A)
        AE_prime_perpendicular = np.array([-AE_prime_direction[1], AE_prime_direction[0], 0]) * 0.15

        AE_mark = Line(
            AE_midpoint + AE_perpendicular,
            AE_midpoint - AE_perpendicular,
            color=YELLOW, stroke_width=3
        )
        AE_prime_mark = Line(
            AE_prime_midpoint + AE_prime_perpendicular,
            AE_prime_midpoint - AE_prime_perpendicular,
            color=YELLOW, stroke_width=3
        )

        self.play(
            Create(AE_mark),
            Create(AE_prime_mark)
        )
        # Сначала E'A = AE и AF - common
        additional_text1 = MathTex("E'A = AE", font_size=40, color=WHITE)
        additional_text1.next_to(rotation_text, DOWN+LEFT, buff=0.3)

        additional_text2 = MathTex("AF - \\text{common}", font_size=40, color=WHITE)
        additional_text2.next_to(additional_text1, DOWN, buff=0.2)

        self.play(
            Write(additional_text1),
            Write(additional_text2),
            run_time=1
        )

        self.wait(2)
        # Перекрашиваем существующие дуги E'AD и DAF в желтый и меняем подписи
        self.play(
            angle_E_prime_AD.animate.set_color(YELLOW),
            angle_DAF.animate.set_color(YELLOW),
            FadeOut(beta_prime_label),
            FadeOut(alpha_label)
        )

        # Создаем общую подпись 45° для объединенного угла
        unified_angle_label = MathTex("45^\\circ", font_size=24, color=YELLOW)
        unified_mid_angle = (angle_AD_2 + angle_AF_2) / 2
        unified_angle_label.move_to(A + (1.4 + 0.3) * np.array([np.cos(unified_mid_angle), np.sin(unified_mid_angle), 0]))



        self.play(
            Write(unified_angle_label)
        )


        self.wait(1)


        # Потом угол E'AF = углу FAB
        additional_text3 = MathTex("\\angle E'AF = \\angle FAE", font_size=40, color=WHITE)
        additional_text3.next_to(additional_text2, DOWN, buff=0.3)

        self.play(
            Write(additional_text3),
            run_time=1
        )

        self.wait(2)

        # Штриховка треугольника E'AF (простая заливка)
        hatch_E_prime_AF = Polygon(A, E_rotated, F_pos, color=YELLOW, stroke_width=2,
                                fill_color=YELLOW, fill_opacity=0.3)

        # Штриховка треугольника AFE (простая заливка)  
        hatch_AFE = Polygon(A, F_pos, E_pos, color=RED, stroke_width=2,
                        fill_color=RED, fill_opacity=0.3)

        vertical_line = Line(
            additional_text1.get_top() + RIGHT * 2,
            additional_text3.get_bottom() + RIGHT * 2,
            color=WHITE, stroke_width=2
        )

        # Текст справа от черты
        conclusion_text = MathTex("\\triangle AE'F = \\triangle AFE", font_size=40, color=WHITE)
        conclusion_text.next_to(vertical_line, RIGHT, buff=0.3)

        implication_text = MathTex("\\Rightarrow", font_size=36, color=WHITE)
        implication_text.next_to(conclusion_text, RIGHT, buff=0.2)

        result_text = MathTex("FE' = FE = 17", font_size=40, color=WHITE)
        result_text.next_to(implication_text, RIGHT, buff=0.2)


        self.play(
            Create(vertical_line),
            Write(conclusion_text),
            Write(implication_text),
            Write(result_text),
            Create(hatch_E_prime_AF),
            Create(hatch_AFE)
        )
        # Штриховка треугольника E'AF (простая заливка)
        hatch_E_prime_AF1 = Polygon(A, E_rotated, F_pos, color=YELLOW, stroke_width=2,
                                fill_color=YELLOW, fill_opacity=0)

        # Штриховка треугольника AFE (простая заливка)  
        hatch_AFE1 = Polygon(A, F_pos, E_pos, color=RED, stroke_width=2,
                        fill_color=RED, fill_opacity=0)
        
        self.wait(3)
        
        self.play(
            FadeOut(hatch_E_prime_AF),
            FadeOut(hatch_AFE),
        )

        # Группируем все надписи под задачей
        all_bottom_text = VGroup(
            rotation_text,
            additional_text1,
            additional_text2, 
            additional_text3,
            vertical_line,
            conclusion_text,
            implication_text,
            result_text
        )

        # Fadeout всех надписей
        self.play(
            FadeOut(all_bottom_text),
            run_time=1
        )

        # Пишем новое уравнение
        equation_text = MathTex("S_{\\triangle AE'B'} = \\frac{1}{2} \\cdot AD \\cdot E'F = 170", font_size=40, color=WHITE)
        equation_text.next_to(E_rotated, DOWN+RIGHT*0.4, buff=0.8)

        # Стрелка следствия и ответ
        implication_arrow = MathTex("\\Rightarrow", font_size=36, color=WHITE)
        answer_text = MathTex("\\text{Answer: } AD = 20", font_size=48, color=WHITE)

        # Позиционируем
        equation_text.next_to(E_rotated, DOWN+RIGHT*0.4, buff=0.8)
        implication_arrow.next_to(equation_text, RIGHT, buff=0.3)
        answer_text.next_to(implication_arrow, RIGHT, buff=0.5)

        # Показываем уравнение и стрелку
        self.play(
            Write(equation_text),
            Write(implication_arrow),
            run_time=1
        )

        # Показываем ответ и обводим в прямоугольник
        self.play(
            Write(answer_text),
            run_time=1
        )

        answer_box = SurroundingRectangle(answer_text, color=WHITE, buff=0.3, stroke_width=3)
        self.play(
            Create(answer_box),
            run_time=1
        )

        self.wait(2)

        answer_group = VGroup(answer_text, answer_box)

        # Fadeout уравнения и сдвигаем группу ответа на его место
        self.play(
            FadeOut(equation_text),
            FadeOut(implication_arrow),
            answer_group.animate.next_to(square, DOWN, buff=0.8),
            run_time=1
        )

        self.wait(3)

        self.wait(3)


# Для рендеринга используйте:
# manim -pqh main.py GeometryProblem