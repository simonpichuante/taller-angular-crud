"""Catálogo territorial de Chile según la DPA 2020 del INE."""

# Fuente: INE, Anuario de Estadísticas Vitales 2018, anexo DPA 2020.
# https://www.ine.gob.cl/docs/default-source/nacimientos-matrimonios-y-defunciones/publicaciones-y-anuarios/anuarios-de-estad%C3%ADsticas-vitales/anuario-de-estad%C3%ADsticas-vitales-2018.pdf

# Cada región conserva el ID usado por el proyecto. Los IDs de provincias y
# comunas se asignan desde la base para mantener las relaciones existentes.
TERRITORIO_DPA = {
    1: (
        ("Iquique", ("Iquique", "Alto Hospicio")),
        ("Tamarugal", ("Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica")),
    ),
    2: (
        ("Antofagasta", ("Antofagasta", "Mejillones", "Sierra Gorda", "Taltal")),
        ("El Loa", ("Calama", "Ollagüe", "San Pedro de Atacama")),
        ("Tocopilla", ("Tocopilla", "María Elena")),
    ),
    3: (
        ("Copiapó", ("Copiapó", "Caldera", "Tierra Amarilla")),
        ("Chañaral", ("Chañaral", "Diego de Almagro")),
        ("Huasco", ("Vallenar", "Alto del Carmen", "Freirina", "Huasco")),
    ),
    4: (
        ("Elqui", ("La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paihuano", "Vicuña")),
        ("Choapa", ("Illapel", "Canela", "Los Vilos", "Salamanca")),
        ("Limarí", ("Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado")),
    ),
    5: (
        ("Valparaíso", ("Valparaíso", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví", "Quintero", "Viña del Mar")),
        ("Isla de Pascua", ("Isla de Pascua",)),
        ("Los Andes", ("Los Andes", "Calle Larga", "Rinconada", "San Esteban")),
        ("Petorca", ("La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar")),
        ("Quillota", ("Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales")),
        ("San Antonio", ("San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo")),
        ("San Felipe de Aconcagua", ("San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María")),
        ("Marga Marga", ("Quilpué", "Limache", "Olmué", "Villa Alemana")),
    ),
    6: (
        ("Cachapoal", ("Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras", "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco", "Rengo", "Requínoa", "San Vicente")),
        ("Cardenal Caro", ("Pichilemu", "La Estrella", "Litueche", "Marchigüe", "Navidad", "Paredones")),
        ("Colchagua", ("San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo", "Placilla", "Pumanque", "Santa Cruz")),
    ),
    7: (
        ("Talca", ("Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael")),
        ("Cauquenes", ("Cauquenes", "Chanco", "Pelluhue")),
        ("Curicó", ("Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén")),
        ("Linares", ("Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas")),
    ),
    8: (
        ("Concepción", ("Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén")),
        ("Arauco", ("Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa")),
        ("Biobío", ("Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío")),
    ),
    9: (
        ("Cautín", ("Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol")),
        ("Malleco", ("Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria")),
    ),
    10: (
        ("Llanquihue", ("Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas")),
        ("Chiloé", ("Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao")),
        ("Osorno", ("Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo")),
        ("Palena", ("Chaitén", "Futaleufú", "Hualaihué", "Palena")),
    ),
    11: (
        ("Coyhaique", ("Coyhaique", "Lago Verde")),
        ("Aysén", ("Aysén", "Cisnes", "Guaitecas")),
        ("Capitán Prat", ("Cochrane", "O’Higgins", "Tortel")),
        ("General Carrera", ("Chile Chico", "Río Ibáñez")),
    ),
    12: (
        ("Magallanes", ("Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio")),
        ("Antártica Chilena", ("Cabo de Hornos", "Antártica")),
        ("Tierra del Fuego", ("Porvenir", "Primavera", "Timaukel")),
        ("Última Esperanza", ("Natales", "Torres del Paine")),
    ),
    13: (
        ("Santiago", ("Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura")),
        ("Cordillera", ("Puente Alto", "Pirque", "San José de Maipo")),
        ("Chacabuco", ("Colina", "Lampa", "Tiltil")),
        ("Maipo", ("San Bernardo", "Buín", "Calera de Tango", "Paine")),
        ("Melipilla", ("Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro")),
        ("Talagante", ("Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor")),
    ),
    14: (
        ("Valdivia", ("Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli")),
        ("Ranco", ("La Unión", "Futrono", "Lago Ranco", "Río Bueno")),
    ),
    15: (
        ("Arica", ("Arica", "Camarones")),
        ("Parinacota", ("Putre", "General Lagos")),
    ),
    16: (
        ("Diguillín", ("Chillán", "Bulnes", "Chillán Viejo", "El Carmen", "Pemuco", "Pinto", "Quillón", "San Ignacio", "Yungay")),
        ("Itata", ("Quirihue", "Cobquecura", "Coelemu", "Ninhue", "Portezuelo", "Ránquil", "Treguaco")),
        ("Punilla", ("San Carlos", "Coihueco", "Ñiquén", "San Fabián", "San Nicolás")),
    ),
}
