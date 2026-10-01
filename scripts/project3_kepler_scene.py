"""Captioned Kepler films, rendered with Manim Community 0.19.0.

Render from the course root:
    python -m manim --media_dir /private/tmp/comp521-kepler-render -r 1920,1080 --fps 30 --disable_caching scripts/project3_kepler_scene.py Project3Kepler Project3Orientation

The films use the existing e = 0.55 example and E = pi/3 snapshot.
Frame timestamps are written to /private/tmp/comp521-kepler-timing.json.
"""
import json
from pathlib import Path
import numpy as np
from manim import (
    Arc, Arrow, Arrow3D, Circle, Create, DashedVMobject, Dot, Ellipse,
    FadeIn, FadeOut, LaggedStart, Line, MathTex, ParametricFunction,
    Polygon, Scene, Square, Text, ThreeDScene, Transform,
    UpdateFromAlphaFunc, VGroup, Write, linear,
)
from scripts.generate_project3_orbit_media import ECCENTRICITY, eccentric_anomaly, position

NIGHT, INK, MUTED = "#0B1220", "#EDF2FA", "#ACBAD0"
CLOCK, ECC, TRUE, ORBIT, STAR = "#B8A5FF", "#64D6E5", "#FFB777", "#89B4E8", "#FFCF87"
TIMING = Path("/private/tmp/comp521-kepler-timing.json")


def text(value, size=28, color=INK):
    return Text(value, font="DejaVu Sans", font_size=size, color=color)


def glowing_dot(point, color=STAR, radius=0.075):
    return VGroup(
        Dot(point, radius=radius*3.8, color=color).set_opacity(0.025),
        Dot(point, radius=radius*2.8, color=color).set_opacity(0.05),
        Dot(point, radius=radius*1.8, color=color).set_opacity(0.10),
        Dot(point, radius=radius, color=color),
    )


class Project3Kepler(Scene):
    def construct(self):
        self.camera.background_color = NIGHT
        a, e = 2.15, ECCENTRICITY
        center = np.array([2.20, -0.25, 0.0])
        focus = center + [a*e, 0, 0]
        clock_center = np.array([-4.55, -0.25, 0])
        chosen_e = np.pi/3
        chosen_m = chosen_e-e*np.sin(chosen_e)
        true = np.arctan2(*position(chosen_m)[[1, 0]])
        timing = {}

        def planet_at(mean):
            return focus+a*np.append(position(mean), 0)

        def hand_tip(mean):
            return clock_center+1.03*np.array([np.cos(mean), np.sin(mean), 0])

        title = text("One planet. One instant. Three descriptions.", 34).move_to([0, 3.58, 0])
        caption = text("Predict: where will equal-time dots cluster?", 27).move_to([0, 2.92, 0])
        step = text("01 / THE CLOCK", 19, CLOCK).move_to([-4.5, 2.18, 0])
        orbit = Ellipse(width=2*a, height=2*a*np.sqrt(1-e*e),
                        color=ORBIT, stroke_width=3).move_to(center)
        planet = glowing_dot(planet_at(0), INK, 0.065)
        star = glowing_dot(focus, STAR, 0.10)
        clock = Circle(radius=1.03, color=CLOCK, stroke_width=2).move_to(clock_center)
        clock_dot = Dot(clock_center, radius=0.035, color=CLOCK)
        hand = Arrow(clock_center, hand_tip(0), buff=0, color=CLOCK,
                     stroke_width=3, max_tip_length_to_length_ratio=0.12)
        ticks = VGroup(*[
            text(value, 20, MUTED).move_to(clock_center+1.42*np.array([np.cos(angle), np.sin(angle), 0]))
            for angle, value in zip([0, np.pi/2, np.pi, 3*np.pi/2], ["0", "P/4", "P/2", "3P/4"])
        ])
        clock_eq = MathTex(r"M=\frac{2\pi t}{P}", font_size=30, color=CLOCK).move_to([-4.55,1.65,0])
        peri = text("Periastron", 20, MUTED).move_to(center+[a+0.80,0,0])
        apa = text("Apastron", 20, MUTED).move_to(center+[-a-0.75,0,0])
        orbit_title = text("THE PLANET CHANGES SPEED", 19, MUTED).move_to([2.4,2.18,0])
        self.add(title, caption, step)
        self.play(LaggedStart(Create(clock), Create(orbit), FadeIn(star), FadeIn(planet),
                              FadeIn(ticks), FadeIn(peri), FadeIn(apa), lag_ratio=0.12), run_time=2)
        self.play(Create(hand), FadeIn(clock_dot), Write(clock_eq), FadeIn(orbit_title), run_time=1)
        self.wait(3)

        def say(value):
            nonlocal caption
            replacement = text(value, 26).move_to([0,2.92,0])
            self.play(Transform(caption, replacement), run_time=0.35)

        def chapter(value, color):
            self.play(Transform(step, text(value,19,color).move_to([-4.5,2.18,0])), run_time=0.4)

        def move(start, end, seconds):
            def update_planet(mob, alpha):
                mob.move_to(planet_at(start+alpha*(end-start)))
            def update_hand(mob, alpha):
                mob.become(Arrow(clock_center, hand_tip(start+alpha*(end-start)), buff=0,
                                 color=CLOCK, stroke_width=3, max_tip_length_to_length_ratio=0.12))
            self.play(UpdateFromAlphaFunc(planet,update_planet),
                      UpdateFromAlphaFunc(hand,update_hand), run_time=seconds, rate_func=linear)

        dots = VGroup(Dot(planet_at(0), radius=0.04, color=ORBIT))
        self.add(dots)
        say("The clock is uniform. The planet covers different distances.")
        for j in range(16):
            move(j*2*np.pi/16,(j+1)*2*np.pi/16,0.7)
            if j<15:
                dots.add(Dot(planet_at((j+1)*2*np.pi/16),radius=0.04,color=ORBIT))
        say("Closer dots near apastron mean slower motion.")
        self.wait(3)
        timing["equal_time"] = self.time-0.3
        self.play(FadeOut(dots), FadeOut(peri), FadeOut(apa), run_time=0.7)
        say("Pause one instant: only 9.09% of the period has elapsed.")
        move(0,chosen_m,2.5)
        m_value = MathTex(r"M=32.7^\circ",font_size=29,color=CLOCK).move_to([-4.55,-2.55,0])
        self.play(FadeIn(m_value),run_time=0.6)
        self.wait(2)

        chapter("02 / THE CONSTRUCTION", ECC)
        say("E points from the ellipse center to Q on an auxiliary circle.")
        q = center+a*np.array([np.cos(chosen_e),np.sin(chosen_e),0])
        auxiliary = DashedVMobject(Circle(radius=a,color=MUTED,stroke_width=1.3).move_to(center),
                                   num_dashes=64)
        q_dot = Dot(q,radius=0.055,color=ECC)
        c_dot = Dot(center,radius=0.045,color=MUTED)
        reference = Line(center,center+[a,0,0],color=MUTED,stroke_width=1)
        e_ray = Line(center,q,color=ECC,stroke_width=2)
        vertical = DashedVMobject(Line(q,planet.get_center(),color=ECC,stroke_width=2),num_dashes=7)
        e_arc = Arc(radius=0.43,start_angle=0,angle=chosen_e,arc_center=center,color=ECC,stroke_width=2)
        e_label = MathTex("E",font_size=28,color=ECC).move_to(center+[0.55,0.34,0])
        labels = VGroup(
            text("C",20,MUTED).move_to(center+[0,-.23,0]),
            text("S",20,STAR).move_to(focus+[0,-.23,0]),
            text("Q",20,ECC).move_to(q+[.20,.12,0]),
        )
        self.play(Create(auxiliary),FadeIn(c_dot),FadeIn(labels),run_time=1.8)
        self.play(Create(reference),Create(e_ray),Create(e_arc),FadeIn(e_label),FadeIn(q_dot),run_time=1.8)
        self.play(Create(vertical),run_time=1.2)
        say("Q maps vertically to the planet. Q is not another body.")
        e_value = MathTex(r"E=60.0^\circ",font_size=29,color=ECC).move_to([1.45,-2.55,0])
        self.play(FadeIn(e_value),run_time=.5)
        self.wait(4)

        chapter("03 / THE REAL DIRECTION", TRUE)
        say("True anomaly is measured at the star, toward the actual planet.")
        n_ray = Line(focus,planet.get_center(),color=TRUE,stroke_width=3)
        n_ref = Line(focus,focus+[.75,0,0],color=MUTED,stroke_width=1)
        n_arc = Arc(radius=.50,start_angle=0,angle=true,arc_center=focus,color=TRUE,stroke_width=2)
        n_label = MathTex(r"\nu",font_size=30,color=TRUE).move_to(focus+[.47,.50,0])
        n_value = MathTex(r"\nu=94.0^\circ",font_size=29,color=TRUE).move_to([4.20,-2.55,0])
        self.play(Create(n_ray),Create(n_ref),Create(n_arc),FadeIn(n_label),FadeIn(n_value),run_time=1.8)
        say("M = 32.7°. E = 60.0°. ν = 94.0°. The same instant.")
        self.wait(4)
        timing["angles"] = self.time-0.3
        kepler = MathTex(r"M=E-e\sin E",font_size=27,color=INK).move_to([-1.45,-.70,0])
        self.play(Write(kepler),run_time=1.2)
        say("Time gives M. Solve Kepler for E. Coordinates give ν.")
        self.wait(4)

        chapter("04 / THE CIRCULAR LIMIT", ORBIT)
        say("Keep time fixed. Reduce eccentricity to zero.")
        self.play(FadeOut(VGroup(auxiliary,q_dot,c_dot,reference,e_ray,vertical,e_arc,e_label,
                                labels,n_ray,n_ref,n_arc,n_label,e_value,n_value,kepler)),
                  run_time=1)
        def circular_orbit(mob,alpha):
            current_e=e*(1-alpha)
            mob.become(Ellipse(width=2*a,height=2*a*np.sqrt(1-current_e**2),
                               color=ORBIT,stroke_width=3).move_to(center))
        def circular_star(mob,alpha):
            mob.move_to(center+[a*e*(1-alpha),0,0])
        def circular_planet(mob,alpha):
            current_e=e*(1-alpha)
            current_E=eccentric_anomaly(chosen_m,current_e)
            mob.move_to(center+a*np.array([np.cos(current_E),
                         np.sqrt(1-current_e**2)*np.sin(current_E),0]))
        self.play(UpdateFromAlphaFunc(orbit,circular_orbit),UpdateFromAlphaFunc(star,circular_star),
                  UpdateFromAlphaFunc(planet,circular_planet),run_time=2.8,rate_func=linear)
        new_planet=planet.get_center()
        circle_ray = Line(center,new_planet,color=TRUE,stroke_width=2)
        same_arcs = VGroup(*[
            Arc(radius=r,start_angle=0,angle=chosen_m,arc_center=center,color=color,stroke_width=2)
            for r,color in zip([.40,.60,.80],[CLOCK,ECC,TRUE])
        ])
        equal = MathTex(r"M=E=\nu=32.7^\circ",font_size=34,color=INK).move_to([2.3,-2.75,0])
        self.play(Create(circle_ray),Create(same_arcs),Write(equal),
                  Transform(orbit_title,text("CIRCULAR MOTION · CONSTANT SPEED",19,MUTED)
                            .move_to([2.4,2.18,0])),run_time=1.5)
        say("For a circle, the center and focus coincide. All three angles agree.")
        self.wait(4)
        finish = MathTex(r"t\longrightarrow M\longrightarrow E\longrightarrow(r,\nu)",
                        font_size=36,color=INK).move_to([0,2.92,0])
        self.play(Transform(caption,finish),run_time=.8)
        self.wait(3)
        TIMING.write_text(json.dumps(timing,indent=2)+"\n")


class Project3Orientation(ThreeDScene):
    def construct(self):
        self.camera.background_color = NIGHT
        a,e,i,w = 2.0,ECCENTRICITY,np.deg2rad(65),np.pi/2
        self.set_camera_orientation(phi=np.deg2rad(62),theta=np.deg2rad(-60),zoom=.90)
        title = text("Orientation and position are different.",32).move_to([0,3.60,0])
        caption = text("The sky plane is our reference plane.",26).move_to([0,2.95,0])
        self.add_fixed_in_frame_mobjects(title,caption)

        def say(value):
            nonlocal caption
            self.play(FadeOut(caption),run_time=.2)
            self.remove_fixed_in_frame_mobjects(caption)
            caption=text(value,26).move_to([0,2.95,0])
            self.add_fixed_in_frame_mobjects(caption)
            self.play(FadeIn(caption),run_time=.2)

        def xyz(mean):
            x,y=a*position(mean)
            transverse=x*np.sin(w)+y*np.cos(w)
            return np.array([x*np.cos(w)-y*np.sin(w),transverse*np.cos(i),transverse*np.sin(i)])

        def direction(radius,angle):
            return np.array([radius*np.cos(angle),radius*np.sin(angle)*np.cos(i),
                             radius*np.sin(angle)*np.sin(i)])

        sky = Square(side_length=5.0,color=MUTED,stroke_width=1).set_fill(MUTED,opacity=.06)
        grid = VGroup(*[Line([x,-2.5,0],[x,2.5,0],color=MUTED,stroke_width=.6).set_opacity(.20)
                        for x in np.arange(-2,2.1,.5)],
                      *[Line([-2.5,y,0],[2.5,y,0],color=MUTED,stroke_width=.6).set_opacity(.20)
                        for y in np.arange(-2,2.1,.5)])
        x_axis = Arrow3D([0,0,0],[2.8,0,0],color=MUTED,thickness=.012)
        z_axis = Arrow3D([0,0,0],[0,0,2.7],color=MUTED,thickness=.012)
        star = glowing_dot(np.zeros(3),STAR,.09)
        self.play(Create(sky),FadeIn(grid),FadeIn(star),Create(x_axis),Create(z_axis),run_time=2)
        x_label=text("X · node direction",19,MUTED).move_to([3.95,-.55,0])
        z_label=text("+Z · toward observer",19,MUTED).move_to([0,0,2.95])
        sky_label=text("SKY PLANE",18,MUTED).move_to([-1.8,-2.7,0])
        self.add_fixed_in_frame_mobjects(x_label)
        self.add_fixed_orientation_mobjects(z_label,sky_label)
        self.play(FadeIn(VGroup(x_label,z_label,sky_label)),run_time=.6)
        self.wait(2)
        orbit = ParametricFunction(xyz,t_range=[0,2*np.pi],color=ORBIT,stroke_width=3)
        say("Inclination i tilts the orbital plane relative to the sky.")
        hinge = np.array([1.7,0,0])
        tilt = ParametricFunction(lambda t: hinge+[0,.75*np.cos(t),.75*np.sin(t)],
                                 t_range=[0,i],color=ECC,stroke_width=3)
        i_label = MathTex("i",color=ECC,font_size=30).move_to(hinge+[0,.80*np.cos(i/2),.80*np.sin(i/2)])
        self.add_fixed_orientation_mobjects(i_label)
        self.play(Create(orbit),Create(tilt),FadeIn(i_label),run_time=2)
        self.move_camera(phi=np.deg2rad(68),theta=np.deg2rad(-80),run_time=3)
        self.wait(2)
        say("ω is measured from the ascending-node direction to periastron.")
        peri = direction(a*(1-e),w)
        peri_ray = Line([0,0,0],peri,color=ECC,stroke_width=2)
        peri_dot=Dot(peri,radius=.045,color=ECC)
        peri_label=text("Periastron",19,ECC).move_to(peri+[.1,.1,.18])
        self.add_fixed_orientation_mobjects(peri_label)
        omega_arc = ParametricFunction(lambda t: direction(.58,t),t_range=[0,w],color=CLOCK,stroke_width=3)
        omega_label = MathTex(r"\omega",font_size=30,color=CLOCK).move_to(direction(.78,w/2))
        self.add_fixed_orientation_mobjects(omega_label)
        self.play(Create(peri_ray),Create(omega_arc),FadeIn(omega_label),FadeIn(peri_dot),FadeIn(peri_label),run_time=2)
        self.wait(3)
        say("ν is measured from periastron to the planet, at the star.")
        mean=(np.pi/3)-e*np.sin(np.pi/3)
        planet=glowing_dot(xyz(mean),INK,.065)
        ray=Line([0,0,0],xyz(mean),color=TRUE,stroke_width=2)
        nu=np.arctan2(*position(mean)[[1,0]])
        nu_arc=ParametricFunction(lambda t:direction(.91,t),t_range=[w,w+nu],color=TRUE,stroke_width=3)
        nu_label=MathTex(r"\nu",font_size=30,color=TRUE).move_to(direction(1.15,w+nu/2))
        self.add_fixed_orientation_mobjects(nu_label)
        self.play(FadeIn(planet),Create(ray),Create(nu_arc),FadeIn(nu_label),run_time=2)
        legend=VGroup(text("i = 65° · tilt",23,ECC),text("ω = 90° · orientation",23,CLOCK),
                      text("ν changes · position",23,TRUE)).arrange(np.array([0,-1,0]),aligned_edge=np.array([-1,0,0]),buff=.40).move_to([-4.85,.20,0])
        self.add_fixed_in_frame_mobjects(legend)
        self.play(FadeIn(legend),run_time=.6)
        self.wait(3)
        say("In the two-body model, i and ω stay fixed while the planet moves.")
        self.play(FadeOut(nu_arc),FadeOut(nu_label),run_time=.5)
        def update_planet(mob,alpha):
            mob.move_to(xyz(mean+alpha*2*np.pi))
        def update_ray(mob,alpha):
            mob.put_start_and_end_on(np.zeros(3),xyz(mean+alpha*2*np.pi))
        self.play(UpdateFromAlphaFunc(planet,update_planet),UpdateFromAlphaFunc(ray,update_ray),
                  run_time=10,rate_func=linear)
        say("Find position in the orbital plane. Then project onto the sky.")
        self.wait(3)
