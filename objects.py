__all__ = ['celestial_objects']


def celestial_objects(moon, set=1):
    m_sol = 1.988e30
    m_jup = 1.898e27
    r_sol = 696340e3
    r_jup = 69911e3
    au = 149597870700

    if moon:
        # Jovian system
        # -------------
        celest1 = {
            "star": {"m": 1.988e30,
                     "hash": 'star',
                     "r": 696340000
                     },
            "planet": {"m": 1.898e27,
                       "a": 7.785e11,
                       "e": 0.0489,
                       "inc": 0.0227,
                       "r": 69911000,
                       "primary": 'star',
                       "hash": 'planet'
                       },
            "moon": {"m": 4.799e22,  # Europa
                     "a": 6.709e8,
                     "e": 0.009,
                     "inc": 0.0082,
                     "r": 1560800,
                     "primary": 'planet',
                     "hash": 'moon'
                     },
            "add1": {"m": 8.932e22,  # Io
                     "a": 4.217e8,
                     "e": 0.0041,
                     "r": 1821600,
                     "primary": 'planet'
                     },
            "add2": {"m": 1.4819e23,  # Ganymede
                     "a": 1070400000,
                     "e": 0.0013,
                     "inc": 0.00349,
                     "r": 2410300,
                     "primary": 'planet'
                     },
            "add3": {"m": 1.0759e22,  # Callisto
                     "a": 1882700000,
                     "e": 0.0074,
                     "inc": 0.00335,
                     "primary": 'planet'
                     }
        }

        # WASP 49
        # -------
        celest2 = {
            "star": {"m": 0.72 * m_sol,
                     "hash": 'star',
                     "r": 1.038 * r_sol
                     },
            "planet": {"m": 0.378 * m_jup,
                       "a": 0.0378 * au,
                       "r": 1.115 * r_jup,
                       "primary": 'star',
                       "hash": 'planet'
                       },
            "moon": {"m": 3.8e24,
                     "a": 1.74 * 1.115 * r_jup,
                     "r": 6370e3,
                     "primary": 'planet',
                     "hash": 'moon'
                     }
        }

        # HD 189733
        # -------
        celest3 = {
            "star": {"m": 0.8 * m_sol,
                     "hash": 'star',
                     "r": 0.805 * r_sol
                     },
            "planet": {"m": 1.138 * m_jup,
                       "a": 0.031 * au,
                       "r": 1.138 * r_jup,
                       "primary": 'star',
                       "hash": 'planet'
                       },
            "moon": {"m": 3.8e24,
                     "a": 2.11 * 1.138 * r_jup,
                     "r": 6370e3,
                     "primary": 'planet',
                     "hash": 'moon'
                     }
        }

        # HD 209458
        # ---------
        celest4 = {
            "star": {"m": 1.148 * m_sol,
                     "hash": 'star',
                     "r": 1.203 * r_sol
                     },
            "planet": {"m": 0.69 * m_jup,
                       "a": 0.0475 * au,
                       "r": 1.38 * r_jup,
                       "primary": 'star',
                       "hash": 'planet'
                       },
            "moon": {"m": 3.8e24,
                     "a": 1.93 * 1.38 * r_jup,
                     "r": 6370e3,
                     "primary": 'planet',
                     "hash": 'moon'
                     }
        }

        # HAT-P-1
        # ---------
        celest5 = {
            "star": {"m": 1.151 * m_sol,
                     "hash": 'star',
                     "r": 1.174 * r_sol
                     },
            "planet": {"m": 0.525 * m_jup,
                       "a": 0.0556 * au,
                       "r": 1.319 * r_jup,
                       "primary": 'star',
                       "hash": 'planet'
                       },
            "moon": {"m": 3.8e24,
                     "a": 2.28 * 1.319 * r_jup,
                     "r": 6370e3,
                     "primary": 'planet',
                     "hash": 'moon'
                     }
        }

    else:
        # 55 Cnc-e
        # --------
        celest1 = {
            "star": {"m": 1.799e30,
                     "hash": 'star',
                     "r": 6.56e8
                     },
            "planet": {"m": 4.77179e25,
                       "a": 2.244e9,
                       "e": 0.05,
                       "inc": 0.00288,
                       "r": 1.196e7,
                       "primary": 'star',
                       "hash": 'planet'}
        }

    try:
        return locals()[f"celest{locals()['set']}"]
    except:
        print("Celestial body set not found. Returning set 1. ")
        return celest1
