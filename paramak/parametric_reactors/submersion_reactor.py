
import math
import operator

import cadquery as cq

import paramak


class SubmersionTokamak(paramak.Reactor):
    """Creates geometry for a simple submersion reactor including a
    plasma, cylindical center column shielding, square toroidal field
    coils. There is an inboard breeder blanket on this ball reactor.

    :param inner_bore_radial_thickness: the radial thickness of 
     the inner bore (cm)
    :type inner_bore_radial_thickness: float
    :inboard_tf_leg_radial_thickness: the radial thickness of the
     inner leg of the toroidal field coils (cm)
    :type inboard_tf_leg_radial_thickness: float
    :center_column_shield_radial_thickness: the radial thickness
     of the center column shield (cm)
    :type center_column_shield_radial_thickness: float
    :inboard_blanket_radial_thickness: the radial thickness of the first wall (cm)
    :type inboard_blanket_radial_thickness: float
    :firstwall_radial_thickness: the radial thickness of the first wall (cm)
    :type firstwall_radial_thickness: float
    :inner_plasma_gap_radial_thickness: the radial thickness of the
     inboard gap between the plasma and the center column shield (cm)
    :type inner_plasma_gap_radial_thickness: float
    :plasma_radial_thickness: the radial thickness of the plasma (cm),
     this is double the minor radius
    :type plasma_radial_thickness: float
    :divertor_radial_thickness: the radial thickness of the divertors (cm)
    :type divertor_radial_thickness: float
    :outer_plasma_gap_radial_thickness: the radial thickness of the
     outboard gap between the plasma and the firstwall (cm)
    :type outer_plasma_gap_radial_thickness: float
    :outboard_blanket_radial_thickness: the radial thickness of the blanket (cm)
    :type outboard_blanket_radial_thickness: float
    :blanket_rear_wall_radial_thickness: the radial thickness of the rear wall
     of the blanket (cm)
    :type blanket_rear_wall_radial_thickness: float

    :rotation_angle: the angle of the sector that is desired
    :type rotation_angle: int

    :return: a Reactor object that has generic functionality
    :rtype: paramak shape object
    """

    def __init__(
        self,
        inner_bore_radial_thickness,
        inboard_tf_leg_radial_thickness,
        center_column_shield_radial_thickness,
        inboard_blanket_radial_thickness,
        firstwall_radial_thickness,
        inner_plasma_gap_radial_thickness,
        plasma_radial_thickness,
        divertor_radial_thickness,
        outer_plasma_gap_radial_thickness,
        outboard_blanket_radial_thickness,
        blanket_rear_wall_radial_thickness,
        # outboard_tf_coil_radial_thickness,
        # pf_coil_to_rear_blanket_radial_gap,
        # pf_coil_radial_thicknesses,
        # pf_coil_to_tf_coil_radial_gap,
        plasma_high_point,
        #ToDo add divertor
        # divertor_vertical_thickness,
        # ToDo add pf and tf coils
        # tf_coil_to_rear_blanket_vertical_gap,
        # tf_coil_vertical_thickness,
        # pf_coil_vertical_thicknesses,
        # number_of_tf_coils,
        rotation_angle = 360,
    ):

        super().__init__([])

        self.inner_bore_radial_thickness = inner_bore_radial_thickness
        self.inboard_tf_leg_radial_thickness = inboard_tf_leg_radial_thickness
        self.center_column_shield_radial_thickness = center_column_shield_radial_thickness
        self.inboard_blanket_radial_thickness = inboard_blanket_radial_thickness
        self.firstwall_radial_thickness = firstwall_radial_thickness
        self.inner_plasma_gap_radial_thickness = inner_plasma_gap_radial_thickness
        self.plasma_radial_thickness = plasma_radial_thickness
        self.outer_plasma_gap_radial_thickness = outer_plasma_gap_radial_thickness

        self.outboard_blanket_radial_thickness = outboard_blanket_radial_thickness
        self.blanket_rear_wall_radial_thickness = blanket_rear_wall_radial_thickness
        #ToDo add pf coils
        # self.pf_coil_to_rear_blanket_radial_gap = pf_coil_to_rear_blanket_radial_gap
        # self.pf_coil_radial_thicknesses = pf_coil_radial_thicknesses
        # self.pf_coil_to_tf_coil_radial_gap = pf_coil_to_tf_coil_radial_gap
        # self.outboard_tf_coil_radial_thickness = outboard_tf_coil_radial_thickness
        self.divertor_radial_thickness = divertor_radial_thickness
        self.plasma_high_point = plasma_high_point
        # self.divertor_vertical_thickness = divertor_vertical_thickness

        # ToDo add pf and tf coils
        # self.tf_coil_to_rear_blanket_vertical_gap = tf_coil_to_rear_blanket_vertical_gap
        # self.tf_coil_vertical_thickness = tf_coil_vertical_thickness
        # self.pf_coil_vertical_thicknesses = pf_coil_vertical_thicknesses
        # self.number_of_tf_coils = number_of_tf_coils
        self.rotation_angle = rotation_angle

        # these are set later by the plasma when it is created
        self.major_radius = None
        self.minor_radius = None
        self.elongation = None
        self.triangularity = None

        self.create_components()

    def create_components(self):

        # this is the radial build sequence, where one componet stops and another starts
        inner_bore_start_radius = 0
        inner_bore_end_radius = inner_bore_start_radius + self.inner_bore_radial_thickness
        print('inner_bore_end_radius',inner_bore_end_radius)

        inboard_tf_coils_start_radius = inner_bore_end_radius
        inboard_tf_coils_end_radius = inboard_tf_coils_start_radius + self.inboard_tf_leg_radial_thickness
        print('inboard_tf_coils_end_radius',inboard_tf_coils_end_radius)

        center_column_shield_start_radius = inboard_tf_coils_end_radius
        center_column_shield_end_radius = center_column_shield_start_radius + self.center_column_shield_radial_thickness
        print('center_column_shield_end_radius',center_column_shield_end_radius)

        inboard_blanket_start_radius = center_column_shield_end_radius
        inboard_blanket_end_radius = inboard_blanket_start_radius + self.inboard_blanket_radial_thickness
        print('inboard_blanket_end_radius',inboard_blanket_end_radius)

        inboard_firstwall_start_radius = inboard_blanket_end_radius
        inboard_firstwall_end_radius = inboard_firstwall_start_radius + self.firstwall_radial_thickness
        print('inboard_firstwall_end_radius',inboard_firstwall_end_radius)

        inner_plasma_gap_start_radius = inboard_firstwall_end_radius
        inner_plasma_gap_end_radius = inner_plasma_gap_start_radius + self.inner_plasma_gap_radial_thickness
        print('inner_plasma_gap_end_radius',inner_plasma_gap_end_radius)

        plasma_start_radius = inner_plasma_gap_end_radius
        plasma_end_radius = plasma_start_radius + self.plasma_radial_thickness
        print('plasma_start_radius',plasma_start_radius)
        print('plasma_end_radius',plasma_end_radius)

        outer_plasma_gap_start_radius = plasma_end_radius
        outer_plasma_gap_end_radius = outer_plasma_gap_start_radius + self.outer_plasma_gap_radial_thickness
        print('outer_plasma_gap_end_radius',outer_plasma_gap_end_radius)

        outboard_firstwall_start_radius = outer_plasma_gap_end_radius
        outboard_firstwall_end_radius = outboard_firstwall_start_radius + self.firstwall_radial_thickness
        print('outboard_firstwall_end_radius',outboard_firstwall_end_radius)

        outboard_blanket_start_radius = outboard_firstwall_end_radius
        outboard_blanket_end_radius = outboard_blanket_start_radius + self.outboard_blanket_radial_thickness
        print('outboard_blanket_end_radius',outboard_blanket_end_radius)

        blanket_rear_wall_start_radius = outboard_blanket_end_radius 
        blanket_rear_wall_end_radius = blanket_rear_wall_start_radius + self.blanket_rear_wall_radial_thickness 

        
        #ToDo add pf tf coils
        # blanket_rear_wall_to_pf_coil_gap_start_radius = blanket_rear_wall_end_radius
        # blanket_rear_wall_to_pf_coil_gap_end_radius = blanket_rear_wall_to_pf_coil_gap_start_radius + self.pf_coil_to_rear_blanket_radial_gap
        
        # pf_coil_start_radius = blanket_rear_wall_to_pf_coil_gap_end_radius
        # pf_coil_end_radius = pf_coil_start_radius + self.pf_coil_radial_thicknesses

        # pf_coil_to_tf_coil_gap_start_radius = pf_coil_end_radius
        # pf_coil_to_tf_coil_gap_end_radius = pf_coil_to_tf_coil_gap_start_radius + self.pf_coil_to_tf_coil_radial_gap

        # tf_coil_start_radius = pf_coil_to_tf_coil_gap_end_radius
        # tf_coil_end_radius = tf_coil_start_radius + self.outboard_tf_coil_radial_thickness

        divertor_start_radius = self.plasma_high_point[0] - 0.5 * self.divertor_radial_thickness
        divertor_end_radius = self.plasma_high_point[0] + 0.5 * self.divertor_radial_thickness


        #this is the vertical build sequence, componets build on each other in a similar manner to the radial build
        plasma_start_height = 0
        plasma_end_height = plasma_start_height + self.plasma_high_point[1]

        plasma_to_divertor_gap_start_height = plasma_end_height
        plasma_to_divertor_gap_end_height = plasma_to_divertor_gap_start_height + self.outer_plasma_gap_radial_thickness

        #the firstwall is cut by the divertor but uses the same control points
        firstwall_start_height = plasma_to_divertor_gap_end_height
        firstwall_end_height = firstwall_start_height + self.firstwall_radial_thickness

        blanket_start_height = firstwall_end_height
        blanket_end_height = blanket_start_height + self.outboard_blanket_radial_thickness

        blanket_rear_wall_start_height = blanket_end_height
        blanket_rear_wall_end_height = blanket_rear_wall_start_height + self.blanket_rear_wall_radial_thickness

        # ToDo add tf coils
        # self.tf_coil_to_rear_blanket_vertical_gap = tf_coil_to_rear_blanket_vertical_gap
        # self.tf_coil_vertical_thickness = tf_coil_vertical_thickness

        #ToDo, return error warning
        if self.plasma_high_point[0] < plasma_start_radius:
            print('The first value in plasma high_point is too small, it should be larger than',plasma_start_radius)
        if self.plasma_high_point[0] > plasma_end_radius:
            print('The first value in plasma high_point is too large, it should be smaller than',plasma_end_radius)

        shapes_or_components = []

        # shapes_or_components.append(inboard_tf_coils)
        inboard_tf_coils = paramak.CenterColumnShieldCylinder(
            height=blanket_rear_wall_end_height * 2,
            inner_radius=inboard_tf_coils_start_radius,
            outer_radius=inboard_tf_coils_end_radius,
            rotation_angle=self.rotation_angle,
            stp_filename="inboard_tf_coils.stp",
            name="inboard_tf_coils",
            material_tag="inboard_tf_coils_mat",
        )
        shapes_or_components.append(inboard_tf_coils)

        center_column_shield = paramak.CenterColumnShieldCylinder(
            height=blanket_rear_wall_end_height * 2,
            inner_radius=center_column_shield_start_radius,
            outer_radius=center_column_shield_end_radius,
            rotation_angle=self.rotation_angle,
            stp_filename="center_column_shield.stp",
            name="center_column_shield",
            material_tag="center_column_shield_mat",
        )
        shapes_or_components.append(center_column_shield)


        plasma = paramak.PlasmaFromPoints(outer_equatorial_x_point=plasma_end_radius,
                                          inner_equatorial_x_point=plasma_start_radius,
                                          high_point=self.plasma_high_point,
                                          rotation_angle=self.rotation_angle)

        self.major_radius = plasma.major_radius
        self.minor_radius = plasma.minor_radius
        self.elongation = plasma.elongation
        self.triangularity = plasma.triangularity

        shapes_or_components.append(plasma)

        inboard_firstwall = paramak.BlanketFP(
            plasma=plasma,
            offset_from_plasma=self.inner_plasma_gap_radial_thickness,
            start_angle=90,
            stop_angle=270,
            thickness=self.firstwall_radial_thickness,
            rotation_angle=self.rotation_angle,
            stp_filename='inboard_firstwall.stp',
            name='inboard_firstwall',
            material_tag='firstwall_mat',
        )
        # shapes_or_components.append(inboard_firstwall)

        inboard_blanket = paramak.CenterColumnShieldCylinder(
            height=blanket_end_height * 2,
            inner_radius=inboard_blanket_start_radius,
            outer_radius=max([item[0] for item in inboard_firstwall.points]),
            rotation_angle=self.rotation_angle,
            # color=centre_column_color,
            stp_filename='inboard_blanket.stp',
            name='inboard_blanket',
            material_tag='blanket_mat',
            cut=inboard_firstwall
        )

        # this takes a single solid from a compound of solids by finding the solid nearest to a point
        inboard_blanket.solid = inboard_blanket.solid.solids(cq.selectors.NearestToPointSelector((0, 0, 0)))

        # shapes_or_components.append(inboard_blanket)

        outboard_firstwall = paramak.BlanketFP(
            plasma=plasma,
            offset_from_plasma=self.outer_plasma_gap_radial_thickness,
            start_angle=90,
            stop_angle=-90,
            thickness=self.firstwall_radial_thickness,
            rotation_angle=self.rotation_angle,
            stp_filename='outboard_firstwall.stp',
            name='outboard_firstwall',
            material_tag='firstwall_mat',
        )
        # shapes_or_components.append(outboard_firstwall)

        divertor = paramak.CenterColumnShieldCylinder(
            height=blanket_rear_wall_end_height * 2,
            inner_radius=divertor_start_radius,
            outer_radius=divertor_end_radius,
            rotation_angle=self.rotation_angle,
            stp_filename="divertor.stp",
            name="divertor",
            material_tag="divertor_mat",
        )

        firstwall = outboard_firstwall.solid.union(inboard_firstwall.solid)

        divertor.solid =divertor.solid.intersect(firstwall)
        shapes_or_components.append(divertor)

        outboard_firstwall.solid = firstwall.cut(divertor.solid)
        shapes_or_components.append(outboard_firstwall)

        outboard_blanket = paramak.BlanketFP(
            plasma=plasma,
            start_angle=90,
            stop_angle=-90,
            offset_from_plasma=self.outer_plasma_gap_radial_thickness +
                               self.firstwall_radial_thickness,
            thickness = self.outboard_blanket_radial_thickness,
            rotation_angle=self.rotation_angle,
            stp_filename='outboard_blanket.stp',
            name='outboard_blanket',
            material_tag='blanket_mat',
        )

        # this fuses / unions the two blankets
        blanket = outboard_blanket.solid.union(inboard_blanket.solid)
        outboard_blanket.solid = blanket
        shapes_or_components.append(outboard_blanket)

        outboard_rear_blanket_wall = paramak.BlanketFP(
            plasma=plasma,
            start_angle=90,
            stop_angle=-90,
            offset_from_plasma=self.outer_plasma_gap_radial_thickness +
                               self.firstwall_radial_thickness +
                               self.outboard_blanket_radial_thickness,
            thickness = self.blanket_rear_wall_radial_thickness,
            rotation_angle=self.rotation_angle,
            stp_filename='outboard_rear_blanket_wall.stp',
            name='outboard_rear_blanket_wall',
            material_tag='rear_blanket_wall_mat',
        )         
        # shapes_or_components.append(outboard_rear_blanket_wall)

        outboard_rear_blanket_wall2 = paramak.RotateStraightShape(
            points=[(center_column_shield_end_radius, blanket_rear_wall_start_height),
                    (center_column_shield_end_radius,blanket_rear_wall_end_height),
                    (max([item[0] for item in inboard_firstwall.points]),blanket_rear_wall_end_height),
                    (max([item[0] for item in inboard_firstwall.points]),blanket_rear_wall_start_height),
            ],
            rotation_angle=self.rotation_angle,
            stp_filename='outboard_rear_blanket_wall2.stp',
            name='outboard_rear_blanket_wall2',
            material_tag='rear_blanket_wall_mat',
        )
        # shapes_or_components.append(outboard_rear_blanket_wall2)

        outboard_rear_blanket_wall3 = paramak.RotateStraightShape(
            points=[(center_column_shield_end_radius, -blanket_rear_wall_start_height),
                    (center_column_shield_end_radius,-blanket_rear_wall_end_height),
                    (max([item[0] for item in inboard_firstwall.points]),-blanket_rear_wall_end_height),
                    (max([item[0] for item in inboard_firstwall.points]),-blanket_rear_wall_start_height),
            ],
            rotation_angle=self.rotation_angle,
            stp_filename='outboard_rear_blanket_wall3.stp',
            name='outboard_rear_blanket_wall3',
            material_tag='rear_blanket_wall_mat',
        )
        # shapes_or_components.append(outboard_rear_blanket_wall3)

        rear_blanket_wall = outboard_rear_blanket_wall.solid.union(outboard_rear_blanket_wall2.solid)
        rear_blanket_wall = rear_blanket_wall.union(outboard_rear_blanket_wall3.solid)
        outboard_rear_blanket_wall.solid = rear_blanket_wall
        shapes_or_components.append(outboard_rear_blanket_wall)

        self.shapes_and_components = shapes_or_components
