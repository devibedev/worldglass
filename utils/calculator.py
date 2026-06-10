import re
import math

LINEA_NACIONAL_1_5_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Línea Nacional 1 ½\" (Económica)",
        "barra_std_mm": 6100,
        "perfiles": {
            "11838": "Riel 1 ½\"",
            "11836": "Cerco 1 ½\"",
            "11835": "Jamba 1 ½\"",
            "1044": "Zoclo Cabezal 1 ½\""
        }
    },
    "configuraciones": {
        "XO_VENTANA_1_5": {
            "descripcion": "Ventana Corrediza 1 ½\" Económica (XO)",
            "perfiles": [
                {"componente": "Riel", "clave": "11838", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Cabezal Marco", "clave": "11835", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jambas", "clave": "11835", "cantidad": 2, "corte_mm": "ALT - 20"},
                {"componente": "Zoclo/Cabezal Hoja", "clave": "1044", "cantidad": 4, "corte_mm": "(AT - 80) / 2"},
                {"componente": "Cerco/Traslape", "clave": "11836", "cantidad": 4, "corte_mm": "ALT - 30"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 35", "alto_mm": "ALT - 65"}],
            "consumibles": []
        }
    }
}

CANCEL_BANO_LINEAL_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Cancel de Baño Semilujo/Económico",
        "barra_std_mm": 6100,
        "perfiles": {
            "1174": "Riel Superior", "1387": "Riel Inferior", "1386": "Jamba Lateral",
            "1104": "Marco Semilujo 1 ¾\"", "9525": "Marco Económico 1 ¼\"", "4154": "Jaladera"
        }
    },
    "configuraciones": {
        "CANCEL_CORREDIZO_SEMILUJO": {
            "descripcion": "Cancel de Baño Corredizo Semilujo",
            "perfiles": [
                {"componente": "Riel Superior", "clave": "1174", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Riel Inferior", "clave": "1387", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jambas Laterales", "clave": "1386", "cantidad": 2, "corte_mm": "ALT"},
                {"componente": "Marco/Cerco Hoja", "clave": "1104", "cantidad": 4, "corte_mm": "ALT - 45"},
                {"componente": "Zoclo/Cabezal Hoja", "clave": "1104", "cantidad": 4, "corte_mm": "(AT / 2) - 20"}
            ],
            "vidrios": [{"tipo": "plastico/cristal", "cantidad": 2, "ancho_mm": "(AT / 2) - 10", "alto_mm": "ALT - 80"}],
            "consumibles": []
        }
    }
}

CANCEL_BANO_PREMIUM_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Herrajes Premium (Acero Inoxidable)",
        "barra_std_mm": 2000, # Rieles suelen venir en 2m para estos kits
        "perfiles": {
            "1305": "Kit Bacalar (Rectangular)",
            "1306": "Kit Tubular Redondo",
            "tub_30_10": "Riel Rectangular 30x10mm",
            "tub_red": "Riel Tubular Redondo"
        }
    },
    "configuraciones": {
        "BACALAR_1305": {
            "descripcion": "Cancel de Baño Bacalar 1305 (1 Fijo, 1 Corredizo)",
            "perfiles": [
                {"componente": "Riel Rectangular", "clave": "tub_30_10", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Kit de Herrajes Bacalar", "clave": "1305", "cantidad": 1, "corte_mm": "0"}
            ],
            "vidrios": [
                {"tipo": "fijo templado", "cantidad": 1, "ancho_mm": "(AT / 2) + 60", "alto_mm": "ALT"},
                {"tipo": "corredizo templado", "cantidad": 1, "ancho_mm": "AT / 2", "alto_mm": "ALT - 8"}
            ],
            "consumibles": [
                { "componente": "Sello magnético", "formula_mm": "ALT" },
                { "componente": "Guía de piso", "formula_mm": "0" }
            ]
        },
        "TUBULAR_1306": {
            "descripcion": "Sistema Corredizo Tubular Redondo 1306",
            "perfiles": [
                {"componente": "Riel Tubular Redondo", "clave": "tub_red", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Kit de Herrajes 1306", "clave": "1306", "cantidad": 1, "corte_mm": "0"}
            ],
            "vidrios": [
                {"tipo": "fijo templado", "cantidad": 1, "ancho_mm": "(AT / 2) + 50", "alto_mm": "ALT"},
                {"tipo": "corredizo templado", "cantidad": 1, "ancho_mm": "(AT / 2) + 50", "alto_mm": "ALT + 23"}
            ],
            "consumibles": [
                { "componente": "Topes de riel", "formula_mm": "0" }
            ]
        }
    }
}

TEMPERED_SYSTEMS_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Cristal Templado y Herrajes (Conalum)",
        "barra_std_mm": 0, # No usa barras, usa kits
        "perfiles": {
            "1035": "Bisagra Muro-Vidrio 90°",
            "1173": "Chapa de Acero Inoxidable",
            "2226": "Jaladera Tipo H (300mm)",
            "1106": "Conector Muro-Vidrio",
            "2325": "Mini Poste 150mm"
        }
    },
    "configuraciones": {
        "PUERTA_BATIENTE_TEMPLADO": {
            "descripcion": "Puerta Batiente de Cristal Templado (8-12mm)",
            "perfiles": [
                {"componente": "Bisagra Superior", "clave": "1035", "cantidad": 1, "corte_mm": "0"},
                {"componente": "Bisagra Inferior", "clave": "1035", "cantidad": 1, "corte_mm": "0"},
                {"componente": "Jaladera Tipo H", "clave": "2226", "cantidad": 1, "corte_mm": "0"},
                {"componente": "Chapa (Opcional)", "clave": "1173", "cantidad": 1, "corte_mm": "0"}
            ],
            "vidrios": [
                {"tipo": "templado 10mm", "cantidad": 1, "ancho_mm": "AT - 6", "alto_mm": "ALT - 10"}
            ],
            "consumibles": [
                { "componente": "Resaque para bisagra", "formula_mm": "2" },
                { "componente": "Barreno para jaladera", "formula_mm": "2" }
            ]
        }
    }
}

EUROALUM_SERIE_2500_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Euroalum Serie 2500 (Versátil)",
        "barra_std_mm": 6100,
        "perfiles": {
            "1678": "Marco Puerta", "1681": "Hoja Ventana Apertura Interior", "1679": "Marco con Mosquitero",
            "1675": "Hoja Ventana Apertura Exterior", "1682": "Hoja Puerta Apertura Exterior", "1692": "Zoclo",
            "1677": "Marco Ventana", "1680": "Hoja Ventana Apertura Interior", "1683": "Hoja Puerta Apertura Interior",
            "1669": "Pletina", "1684": "Junquillo", "1668": "Junquillo Redondo", "1688": "Marco de Lujo",
            "1686": "Junquillo Duo", "1667": "Junquillo Redondo Duo", "1689": "Hoja de Lujo Apertura Exterior",
            "1654": "Hoja de Lujo Apertura Interior", "1690": "Intermedio de Lujo", "2500": "Perfil Genérico 2500"
        }
    },
    "configuraciones": {
        "VENTANA_BATIENTE_2500": {
            "descripcion": "Ventana Batiente Serie 2500 (1 Hoja)",
            "perfiles": [
                {"componente": "Marco Horizontal", "clave": "1677", "cantidad": 2, "corte_mm": "AT"},
                {"componente": "Marco Vertical", "clave": "1677", "cantidad": 2, "corte_mm": "ALT"},
                {"componente": "Hoja Horizontal", "clave": "1675", "cantidad": 2, "corte_mm": "AT - 50"},
                {"componente": "Hoja Vertical", "clave": "1675", "cantidad": 2, "corte_mm": "ALT - 50"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 1, "ancho_mm": "AT - 100", "alto_mm": "ALT - 100"}],
            "consumibles": []
        }
    }
}

EUROALUM_SERIE_2800_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Euroalum Serie 2800 (Ventana Corrediza)",
        "barra_std_mm": 6100,
        "perfiles": {
            "12156": "Zoclo Duo", "12157": "Cerco Duo", "12158": "Traslape Duo", "12150": "Riel Inferior",
            "12153": "Zoclo", "12154": "Cerco", "12155": "Traslape", "12152": "Jamba", "12161": "Marco Fijo",
            "12151": "Riel Superior", "12159": "Mosquitero", "12160": "Adaptador OXXO", "2800": "Perfil Genérico 2800"
        }
    },
    "configuraciones": {
        "XO_VENTANA_2800": {
            "descripcion": "Ventana Corrediza Serie 2800 (1 Fijo, 1 Corredizo)",
            "perfiles": [
                {"componente": "Riel Inferior", "clave": "12150", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Riel Superior", "clave": "12151", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jambas", "clave": "12152", "cantidad": 2, "corte_mm": "ALT"},
                {"componente": "Zoclo Hoja", "clave": "12153", "cantidad": 2, "corte_mm": "(AT - 100) / 2"},
                {"componente": "Cerco Hoja", "clave": "12154", "cantidad": 2, "corte_mm": "ALT - 50"},
                {"componente": "Traslape Hoja", "clave": "12155", "cantidad": 2, "corte_mm": "ALT - 50"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 60", "alto_mm": "ALT - 100"}],
            "consumibles": []
        }
    }
}

EUROALUM_SERIE_3500_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Euroalum Serie 3500 (Puerta Batiente)",
        "barra_std_mm": 6100,
        "perfiles": {
            "2277": "Cabezal", "2215": "Intermedio", "2278": "Zoclo", "2287": "Cerco Chapa",
            "2273": "Contramarco", "2274": "Contramarco Abierto", "2275": "Contramarco Residencial",
            "2279": "Zoclo Residencial", "12017": "Junta de Hermeticidad", "2288": "Cerco Residencial",
            "2223": "Junquillo Duo", "2227": "Junquillo Colonial", "2216": "Intermedio Residencial",
            "2220": "Junquillo", "2221": "Junquillo Redondo", "2222": "Junquillo Biselado",
            "2348": "Mullion", "2289": "Adaptador para Cerco Chapa", "3500": "Perfil Genérico 3500"
        }
    },
    "configuraciones": {
        "PUERTA_BATIENTE_3500": {
            "descripcion": "Puerta Batiente Serie 3500 (1 Hoja)",
            "perfiles": [
                {"componente": "Contramarco Horizontal", "clave": "2273", "cantidad": 2, "corte_mm": "AT"},
                {"componente": "Contramarco Vertical", "clave": "2273", "cantidad": 2, "corte_mm": "ALT"},
                {"componente": "Cerco Chapa", "clave": "2287", "cantidad": 2, "corte_mm": "ALT - 44"},
                {"componente": "Zoclo Residencial", "clave": "2279", "cantidad": 1, "corte_mm": "AT - 50"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 1, "ancho_mm": "AT - 120", "alto_mm": "ALT - 120"}],
            "consumibles": []
        }
    }
}

EUROALUM_SERIE_3800_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Euroalum Serie 3800 (Ventana/Puerta Corrediza)",
        "barra_std_mm": 6100,
        "perfiles": {
            "12263": "Riel Doble", "12302": "Riel Doble con Ceja", "12271": "Riel Colgante", "12264": "Riel Triple",
            "12208": "Jamba Doble", "12209": "Jamba Triple", "12292": "Adaptador OXXO", "12272": "Guia para Mosquitero",
            "2138": "Hoja Mosquitero", "12289": "Cerco Ventana Duo", "12240": "Zoclo y Cabezal Ventana",
            "12288": "Cerco Ventana", "12241": "Zoclo y Cabezal Ventana Duo", "12298": "Traslape Ventana Duo",
            "12297": "Traslape Ventana", "12301": "Goterón", "12315": "Adaptador Mosquitero",
            "2214": "Guía de Refuerzo", "2218": "Refuerzo", "12246": "Zoclo y Cabezal Puerta Duo",
            "12291": "Cerco Puerta Duo", "12300": "Traslape Puerta Duo", "12245": "Zoclo y Cabezal Puerta",
            "12290": "Cerco Puerta", "12299": "Traslape Puerta", "3800": "Perfil Genérico 3800"
        }
    },
    "configuraciones": {
        "XO_VENTANA_3800": {
            "descripcion": "Ventana Corrediza Serie 3800 (1 Fijo, 1 Corredizo)",
            "perfiles": [
                {"componente": "Riel Doble", "clave": "12263", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jamba Doble", "clave": "12208", "cantidad": 2, "corte_mm": "ALT"},
                {"componente": "Zoclo y Cabezal Ventana", "clave": "12240", "cantidad": 2, "corte_mm": "(AT - 100) / 2"},
                {"componente": "Cerco Ventana", "clave": "12288", "cantidad": 2, "corte_mm": "ALT - 50"},
                {"componente": "Traslape Ventana", "clave": "12297", "cantidad": 2, "corte_mm": "ALT - 50"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 70", "alto_mm": "ALT - 120"}],
            "consumibles": []
        }
    }
}

EUROALUM_SERIE_3900_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Euroalum Serie 3900 (Puerta Corrediza)",
        "barra_std_mm": 6100,
        "perfiles": {
            "12303": "Riel Doble", "12305": "Jamba Doble", "12307": "Zoclo y Cabezal", "12308": "Cerco",
            "12309": "Traslape", "12306": "Adaptador Jamba", "12304": "Adaptador Riel", "12314": "Mullion",
            "12315": "Adaptador Mosquitero", "12313": "Adaptador OXXO", "12311": "Cerco Duo",
            "12312": "Traslape Duo", "12310": "Zoclo y Cabezal Duo", "3900": "Perfil Genérico 3900"
        }
    },
    "configuraciones": {
        "XO_PUERTA_3900": {
            "descripcion": "Puerta Corrediza Serie 3900 (1 Fijo, 1 Corredizo)",
            "perfiles": [
                {"componente": "Riel Doble", "clave": "12303", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jamba Doble", "clave": "12305", "cantidad": 2, "corte_mm": "ALT"},
                {"componente": "Zoclo y Cabezal", "clave": "12307", "cantidad": 2, "corte_mm": "(AT - 100) / 2"},
                {"componente": "Cerco", "clave": "12308", "cantidad": 2, "corte_mm": "ALT - 50"},
                {"componente": "Traslape", "clave": "12309", "cantidad": 2, "corte_mm": "ALT - 50"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 70", "alto_mm": "ALT - 120"}],
            "consumibles": []
        }
    }
}

EUROALUM_SERIE_4000_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Euroalum Serie 4000 (Lujo y Confort)",
        "barra_std_mm": 6100,
        "perfiles": {
            "2314": "Riel Doble", "2346": "Riel Triple", "2361": "Adaptador Riel", "2276": "Adaptador Traslape Ventana",
            "2297": "Hoja Ventana", "2298": "Hoja Ventana Duo", "2199": "Mosquitero Ventana", "2292": "Adaptador OXXO",
            "2316": "Hoja Puerta", "2319": "Hoja Puerta Duo", "2198": "Mosquitero Puerta", "2251": "Intermedio Hoja",
            "2218": "Perfil de Refuerzo", "2214": "Guia de Refuerzo", "2344": "Adaptador Traslape Puerta",
            "2188": "Tapa Refuerzo", "12012": "Junquillo Redondo", "12010": "Junquillo Redondo Duo", "12009": "Fijo",
            "12013": "Fijo", "12015": "Intermedio", "12016": "Refuerzo", "4000": "Perfil Genérico 4000"
        }
    },
    "configuraciones": {
        "XO_VENTANA_4000": {
            "descripcion": "Ventana Corrediza Serie 4000 (1 Fijo, 1 Corredizo)",
            "perfiles": [
                {"componente": "Riel Doble", "clave": "2314", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Hoja Ventana", "clave": "2297", "cantidad": 2, "corte_mm": "(AT - 100) / 2"},
                {"componente": "Hoja Ventana Duo", "clave": "2298", "cantidad": 2, "corte_mm": "ALT - 50"},
                {"componente": "Adaptador Riel", "clave": "2361", "cantidad": 1, "corte_mm": "AT"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 60", "alto_mm": "ALT - 100"}],
            "consumibles": []
        }
    }
}

EUROALUM_SERIE_4500_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Euroalum Serie 4500 (Grandes Dimensiones)",
        "barra_std_mm": 6100,
        "perfiles": {
            "4057": "Riel Triple", "4053": "Riel Bajo Doble", "4054": "Riel Bajo Triple", "4041": "Riel Doble",
            "4045": "Adaptador Riel", "4024": "Adaptador Riel Bajo", "4050": "Adaptador OXXO",
            "2218": "Perfil de Refuerzo", "4055": "Hoja", "4086": "Hoja Vidrio Laminado", "4056": "Hoja Duo",
            "4059": "Mosquitero", "4044": "Adaptador Traslape", "2214": "Guía de Refuerzo", "12013": "Fijo",
            "12014": "Fijo", "12015": "Intermedio", "2188": "Tapa Refuerzo", "12016": "Refuerzo",
            "12010": "Junquillo Redondo Duo", "12012": "Junquillo Redondo", "4500": "Perfil Genérico 4500"
        }
    },
    "configuraciones": {
        "XO_PUERTA_4500": {
            "descripcion": "Puerta Corrediza Serie 4500 (1 Fijo, 1 Corredizo)",
            "perfiles": [
                {"componente": "Riel Doble", "clave": "4041", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Hoja Duo", "clave": "4056", "cantidad": 2, "corte_mm": "(AT - 100) / 2"},
                {"componente": "Hoja", "clave": "4055", "cantidad": 2, "corte_mm": "ALT - 60"},
                {"componente": "Adaptador Traslape", "clave": "4044", "cantidad": 1, "corte_mm": "ALT - 60"}
            ],
            "vidrios": [{"tipo": "laminado", "cantidad": 2, "ancho_mm": "(AT / 2) - 80", "alto_mm": "ALT - 140"}],
            "consumibles": []
        }
    }
}

CUPRUM_SERIE_2_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Ventana y Puerta Corrediza 2.000\"",
        "barra_std_mm": 6100,
        "perfiles": {
            "27819": "Cabezal mosquitero corredizo",
            "67518": "Cabezal y jamba",
            "9956": "Cabezal y zoclo hoja",
            "11044": "Cabezal y zoclo hoja",
            "68370": "Riel con mosquitero ext.",
            "14286": "Riel",
            "67825": "Zoclo puerta",
            "67819": "Cabezal mosquitero colgante",
            "38370": "Riel con mosq. ext",
            "27525": "Cerco fijo económico",
            "8320": "Cerco ventana",
            "67821": "Cerco puerta",
            "39954": "Traslape ventana",
            "69955": "Traslape puerta",
            "67822": "Cerco OXXO puerta",
            "7818": "Adaptador XX",
            "66534": "Cerco mosquitero",
            "66533": "Cabezal y zoclo mosquitero"
        }
    },
    "configuraciones": {
        "XO_VENTANA_2": {
            "descripcion": "Ventana Corrediza 2\" económica (1 fijo, 1 corredizo).",
            "perfiles": [
                {"componente": "Riel", "clave": "14286", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Cabezal", "clave": "67518", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jambas", "clave": "67518", "cantidad": 2, "corte_mm": "ALT - 25"},
                {"componente": "Zoclo Hoja", "clave": "9956", "cantidad": 2, "corte_mm": "(AT - 102) / 2"},
                {"componente": "Cabezal Hoja", "clave": "9956", "cantidad": 2, "corte_mm": "(AT - 102) / 2"},
                {"componente": "Cerco", "clave": "8320", "cantidad": 2, "corte_mm": "ALT - 35"},
                {"componente": "Traslape", "clave": "39954", "cantidad": 2, "corte_mm": "ALT - 35"}
            ],
            "vidrios": [
                {"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 45", "alto_mm": "ALT - 85"}
            ],
            "consumibles": []
        }
    }
}

CUPRUM_SERIE_3_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Ventana y puerta corrediza de 3.000 x 1.250",
        "barra_std_mm": 6100,
        "perfiles": {
            "67826": "Cabezal y jamba",
            "69957": "Riel",
            "67835": "Zoclo ventana",
            "67842": "Zoclo puerta",
            "67836": "Cabezal ventana",
            "67843": "Cerco ventana",
            "67844": "Cerco traslape ventana",
            "67847": "Cerco chapa puerta",
            "67848": "Traslape puerta",
            "66533": "Cabezal y zoclo mosquitero",
            "66534": "Cerco mosquitero",
            "9966": "Adaptador mosquitero",
            "2522": "Empaque",
            "11032": "Empaque",
            "36370": "Empaque",
            "59204": "Cuña",
            "29207": "Respaldo",
            "29187": "Respaldo"
        }
    },
    "configuraciones": {
        "XO_PUERTA_CERCO_TRASLAPE_PUERTA": {
            "descripcion": "Caso tipo 1.x: XO con cerco chapa y traslape puerta, 3 paños (1 fijo, 2 corredizos).",
            "perfiles": [
                {"componente": "Riel 3\"", "clave": "69957", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jamba (cabezal)", "clave": "67826", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Adaptador paloma", "clave": "adapt_paloma", "cantidad": 1, "corte_mm": "AT - 65"},
                {"componente": "Jambas", "clave": "67826", "cantidad": 2, "corte_mm": "ALT - 26"},
                {"componente": "Zoclos", "clave": "67842", "cantidad": 3, "corte_mm": "(AT - 167) / 3"},
                {"componente": "Cabezales", "clave": "67836", "cantidad": 3, "corte_mm": "(AT - 167) / 3"},
                {"componente": "Cerco chapa fijo", "clave": "67847", "cantidad": 1, "corte_mm": "ALT"},
                {"componente": "Cerco chapa corredizo", "clave": "67847", "cantidad": 1, "corte_mm": "ALT - 40"},
                {"componente": "Traslape fijo", "clave": "67848", "cantidad": 1, "corte_mm": "ALT"},
                {"componente": "Traslapes corredizos", "clave": "67848", "cantidad": 3, "corte_mm": "ALT - 40"}
            ],
            "vidrios": [
                {"tipo": "fijo", "cantidad": 1, "ancho_mm": "(AT - 117) / 3", "alto_mm": "ALT - 95"},
                {"tipo": "corredizo", "cantidad": 2, "ancho_mm": "(AT - 117) / 3", "alto_mm": "ALT - 135"}
            ],
            "consumibles": [
                { "componente": "Felpa", "formula_mm": "(AT * 5) + (ALT * 8)" },
                { "componente": "Vinil", "formula_mm": "(AT * 2) + (ALT * 9)" }
            ]
        },
        "OXXO_PUERTA_MOSQ_CERCO_TRASLAPE_PUERTA": {
            "descripcion": "Caso tipo 2.x: OXXO con mosquitero, 4 paños, con cerco chapa y traslape puerta.",
            "perfiles": [
                {"componente": "Riel 3\"", "clave": "69957", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jamba c/mosquitero", "clave": "67826", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Adaptador mosquitero", "clave": "9966", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jambas", "clave": "67826", "cantidad": 2, "corte_mm": "ALT - 26"},
                {"componente": "Zoclos", "clave": "67842", "cantidad": 4, "corte_mm": "(AT - 330) / 4"},
                {"componente": "Cabezales", "clave": "67836", "cantidad": 4, "corte_mm": "(AT - 330) / 4"},
                {"componente": "Cerco chapa fijos", "clave": "67847", "cantidad": 2, "corte_mm": "ALT - 30"},
                {"componente": "Cerco chapa corredizos", "clave": "67847", "cantidad": 2, "corte_mm": "ALT - 40"},
                {"componente": "Traslapes fijos", "clave": "67848", "cantidad": 2, "corte_mm": "ALT - 30"},
                {"componente": "Traslapes corredizos", "clave": "67848", "cantidad": 2, "corte_mm": "ALT - 40"},
                {"componente": "Vertical mosquitero", "clave": "66534", "cantidad": 4, "corte_mm": "ALT - 20"},
                {"componente": "Horizontal mosquitero", "clave": "66533", "cantidad": 4, "corte_mm": "(AT - 10) / 4"},
                {"componente": "Adaptador OXXO", "clave": "adapt_oxxo", "cantidad": 2, "corte_mm": "ALT - 50"}
            ],
            "vidrios": [
                {"tipo": "fijo", "cantidad": 2, "ancho_mm": "(AT - 265) / 4", "alto_mm": "ALT - 125"},
                {"tipo": "corredizo", "cantidad": 2, "ancho_mm": "(AT - 265) / 4", "alto_mm": "ALT - 135"}
            ],
            "consumibles": [
                { "componente": "Felpa", "formula_mm": "(AT * 5) + (ALT * 10)" },
                { "componente": "Vinil 11 peine", "formula_mm": "(AT * 2) + (ALT * 8)" }
            ]
        },
        "XO_VENTANA_CERCO_TRASLAPE_VENTANA": {
            "descripcion": "XO ventana usando cerco 67843 y traslape 67844 en lugar de perfiles de puerta.",
            "perfiles": [
                {"componente": "Riel 3\"", "clave": "69957", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Cabezal 3\"", "clave": "67826", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Jambas", "clave": "67826", "cantidad": 2, "corte_mm": "ALT - 26"},
                {"componente": "Zoclo 3\"", "clave": "67835", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Cerco fijo", "clave": "67843", "cantidad": 1, "corte_mm": "ALT - 30"},
                {"componente": "Cerco corredizo", "clave": "67843", "cantidad": 1, "corte_mm": "ALT - 40"},
                {"componente": "Traslape fijo", "clave": "67844", "cantidad": 1, "corte_mm": "ALT - 30"},
                {"componente": "Traslape corredizo", "clave": "67844", "cantidad": 1, "corte_mm": "ALT - 40"}
            ],
            "vidrios": [],
            "consumibles": []
        }
    }
}

CUPRUM_SERIE_3100_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Serie 3100 Batiente/Fija",
        "barra_std_mm": 6100,
        "perfiles": {
            "1830": "Cerco liso ventana", "1823": "Pilastra lisa ventana", "1824": "Hoja lisa ventana",
            "1825": "Cerco liso puerta", "1826": "Pilastra lisa puerta", "1829": "Zoclo inferior 5\"",
            "1832": "Hoja lisa monumental", "2351": "Fijo riel triple", "667": "Junquillo duo redondo"
        }
    },
    "configuraciones": {
        "VENTANA_BATIENTE_3100": {
            "descripcion": "Ventana Batiente 1 Hoja Serie 3100",
            "perfiles": [
                {"componente": "Cerco Horizontal", "clave": "1830", "cantidad": 2, "corte_mm": "AT"},
                {"componente": "Cerco Vertical", "clave": "1830", "cantidad": 2, "corte_mm": "ALT"},
                {"componente": "Hoja Horizontal", "clave": "1824", "cantidad": 2, "corte_mm": "AT - 51"},
                {"componente": "Hoja Vertical", "clave": "1824", "cantidad": 2, "corte_mm": "ALT - 51"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 1, "ancho_mm": "AT - 90", "alto_mm": "ALT - 90"}],
            "consumibles": []
        }
    }
}

CUPRUM_SERIE_4100_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Serie 4100 Corrediza",
        "barra_std_mm": 6100,
        "perfiles": {
            "12550": "Riel 3 vías", "508": "Riel adicional", "298": "Hoja baja perimetral duo",
            "319": "Hoja alta perimetral duo", "199": "Hoja baja perimetral mosquitero",
            "317": "Hoja alta perimetral mosquitero", "276": "Traslape hoja baja",
            "344": "Traslape hoja alta", "292": "Unión 4 hojas"
        }
    },
    "configuraciones": {
        "XO_VENTANA_4100": {
            "descripcion": "Ventana Corrediza Serie 4100 (1 fijo, 1 corredizo)",
            "perfiles": [
                {"componente": "Riel", "clave": "12550", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Marco Cabezal/Jambas", "clave": "12550", "cantidad": 3, "corte_mm": "ALT"},
                {"componente": "Hoja Horizontal", "clave": "298", "cantidad": 4, "corte_mm": "(AT / 2) - 64"},
                {"componente": "Hoja Vertical", "clave": "298", "cantidad": 4, "corte_mm": "ALT - 45"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 100", "alto_mm": "ALT - 100"}],
            "consumibles": []
        }
    }
}

CUPRUM_SERIE_5100_DATA = {
    "version": "1.0",
    "catalogo": {
        "serie": "Serie 5100 Corrediza Pesada",
        "barra_std_mm": 6100,
        "perfiles": {
            "1546": "Riel bajo 2 vías con ceja", "548": "Riel adicional", "56": "Hoja perimetral duo",
            "59": "Hoja perimetral mosquitero", "44": "Traslape", "58": "Unión 4 hojas"
        }
    },
    "configuraciones": {
        "XO_VENTANA_5100": {
            "descripcion": "Ventana Corrediza Serie 5100 (1 fijo, 1 corredizo)",
            "perfiles": [
                {"componente": "Riel", "clave": "1546", "cantidad": 1, "corte_mm": "AT"},
                {"componente": "Marco Cabezal/Jambas", "clave": "1546", "cantidad": 3, "corte_mm": "ALT"},
                {"componente": "Hoja Horizontal", "clave": "56", "cantidad": 4, "corte_mm": "(AT / 2) - 54"},
                {"componente": "Hoja Vertical", "clave": "56", "cantidad": 4, "corte_mm": "ALT - 60"}
            ],
            "vidrios": [{"tipo": "claro", "cantidad": 2, "ancho_mm": "(AT / 2) - 110", "alto_mm": "ALT - 110"}],
            "consumibles": []
        }
    }
}

def evaluate_formula(formula: str, at: float, alt: float) -> float:
    """Convierte texto como '(AT - 167) / 3' en un número real"""
    # Sanitización básica: solo permitir números, operadores y AT/ALT
    clean_formula = formula.replace("AT", str(at)).replace("ALT", str(alt))
    try:
        # Usamos un diccionario vacío para __builtins__ por seguridad
        return round(float(eval(clean_formula, {"__builtins__": None}, {})), 2)
    except Exception as e:
        print(f"Error evaluando formula {formula}: {e}")
        return 0.0

def calculate_cuprum_despiece(at_mm: float, alt_mm: float, config_id: str, serie: str = "3", merma_pct: float = 0.05):
    """
    Calcula el despiece completo para Series (1.5, 2, 3, 3100, 4100, 5100, cancel_bano).
    """
    series_map = {
        "1.5": LINEA_NACIONAL_1_5_DATA,
        "2": CUPRUM_SERIE_2_DATA,
        "3": CUPRUM_SERIE_3_DATA,
        "3100": CUPRUM_SERIE_3100_DATA,
        "4100": CUPRUM_SERIE_4100_DATA,
        "5100": CUPRUM_SERIE_5100_DATA,
        "cancel_bano": CANCEL_BANO_LINEAL_DATA,
        "premium": CANCEL_BANO_PREMIUM_DATA,
        "tempered": TEMPERED_SYSTEMS_DATA,
        "euroalum_2500": EUROALUM_SERIE_2500_DATA,
        "euroalum_2800": EUROALUM_SERIE_2800_DATA,
        "euroalum_3500": EUROALUM_SERIE_3500_DATA,
        "euroalum_3800": EUROALUM_SERIE_3800_DATA,
        "euroalum_3900": EUROALUM_SERIE_3900_DATA,
        "euroalum_4000": EUROALUM_SERIE_4000_DATA,
        "euroalum_4500": EUROALUM_SERIE_4500_DATA
    }
    dataset = series_map.get(serie, CUPRUM_SERIE_3_DATA)
    
    config = dataset["configuraciones"].get(config_id)
    if not config:
        return {"error": "Configuración no encontrada"}

    resultado = {
        "vista_cliente": {
            "configuracion": config_id.replace("_", " "),
            "dimensiones_totales": {"ancho": at_mm, "alto": alt_mm},
            "vidrios": []
        },
        "vista_tecnica": {
            "cortes_perfiles": [],
            "optimizacion_barras": [],
            "consumibles": []
        }
    }

    # 1. Calcular cortes individuales
    claves_totales = {} # Para sumar longitud total por clave de perfil

    for p in config["perfiles"]:
        longitud_corte = evaluate_formula(p["corte_mm"], at_mm, alt_mm)
        resultado["vista_tecnica"]["cortes_perfiles"].append({
            "componente": p["componente"],
            "clave": p["clave"],
            "cantidad": p["cantidad"],
            "medida_mm": longitud_corte
        })

        # Sumar para el cálculo de barras
        if p["clave"] in dataset["catalogo"]["perfiles"]:
            claves_totales[p["clave"]] = claves_totales.get(p["clave"], 0) + (longitud_corte * p["cantidad"])

    # 2. Calcular vidrios
    for v in config["vidrios"]:
        resultado["vista_cliente"]["vidrios"].append({
            "tipo": v["tipo"],
            "cantidad": v["cantidad"],
            "ancho_mm": evaluate_formula(v["ancho_mm"], at_mm, alt_mm),
            "alto_mm": evaluate_formula(v["alto_mm"], at_mm, alt_mm)
        })

    # 3. Calcular consumibles
    for c in config.get("consumibles", []):
        resultado["vista_tecnica"]["consumibles"].append({
            "componente": c["componente"],
            "medida_mm": evaluate_formula(c["formula_mm"], at_mm, alt_mm)
        })

    # 4. Calcular barras de 6.10m necesarias
    BARRA_STD_MM = dataset["catalogo"]["barra_std_mm"]
    for clave, longitud_total in claves_totales.items():
        longitud_con_merma = longitud_total * (1 + merma_pct)
        barras_necesarias = math.ceil(longitud_con_merma / BARRA_STD_MM)

        resultado["vista_tecnica"]["optimizacion_barras"].append({
            "clave": clave,
            "longitud_total_mm": round(longitud_total, 2),
            "longitud_con_merma_mm": round(longitud_con_merma, 2),
            "barras_6_10m": barras_necesarias
        })

    return resultado

def calculate_shower_door(width_cm: int, height_cm: int, color: str = "natural", glass_type: str = "9mm") -> dict:
    """
    Calcula precio de cancel de baño basado en dimensiones y materiales.

    Fórmula:
    - Precio por m2 de aluminio (según color)
    - Precio por m2 de cristal (según grosor)
    - Herrajes (fijo)
    - Instalación (fijo)
    - Margen de ganancia (30%)

    Args:
        width_cm: Ancho en centímetros
        height_cm: Alto en centímetros
        color: Color del aluminio (natural, blanco, negro, champagne)
        glass_type: Tipo de cristal (6mm, 8mm, 9mm)

    Returns:
        dict con breakdown del precio
    """
    # Precios base (configurables)
    aluminum_price_per_m2 = {
        "natural": 450,
        "blanco": 520,
        "negro": 580,
        "champagne": 550
    }

    glass_price_per_m2 = {
        "6mm": 350,
        "8mm": 420,
        "9mm": 480
    }

    # Normalizar color y tipo de cristal
    color = color.lower()
    glass_type = glass_type.lower()

    # Usar valores por defecto si no existen
    aluminum_price = aluminum_price_per_m2.get(color, 450)
    glass_price = glass_price_per_m2.get(glass_type, 480)

    # Cálculos
    area_m2 = (width_cm * height_cm) / 10000
    aluminum_cost = area_m2 * aluminum_price
    glass_cost = area_m2 * glass_price
    hardware_cost = 850  # Promedio herrajes
    installation_cost = 1200  # Instalación fija

    subtotal = aluminum_cost + glass_cost + hardware_cost + installation_cost

    # Margen de ganancia (30%)
    final_price = subtotal * 1.3

    return {
        "product": "cancel_bano",
        "dimensions": {"width_cm": width_cm, "height_cm": height_cm},
        "materials": {
            "color": color,
            "glass_type": glass_type
        },
        "breakdown": {
            "aluminum_cost": round(aluminum_cost, 2),
            "glass_cost": round(glass_cost, 2),
            "hardware_cost": hardware_cost,
            "installation_cost": installation_cost,
            "subtotal": round(subtotal, 2),
            "margin_percentage": 30,
            "margin_amount": round(subtotal * 0.3, 2)
        },
        "total_mxn": round(final_price, 2),
        "area_m2": round(area_m2, 2)
    }


def parse_dimensions(text: str) -> dict:
    """
    Extrae dimensiones del texto usando regex (gratuito, sin OpenAI).

    Busca patrones como "150x190", "150 x 190", "150X190"

    Args:
        text: Texto del usuario

    Returns:
        dict con {width, height} o None si no encuentra
    """
    import re

    # Buscar patrón de dimensiones
    match = re.search(r'(\d+)\s*[\*xX]\s*(\d+)', text)

    if match:
        width = int(match.group(1))
        height = int(match.group(2))

        # Validar rangos razonables
        if 50 <= width <= 300 and 50 <= height <= 300:
            return {"width_cm": width, "height_cm": height}

    return None


def extract_product_type(text: str) -> str:
    """
    Identifica tipo de producto del texto.

    Returns:
        "cancel", "ventana", "barandal" o "unknown"
    """
    text_lower = text.lower()

    if "cancel" in text_lower or "baño" in text_lower:
        return "cancel"
    elif "ventana" in text_lower or "window" in text_lower:
        return "ventana"
    elif "barandal" in text_lower or "railing" in text_lower:
        return "barandal"
    else:
        return "unknown"


def extract_color(text: str) -> str:
    """
    Extrae color del texto.

    Returns:
        Color encontrado o "natural" por defecto
    """
    text_lower = text.lower()

    colors = {
        "negro": "negro",
        "black": "negro",
        "blanco": "blanco",
        "white": "blanco",
        "natural": "natural",
        "champagne": "champagne"
    }

    for color_key, color_value in colors.items():
        if color_key in text_lower:
            return color_value

    return "natural"  # Por defecto
