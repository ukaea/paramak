
"""Example reactor based on the SPARC design as published in Figure 4 of
Overview of the SPARC tokamak. Journal of Plasma Physics, 86(5), 865860502.
doi:10.1017/S0022377820001257. Coordinates extracted from the figure are
not exact and therefore this model does not perfectly represent the reactor."""

import paramak


def main(rotation_angle=180):

    inboard_pf_coils = paramak.PoloidalFieldCoilSet(
        center_points=[
            (53.5, -169.58),
            (53.5, -118.43),
            (53.5, -46.54),
            (53.5, 46.54),
            (53.5, 118.43),
            (53.5, 169.58),
        ],
        heights=[41.5, 40.5, 82.95, 82.95, 40.5, 41.5, ],
        widths=[27.7, 27.7, 27.7, 27.7, 27.7, 27.7],
        rotation_angle=rotation_angle,
        stp_filename='inboard_pf_coils.stp'
    )

    outboard_pf_coils = paramak.PoloidalFieldCoilSet(
        center_points=[
            (86, 230),
            (86, -230),
            (164, 241),
            (164, -241),
            (263, 222),
            (263, -222),
            (373, 131),
            (373, -131),
        ],
        widths=[32, 32, 50, 50, 43, 43, 48, 48, ],
        heights=[40, 40, 30, 30, 28, 28, 37, 37, ],
        rotation_angle=rotation_angle,
        stp_filename='outboard_pf_coils.stp'
    )

    div_coils = paramak.PoloidalFieldCoilSet(
        center_points=[
            (207, 144),
            (207, 125),
            (207, -144),
            (207, -125),

        ],
        widths=[15, 15, 15, 15],
        heights=[15, 15, 15, 15],
        rotation_angle=rotation_angle,
        stp_filename='div_coils.stp'
    )

    vs_coils = paramak.PoloidalFieldCoilSet(
        center_points=[
            (240, 70),
            (240, -70),
        ],
        widths=[10, 10],
        heights=[10, 10],
        rotation_angle=rotation_angle,
        stp_filename='vs_coils.stp'
    )

    EFCCu_coils_1 = paramak.RotateStraightShape(
        points=[
            (235.56581986143186, -127.64976958525347),
            (240.1847575057737, -121.19815668202767),
            (246.65127020785218, -125.80645161290323),
            (242.0323325635104, -132.25806451612902),
        ],
        rotation_angle=rotation_angle,
        stp_filename='EFCCu_coils_1.stp'
    )
    EFCCu_coils_2 = paramak.RotateStraightShape(
        points=[
            (262.3556581986143, -90.78341013824888),
            (266.97459584295615, -84.33179723502303),
            (273.44110854503464, -88.94009216589859),
            (268.82217090069287, -94.47004608294935),
        ],
        rotation_angle=rotation_angle,
        stp_filename='EFCCu_coils_2.stp'
    )
    EFCCu_coils_3 = paramak.RotateStraightShape(
        points=[
            (281.7551963048499, -71.42857142857144),
            (289.1454965357968, -71.42857142857144),
            (289.1454965357968, -78.80184331797238),
            (281.7551963048499, -78.80184331797238),
        ],
        rotation_angle=rotation_angle,
        stp_filename='EFCCu_coils_3.stp'
    )

    EFCCu_coils_4 = paramak.RotateStraightShape(
        points=[
            (235.56581986143186, 127.64976958525347),
            (240.1847575057737, 121.19815668202767),
            (246.65127020785218, 125.80645161290323),
            (242.0323325635104, 132.25806451612902),
        ],
        rotation_angle=rotation_angle,
        stp_filename='EFCCu_coils_4.stp'
    )
    EFCCu_coils_5 = paramak.RotateStraightShape(
        points=[
            (262.3556581986143, 90.78341013824888),
            (266.97459584295615, 84.33179723502303),
            (273.44110854503464, 88.94009216589859),
            (268.82217090069287, 94.47004608294935),
        ],
        rotation_angle=rotation_angle,
        stp_filename='EFCCu_coils_5.stp'
    )
    EFCCu_coils_6 = paramak.RotateStraightShape(
        points=[
            (281.7551963048499, 71.42857142857144),
            (289.1454965357968, 71.42857142857144),
            (289.1454965357968, 78.80184331797238),
            (281.7551963048499, 78.80184331797238),
        ],
        rotation_angle=rotation_angle,
        stp_filename='EFCCu_coils_6.stp'
    )

    plasma = paramak.Plasma(
        major_radius=185,
        minor_radius=57 - 6,  # 3 is a small ofset to avoid overlaps
        triangularity=0.31,
        elongation=1.97,
        rotation_angle=rotation_angle,
        stp_filename='plasma.stp',
    )

    antenna = paramak.RotateMixedShape(
        points=[
            (263.2794457274827, 46.5437788018433, 'straight'),
            (263.2794457274827, -46.54377880184336, 'straight'),
            (231.87066974595842, -46.54377880184336, 'spline'),
            (243.87990762124713, 0, 'spline'),
            (231.87066974595842, 46.5437788018433, 'straight'),
        ],
        rotation_angle=rotation_angle,
        stp_filename='antenna.stp'
    )

    tf_coil = paramak.ToroidalFieldCoilPrincetonD(
        R1=105,
        R2=339,
        thickness=33,
        distance=33,
        number_of_coils=12,
        rotation_angle=rotation_angle,
        stp_filename='tf_coil.stp'
    )

    vac_vessel = paramak.RotateStraightShape(
        points=[
            (117.32101616628177, 126.72811059907835),
            (163.51039260969978, 170.04608294930875),
            (181.98614318706697, 171.88940092165896),
            (196.76674364896073, 169.12442396313364),
            (196.76674364896073, 115.66820276497694),
            (236.4896073903002, 114.74654377880185),
            (273.44110854503464, 65.89861751152074),
            (272.51732101616625, -65.89861751152074),
            (236.4896073903002, -115.66820276497697),
            (196.76674364896073, -115.66820276497697),
            (196.76674364896073, -169.12442396313367),
            (181.98614318706697, -172.81105990783408),
            (163.51039260969978, -170.04608294930875),
            (117.32101616628177, -126.72811059907832),
            (117.32101616628177, 123.04147465437785),
            (123.78752886836028, 123.04147465437785),
            (123.78752886836028, -123.963133640553),
            (165.3579676674365, -162.67281105990781),
            (181.98614318706697, -164.5161290322581),
            (190.3002309468822, -162.67281105990781),
            (190.3002309468822, -112.90322580645159),
            (193.99538106235568, -109.21658986175117),
            (232.7944572748268, -109.21658986175117),
            (266.97459584295615, -63.13364055299536),
            (266.05080831408776, 62.21198156682027),
            (232.7944572748268, 109.21658986175115),
            (193.99538106235568, 109.21658986175115),
            (190.3002309468822, 111.98156682027647),
            (190.3002309468822, 162.67281105990784),
            (181.98614318706697, 164.51612903225805),
            (165.3579676674365, 162.67281105990784),
            (123.78752886836028, 123.04147465437785),
            (117.32101616628177, 123.04147465437785),
        ],
        rotation_angle=rotation_angle,
        stp_filename='vacvessel.stp'
    )

    inner_vessel = paramak.RotateStraightShape(
        points=[
            (269.7459584295612, -46.54377880184336, 'straight'),
            (231.87066974595842, -46.5437788018433, 'spline'),
            (223.55658198614316, -62.21198156682027, 'spline'),
            (207.85219399538107, -80.64516129032262, 'spline'),
            (166.28175519630486, -115.66820276497697, 'spline'),
            (164.43418013856814, -119.35483870967744, 'spline'),
            (164.43418013856814, -122.11981566820276, 'straight'),
            (173.67205542725173, -140.5529953917051, 'straight'),
            (184.75750577367205, -140.5529953917051, 'straight'),
            (184.75750577367205, -158.98617511520735, 'straight'),
            (181.98614318706697, -159.9078341013825, 'straight'),
            (147.80600461893764, -118.43317972350235, 'straight'),
            (129.33025404157044, -123.04147465437785, 'straight'),
            (145.95842956120094, -111.05990783410135, 'straight'),
            (126.55889145496536, -50.23041474654377, 'straight'),
            (127.48267898383372, 50.23041474654377, 'straight'),
            (145.95842956120094, 110.13824884792626, 'straight'),
            (128.40646651270208, 123.04147465437785, 'straight'),
            (147.80600461893764, 117.51152073732717, 'straight'),
            (181.98614318706697, 159.90783410138246, 'straight'),
            (185.6812933025404, 158.98617511520735, 'straight'),
            (184.75750577367205, 140.55299539170505, 'straight'),
            (172.74826789838338, 140.55299539170505, 'spline'),
            (164.43418013856814, 121.19815668202764, 'spline'),
            (164.43418013856814, 118.43317972350229, 'spline'),
            (165.3579676674365, 115.66820276497694, 'spline'),
            (173.67205542725173, 111.05990783410135, 'spline'),
            (207.85219399538107, 80.64516129032256, 'spline'),
            (220.7852193995381, 66.82027649769586, 'spline'),
            (231.87066974595842, 46.5437788018433, 'spline'),
            (268.82217090069287, 46.5437788018433, 'straight'),
            (268.82217090069287, 63.13364055299536, 'straight'),
            (233.71824480369514, 111.98156682027647, 'straight'),
            (193.99538106235568, 112.90322580645159, 'straight'),
            (192.14780600461893, 164.51612903225805, 'straight'),
            (163.51039260969978, 166.35944700460828, 'straight'),
            (121.93995381062356, 123.96313364055297, 'straight'),
            (121.0161662817552, -125.80645161290323, 'straight'),
            (163.51039260969978, -166.35944700460834, 'straight'),
            (192.14780600461893, -166.35944700460834, 'straight'),
            (193.99538106235568, -112.90322580645159, 'straight'),
            (234.64203233256353, -111.9815668202765, 'straight'),
            (269.7459584295612, -63.13364055299536, 'straight'),
        ],
        rotation_angle=rotation_angle,
        stp_filename='inner_vessel.stp',
        cut=[vac_vessel, vs_coils, antenna]
    )

    sparc = paramak.Reactor([inboard_pf_coils, outboard_pf_coils,
                             plasma, antenna, vs_coils, inner_vessel, tf_coil,
                             EFCCu_coils_1, EFCCu_coils_2, EFCCu_coils_3,
                             EFCCu_coils_4, EFCCu_coils_5, EFCCu_coils_6,
                             vac_vessel, div_coils])

    sparc.export_stp()
    sparc.export_svg('htc_reactor.svg')


if __name__ == "__main__":
    main()
