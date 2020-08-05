
import math
import operator

import cadquery as cq

import paramak


class BallReactor(paramak.Reactor):
    """Creates geometry for a simple ball reactor including a plasma,
    cylindical center column shielding, square toroidal field coils.
    There is no inboard breeder blanket on this ball reactor like
    most spherical reactors.

    :param inner_bore_radial_thickness: the radial thickness of 
     the inner bore (cm)
    :type inner_bore_radial_thickness: float
    :inboard_tf_leg_radial_thickness: the radial thickness of the
     inner leg of the toroidal field coils (cm)
    :type inboard_tf_leg_radial_thickness: float
    :center_column_shield_radial_thickness: the radial thickness
     of the center column shield (cm)
    :type center_column_shield_radial_thickness: float
    :divertor_radial_thickness: the radial thickness of the divertor
     (cm), this fills the gap between the center column shield and blanket
    :type divertor_radial_thickness: float
    :inner_plasma_gap_radial_thickness: the radial thickness of the
     inboard gap between the plasma and the center column shield (cm)
    :type inner_plasma_gap_radial_thickness: float
    :plasma_radial_thickness: the radial thickness of the plasma (cm),
     this is double the minor radius
    :type plasma_radial_thickness: float
    :outer_plasma_gap_radial_thickness: the radial thickness of the
     outboard gap between the plasma and the firstwall (cm)
    :type outer_plasma_gap_radial_thickness: float
    :firstwall_radial_thickness: the radial thickness of the first wall (cm)
    :type firstwall_radial_thickness: float
    :blanket_radial_thickness: the radial thickness of the blanket (cm)
    :type blanket_radial_thickness: float
    :blanket_rear_wall_radial_thickness: the radial thickness of the rear wall
     of the blanket (cm)
    :type blanket_rear_wall_radial_thickness: float
    :elongation: the elongation of the plasma
    :type elongation: float
    :triangularity: the triangularity of the plasma
    :type triangularity: float
    :number_of_tf_coils: the number of tf coils
    :type number_of_tf_coils: int
    :pf_coil_to_rear_blanket_radial_gap: the radial distance between the rear
     blanket and the closest poloidal field coil (optional)
    :type pf_coil_to_rear_blanket_radial_gap: float
    :pf_coil_radial_thicknesses: the radial thickness of each poloidal field
     coil (optional)
    :type pf_coil_radial_thicknesses: list of floats
    :pf_coil_vertical_thicknesses: the vertical thickness of each poloidal
     field coil (optional)
    :type pf_coil_vertical_thicknesses: list of floats
    :pf_coil_to_tf_coil_radial_gap: the radial distance between the rear of
     the poloidal field coil and the toroidal field coil (optional)
    :type pf_coil_to_tf_coil_radial_gap: float
    :outboard_tf_coil_radial_thickness: the radial thickness of the toroidal field
     coil (optional)
    :type outboard_tf_coil_radial_thickness: float
    :tf_coil_poloidal_thickness: the poloidal thickness of the toroidal field
     coil (optional)
    :type tf_coil_poloidal_thickness: float
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
        divertor_radial_thickness,
        inner_plasma_gap_radial_thickness,
        plasma_radial_thickness,
        outer_plasma_gap_radial_thickness,
        firstwall_radial_thickness,
        blanket_radial_thickness,
        blanket_rear_wall_radial_thickness,
        elongation,
        triangularity,
        number_of_tf_coils,
        pf_coil_to_rear_blanket_radial_gap = None,
        pf_coil_radial_thicknesses = None,
        pf_coil_vertical_thicknesses = None,
        pf_coil_to_tf_coil_radial_gap = None,
        outboard_tf_coil_radial_thickness = None,
        tf_coil_poloidal_thickness = None,
        rotation_angle = 360,
    ):

        super().__init__([])

        self.inner_bore_radial_thickness = inner_bore_radial_thickness
        self.inboard_tf_leg_radial_thickness = inboard_tf_leg_radial_thickness
        self.center_column_shield_radial_thickness = center_column_shield_radial_thickness
        self.divertor_radial_thickness = divertor_radial_thickness
        self.inner_plasma_gap_radial_thickness = inner_plasma_gap_radial_thickness
        self.plasma_radial_thickness = plasma_radial_thickness
        self.outer_plasma_gap_radial_thickness = outer_plasma_gap_radial_thickness
        self.firstwall_radial_thickness = firstwall_radial_thickness
        self.blanket_radial_thickness = blanket_radial_thickness
        self.blanket_rear_wall_radial_thickness = blanket_rear_wall_radial_thickness
        self.pf_coil_to_rear_blanket_radial_gap = pf_coil_to_rear_blanket_radial_gap
        self.pf_coil_radial_thicknesses = pf_coil_radial_thicknesses
        self.pf_coil_vertical_thicknesses = pf_coil_vertical_thicknesses
        self.pf_coil_to_tf_coil_radial_gap = pf_coil_to_tf_coil_radial_gap
        self.outboard_tf_coil_radial_thickness = outboard_tf_coil_radial_thickness
        self.tf_coil_poloidal_thickness = tf_coil_poloidal_thickness

        # sets major raduis and minor radius from equatorial_points to allow a radial build
        # this helps avoid the plasma overlapping the center column and such things
        inner_equatorial_point = inner_bore_radial_thickness + inboard_tf_leg_radial_thickness + center_column_shield_radial_thickness + inner_plasma_gap_radial_thickness
        outer_equatorial_point = inner_equatorial_point + plasma_radial_thickness
        self.major_radius = (inner_equatorial_point + plasma_radial_thickness + inner_equatorial_point) /2
        self.minor_radius = ((outer_equatorial_point + inner_equatorial_point) /2 )-inner_equatorial_point

        self.elongation = elongation
        self.triangularity = triangularity

        self.number_of_tf_coils = number_of_tf_coils
        self.rotation_angle = rotation_angle

        self.create_components()


    def create_components(self):

        shapes_or_components = []

        plasma = paramak.Plasma(major_radius=self.major_radius,
                                minor_radius=self.minor_radius,
                                elongation=self.elongation,
                                triangularity=self.triangularity,
                                rotation_angle=self.rotation_angle)
        plasma.create_solid()

        shapes_or_components.append(plasma)


        # this is the radial build sequence, where one componet stops and another starts
        inner_bore_start_radius = 0
        inner_bore_end_radius = inner_bore_start_radius + self.inner_bore_radial_thickness

        inboard_tf_coils_start_radius = inner_bore_end_radius
        inboard_tf_coils_end_radius = inboard_tf_coils_start_radius + self.inboard_tf_leg_radial_thickness

        center_column_shield_start_radius = inboard_tf_coils_end_radius
        center_column_shield_end_radius = center_column_shield_start_radius + self.center_column_shield_radial_thickness

        divertor_start_radius = center_column_shield_end_radius
        divertor_end_radius = center_column_shield_end_radius + self.divertor_radial_thickness

        firstwall_start_radius = center_column_shield_end_radius \
                                 + self.inner_plasma_gap_radial_thickness \
                                 + self.plasma_radial_thickness \
                                 + self.outer_plasma_gap_radial_thickness 
        firstwall_end_radius = firstwall_start_radius + self.firstwall_radial_thickness

        blanket_start_radius = firstwall_end_radius
        blanket_end_radius = blanket_start_radius + self.blanket_radial_thickness

        blanket_read_wall_start_radius = blanket_end_radius 
        blanket_read_wall_end_radius = blanket_read_wall_start_radius + self.blanket_rear_wall_radial_thickness 

        #this is the vertical build sequence, componets build on each other in a similar manner to the radial build

        firstwall_start_height = plasma.high_point[1]+ self.outer_plasma_gap_radial_thickness
        firstwall_end_height = firstwall_start_height + self.firstwall_radial_thickness

        blanket_start_height = firstwall_end_height
        blanket_end_height = blanket_start_height + self.blanket_radial_thickness

        blanket_rear_wall_start_height = blanket_end_height
        blanket_rear_wall_end_height = blanket_rear_wall_start_height + self.blanket_rear_wall_radial_thickness

        tf_coil_height = blanket_rear_wall_end_height
        center_column_shield_height = blanket_rear_wall_end_height * 2

        if self.pf_coil_vertical_thicknesses!=None and self.pf_coil_radial_thicknesses !=None and self.pf_coil_to_rear_blanket_radial_gap !=None:
            number_of_pf_coils = len(self.pf_coil_vertical_thicknesses)

            y_position_step = (2*(blanket_rear_wall_end_height + self.pf_coil_to_rear_blanket_radial_gap))/(number_of_pf_coils+1)

            pf_coils_y_values = []
            pf_coils_x_values = []
            # adds in coils with equal spacing strategy, should be updated to allow user positions
            for i in range(number_of_pf_coils):
                y_value =blanket_rear_wall_end_height + self.pf_coil_to_rear_blanket_radial_gap - y_position_step*(i+1)
                x_value = blanket_read_wall_end_radius + self.pf_coil_to_rear_blanket_radial_gap + \
                          0.5*self.pf_coil_radial_thicknesses[i]
                pf_coils_y_values.append(y_value)
                pf_coils_x_values.append(x_value)

            pf_coil_start_radius = blanket_read_wall_end_radius + self.pf_coil_to_rear_blanket_radial_gap
            pf_coil_end_radius = pf_coil_start_radius + max(self.pf_coil_radial_thicknesses)
        
            if self.pf_coil_to_tf_coil_radial_gap !=None and self.outboard_tf_coil_radial_thickness !=None:
                tf_coil_start_radius = pf_coil_end_radius + self.pf_coil_to_rear_blanket_radial_gap 
                tf_coil_end_radius = tf_coil_start_radius + self.outboard_tf_coil_radial_thickness

        # makes a large cylinder that is used to cut the TF coils when the rotation angle is less than 360
        if self.rotation_angle < 360:
            max_high = 3 * center_column_shield_height
            max_width = 3 * blanket_read_wall_end_radius
            cutting_slice = paramak.RotateStraightShape(points=[
                    (0,max_high),
                    (max_width, max_high),
                    (max_width, -max_high),
                    (0, -max_high),
                ],
                rotation_angle=360-self.rotation_angle,
                azimuth_placement_angle=360-self.rotation_angle
            )
        else:
            cutting_slice=None

        inboard_tf_coils = paramak.CenterColumnShieldCylinder(
            height=tf_coil_height * 2,
            inner_radius=inboard_tf_coils_start_radius,
            outer_radius=inboard_tf_coils_end_radius,
            rotation_angle=self.rotation_angle,
            # color=centre_column_color,
            stp_filename="inboard_tf_coils.stp",
            name="inboard_tf_coils",
            material_tag="inboard_tf_coils_mat",
        )
        shapes_or_components.append(inboard_tf_coils)

        center_column_shield = paramak.CenterColumnShieldCylinder(
            height=center_column_shield_height,
            inner_radius=center_column_shield_start_radius,
            outer_radius=center_column_shield_end_radius,
            rotation_angle=self.rotation_angle,
            # color=centre_column_color,
            stp_filename="center_column_shield.stp",
            name="center_column_shield",
            material_tag="center_column_shield_mat",
        )
        shapes_or_components.append(center_column_shield)

        extra_blanket_upper = paramak.RotateStraightShape(points=[
            (center_column_shield_end_radius, blanket_start_height),
            (center_column_shield_end_radius, blanket_end_height),
            (plasma.high_point[0], blanket_end_height),
            (plasma.high_point[0], blanket_start_height),
            ],
            rotation_angle=self.rotation_angle,)

        extra_firstwall_upper = paramak.RotateStraightShape(points=[
            (center_column_shield_end_radius, firstwall_start_height),
            (center_column_shield_end_radius, firstwall_end_height),
            (plasma.high_point[0], firstwall_end_height),
            (plasma.high_point[0], firstwall_start_height),
            ],
            rotation_angle=self.rotation_angle,)

        extra_blanket_rear_wall_upper = paramak.RotateStraightShape(points=[
            (center_column_shield_end_radius, blanket_rear_wall_start_height),
            (center_column_shield_end_radius, blanket_rear_wall_end_height),
            (plasma.high_point[0], blanket_rear_wall_end_height),
            (plasma.high_point[0], blanket_rear_wall_start_height),
            ],
            rotation_angle=self.rotation_angle,)

        extra_blanket_lower = paramak.RotateStraightShape(points=[
            (center_column_shield_end_radius, -blanket_start_height),
            (center_column_shield_end_radius, -blanket_end_height),
            (plasma.high_point[0], -blanket_end_height),
            (plasma.high_point[0], -blanket_start_height),
            ],
            rotation_angle=self.rotation_angle,)

        extra_firstwall_lower = paramak.RotateStraightShape(points=[
            (center_column_shield_end_radius, -firstwall_start_height),
            (center_column_shield_end_radius, -firstwall_end_height),
            (plasma.high_point[0], -firstwall_end_height),
            (plasma.high_point[0], -firstwall_start_height),
            ],
            rotation_angle=self.rotation_angle,)

        extra_blanket_rear_wall_lower = paramak.RotateStraightShape(points=[
            (center_column_shield_end_radius, -blanket_rear_wall_start_height),
            (center_column_shield_end_radius, -blanket_rear_wall_end_height),
            (plasma.high_point[0], -blanket_rear_wall_end_height),
            (plasma.high_point[0], -blanket_rear_wall_start_height),
            ],
            rotation_angle=self.rotation_angle,)

        firstwall = paramak.BlanketConstantThicknessArcV(
            inner_mid_point=(firstwall_start_radius, 0),
            inner_upper_point=(plasma.high_point[0], firstwall_start_height),
            inner_lower_point=(plasma.low_point[0], -firstwall_start_height),
            thickness=self.firstwall_radial_thickness,
            rotation_angle=self.rotation_angle,
            stp_filename='firstwall.stp',
            name='firstwall',
            material_tag='firstwall_mat',
            union=[extra_firstwall_upper, extra_firstwall_lower]
        )

        blanket = paramak.BlanketConstantThicknessArcV(
            inner_mid_point=(blanket_start_radius, 0),
            inner_upper_point=(plasma.high_point[0], blanket_start_height),
            inner_lower_point=(plasma.low_point[0], -blanket_start_height),
            thickness=self.blanket_radial_thickness,
            rotation_angle=self.rotation_angle,
            stp_filename='blanket.stp',
            name='blanket',
            material_tag='blanket_mat',
            union=[extra_blanket_upper, extra_blanket_lower]
        )

        blanket_rear_casing = paramak.BlanketConstantThicknessArcV(
            inner_mid_point=(blanket_read_wall_start_radius, 0),
            inner_upper_point=(plasma.high_point[0], blanket_rear_wall_start_height),
            inner_lower_point=(plasma.low_point[0], -blanket_rear_wall_start_height),
            thickness=self.blanket_rear_wall_radial_thickness,
            rotation_angle=self.rotation_angle,
            stp_filename='blanket_rear_wall.stp',
            name='blanket_rear_wall',
            material_tag='blanket_rear_wall_mat',
            union=[extra_blanket_rear_wall_upper, extra_blanket_rear_wall_lower]
        )

        # used as an intersect when making the divertor
        blanket_fw_rear_wall_envelope = paramak.BlanketConstantThicknessArcV(
            inner_mid_point=(firstwall_start_radius, 0),
            inner_upper_point=(plasma.high_point[0], firstwall_start_height),
            inner_lower_point=(plasma.low_point[0], -firstwall_start_height),
            thickness=self.firstwall_radial_thickness + self.blanket_radial_thickness + self.blanket_rear_wall_radial_thickness,
            rotation_angle=self.rotation_angle,
            union=[extra_blanket_upper, extra_firstwall_upper, extra_blanket_rear_wall_upper,
                   extra_blanket_lower, extra_firstwall_lower, extra_blanket_rear_wall_lower],
            stp_filename='test.stp'
        )

        divertor = paramak.CenterColumnShieldCylinder(
            height=blanket_rear_wall_end_height*2,
            inner_radius=divertor_start_radius,
            outer_radius=divertor_end_radius,
            intersect=blanket_fw_rear_wall_envelope,
            stp_filename='divertor.stp',
            name='divertor',
            material_tag='divertor_mat',
        )
        shapes_or_components.append(divertor)

        firstwall.solid = firstwall.solid.cut(divertor.solid)
        blanket.solid = blanket.solid.cut(divertor.solid)
        blanket_rear_casing.solid = blanket_rear_casing.solid.cut(divertor.solid)
        shapes_or_components.append(firstwall)
        shapes_or_components.append(blanket)
        shapes_or_components.append(blanket_rear_casing)

        if self.pf_coil_vertical_thicknesses!=None and self.pf_coil_radial_thicknesses !=None and self.pf_coil_to_rear_blanket_radial_gap !=None:
            
            for i, (rt, vt, y_value, x_value) in enumerate(zip(self.pf_coil_radial_thicknesses,
                                                             self.pf_coil_vertical_thicknesses,
                                                             pf_coils_y_values,
                                                             pf_coils_x_values,
                                                            )
                                                        ):


                pf_coil = paramak.PoloidalFieldCoil(width=rt, 
                                                    height=vt,
                                                    center_point=(x_value,y_value),
                                                    rotation_angle=self.rotation_angle,
                                                    stp_filename='pf_coil_'+str(i)+'.stp',
                                                    name='pf_coil',
                                                    material_tag='pf_coil_mat')
                shapes_or_components.append(pf_coil)
        
            if self.pf_coil_to_tf_coil_radial_gap !=None and self.outboard_tf_coil_radial_thickness !=None:
                tf_coil = paramak.ToroidalFieldCoilRectangle(inner_upper_point=(inboard_tf_coils_start_radius, tf_coil_height),
                                                inner_lower_point=(inboard_tf_coils_start_radius, -tf_coil_height),
                                                inner_mid_point=(tf_coil_start_radius, 0),
                                                thickness= self.outboard_tf_coil_radial_thickness,
                                                number_of_coils=self.number_of_tf_coils,
                                                distance=self.tf_coil_poloidal_thickness,
                                                stp_filename='tf_coil.stp',
                                                name='tf_coil',
                                                material_tag='tf_coil_mat',
                                                cut=cutting_slice)

                shapes_or_components.append(tf_coil)
        
        self.shapes_and_components = shapes_or_components