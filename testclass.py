from CoolProp.CoolProp import PropsSI


class HeatPump(object):
    """Simulation Hybridwaermepumpe."""

    def __init__(self, niederdruck, hochdruck, drehzahl,
                 konzentration_arm, durchfluss_pumpe, temp_arm):
        """initialisierung."""
        self.p_nd = niederdruck
        self.p_hd = hochdruck
        self.n = drehzahl
        self.x_arm = konzentration_arm
        self.m_liq = durchfluss_pumpe
        self.t_liq = temp_arm

    def verdichter_massenstrom(self):
        """Berechnet mvap."""
        to = PropsSI('T', 'Q', 0, 'P', self.p_nd, 'REFPROP::Ammonia')-273.15
        tc = PropsSI('T', 'Q', 1, 'P', self.p_hd, 'REFPROP::Ammonia')-273.15

        coef = [250.8882232197, 9.0261166145, 0.8291749454, 0.1352143006,
                0.0296764505, -0.0218782337, 0.0008803891, -0.0002082006,
                -0.0004852754, 1.87E-05]

        m_vap = coef[0] + coef[1]*to + coef[2]*tc + coef[3]*to**2 + coef[4] * \
                to * tc + coef[5]*tc**2+coef[6]*to**3+coef[7]*tc*to**2 + \
                coef[8]*to*tc**2+coef[9]*tc**3

        m_vap = m_vap/3600
        m_vap = (m_vap/2900)*self.n

        return m_vap

    def verdichter_leistung(self):
        """Berechnet die Leistung des Verdichters."""
        to = PropsSI('T', 'Q', 0, 'P', self.p_nd, 'REFPROP::Ammonia')-273.15
        tc = PropsSI('T', 'Q', 1, 'P', self.p_hd, 'REFPROP::Ammonia')-273.15

        coef_p = [6091.8748892052, 41.4177945033, 361.6132671939, 2.7293850346,
                  7.7267739693, -1.6873740008, 0.0136121181, -0.0342046757,
                  -0.0514325376, 0.0236603063]
        p_v = coef_p[0] + coef_p[1]*to+coef_p[2]*tc+coef_p[3]*to**2+coef_p[4] * \
              to*tc+coef_p[5]*tc**2+coef_p[6]*to**3+coef_p[7]*tc*to**2+coef_p[8]* \
              to*tc**2+coef_p[9]*tc**3
        p_v = (p_v/2900)*self.n

        return p_v

    def stoffdaten_arm(self):

        return 'REFPROP::Ammonia[%s]&Water[%s]' % (self.x_arm, 1-self.x_arm)

    def stoffdaten_reich(self):

        x_reich = self.konzentration_reich()

        test =  'REFPROP::Ammonia[%s]&Water[%s]' % (x_reich, 1-x_reich)
        return test

    def converted_massenstrom_arm(self):
        return self.m_liq * PropsSI('D', 'T', self.t_liq+273.15, 'P', self.p_hd, self.stoffdaten_arm())*(1.0/60000)


    def massenstrom_reicheloesung(self):
        
        m_vap = self.verdichter_massenstrom()
        return m_vap + self.converted_massenstrom_arm()

    def konzentration_reich(self):

        x_reich = (self.verdichter_massenstrom()+self.converted_massenstrom_arm()*self.x_arm) / self.massenstrom_reicheloesung()
        return x_reich

    # def set_outside()