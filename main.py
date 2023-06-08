from neo4j import GraphDatabase
from Algoritmos import Algoritmo
from Usuario import Usuario
from UsuarioAux import UsuarioAux 
from Grupo import Grupo
from Restaurante import Restaurante
from RestauranteAux import RestauranteAux


#Conexion a la base de datos
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "12345678"))
session = driver.session()

ciudades = ['Abington', 'Abington Township', 'Affton', 'Aldan', 'Algiers', 'Alloway', 'Alton', 'Ambler', 'Antioch', 'Apollo Beach', 'Arabi', 'Ardmore', 'Arnold', 'Ashland', 'Ashland City', 'Aston', 'Atco',  'Audubon', 'Audubon ', 'Avon', 'Avondale', 'BOISE', 'BRANDON', 'Bala Cynwyd', 'Ballwin', 'Balm', 'Bargersville', 'Barrington', 'Bayonet Point', 'Beaumont', 'Beech Grove', 'Bel Ridge', 'Belle Chase', 'Belle Chasse', 'Belle Meade', 'Belleair Blf', 'Belleair Bluffs', 'Bellefontaine', 'Bellefontaine Neighbors', 'Belleville', 'Bellevue', 'Bellmawr', 'Bellville', 'Belmont Hills', 'Bensalem', 'Bensalem Township', 'Bensalem. Pa', 'Berkeley', 'Berlin', 'Berlin Township', 'Berry Hill', 'Berwyn', 'Bethalto', 'Bethel', 'Bethel Township', 'Beverly', 'Birchrunville', 'Black Jack', 'Blackwood', 'Blackwood ', 'Blooming Glen', 'Blue Bell', 'Blvd', 'Boise', 'Boise City', 'Boone', 'Boothwyn', 'Bordentown', 'Boyertown', 'Brandon', 'Breckenridge Hills', 'Brentwood', 'Bridge City', 'Bridgeport', 'Bridgeton', 'Bristol', 'Bristol Twp', 'Brookhaven', 'Brooklawn', 'Broomall', 'Brownsburg', 'Bryn Athyn', 'Bryn Mawr', 'Buckingham', 'Bucks', 'Bucktown', 'Burlington', 'Burlington Township', 'Bywater', 'CLEARWATER', 'CLIFTON HEIGHTS', 'Cahokia', 'Caln', 'Camby', 'Camden', 'Cane Ridge', 'Carmel', "Carney's Point", 'Carneys Point', 'Carpinteria', 'Carrollwood', 'Carversville', 'Casas Adobes', 'Caseyville', 'Castleton', 'Catalina', 'Cedar Brook', 'Cedarbrook', 'Cedars', 'Center Square', 'Chadds Ford', 'Chalemette', 'Chalfont', 'Chalmette', 'Charlotte', 'Cheltenham', 'Cheltenham Township', 'Cherry Hill', 'Chesilhurst', 'Chester', 'Chester Springs', 'Chesterbrook', 'Chesterfield', 'Chichester', 'Christiana', 'Churchville', 'Cinnaminson', 'Citrus Park', 'Clarksboro', 'Clarksville', 'Claymont', 'Clayton', 'Clearwater', 'Clearwater Beach', 'Clearwater/ Countryside', 'Clementon', 'Clermont', 'Clifton Heights', 'Coatesville', 'Cold Springs', 'Collegeville', 'Collingdale', 'Collingswood', 'Collinsville', 'Colmar', 'Columbia', 'Columbus', 'Concord Township', 'Concordville', 'Conshohocken', 'Conshohoeken', 'Cornwells Heights', 'Corona De Tucson', 'Corona de Tucson', 'Cottage Hills', 'Crestwood', 'Creve Coeur', 'Croydon', 'Crum Lynne', 'Cumberland', 'DELRAN', 'DONELSON', 'Dade City', 'Danville', 'Darby', 'Delanco', 'Dellwood', 'Delran', 'Delran Township', 'Delran Twp', 'Deptford', 'Deptford Township', 'Des Peres', 'Devon', 'Dover', 'Downingtown', 'Downtown', 'Doylestown', 'Dresher', 'Drexel Heights', 'Drexel Hill', 'Dublin', 'Dunedin', 'Dupo', 'E. Norristown', 'Eagle', 'Eagleville', 'Earth City', 'East Alton', 'East Edmonton', 'East Falls', 'East Greenville', 'East Lansdowne', 'East Nashville', 'East Norriton', 'East Saint Louis', 'East St Louis', 'East St. Louis', 'Eastampton', 'Eastampton Township', 'Eaux Claires', 'EdMonton', 'Eddington', 'Eddystone', 'Edgemont', 'Edgewater Park', 'Edmonton', 'Edwardsville', 'Elk Township', 'Elkins Park', 'Elmer', 'Elmwood', 'Elsmere', 'Elverson', 'Enoch', 'Erdenheim', 'Erial', 'Essington', 'Evesham', 'Evesham Township', 'Ewing', 'Ewing Township', 'Exton', 'Fairless Hills', 'Fairmont City', 'Fairview', 'Fairview Heights', 'Fairview Hts', 'Fairview Hts.', 'Fairview Village', 'Feasterville', 'Feasterville Trevose', 'Feasterville-Trevose', 'Feasterville-trevose', 'Fenton', 'Ferguson', 'Festerville', 'Fieldsboro', 'Fishers', 'Flanders', 'Florence', 'Florence Township', 'Florissant', 'Flourtown', 'Folcroft', 'Folsom', 'Fort Washington', 'Fortville', 'Foster Pond', 'Fox Street', 'Franconia', 'Franklin', 'Franklinville', 'Frazer', 'Freeburg', 'Freehold', 'Frontenac', 'Furlong', 'Gallatin', 'Garden City', 'Gardenville', 'Garnet Valley', 'Gentilly', 'Gibbsboro', 'Gibbstown', 'Gibsonton', 'Gilbertsville', 'Gladwyne', 'Glassboro', 'Glen Carbon', 'Glen Mills', 'Glendale', 'Glendora', 'Glenmoore', 'Glenoldan', 'Glenolden', 'Glenside', 'Gloucester', 'Gloucester City', 'Gloucester Township', 'Godfrey', 'Goleta', 'Goodletsville', 'Goodlettsville', 'Granite City', 'Greater Northdale', 'Green Lane', 'Green Park', 'Green Valley', 'Greenbrier', 'Greenfield', 'Greenville', 'Greenwood', 'Gretna', 'Gulfport', 'Gulph Mills', 'Gwynedd', 'Gwynedd Valley', 'HUdson', 'Haddon Heights', 'Haddon Township', 'Haddon Twp', 'Haddonfield', 'Hainesport', 'Hamiltion', 'Hamilton', 'Hamilton Township', 'Hammonton', 'Hancock', 'Harahan', 'Harleysville', 'Harrison Township', 'Harvey', 'Hatboro', 'Hatfield', 'Haverford', 'Havertown', 'Hazelwood', 'Hendersonville', 'Hermitage', 'Hernando Bch', 'Hernando Beach', 'Hi-Nella', 'High Ridge', 'Hillsborough County', 'Hilltop', 'Hilltown', 'Hockessin', 'Holicong', 'Holiday', 'Holland', 'Holland Southampton', 'Hollywood', 'Holmes', 'Horsham', 'Hudson', 'Hulmeville', 'Huntingdon Valley', 'Hurffville', 'INpolis', 'Imperial', 'Indian Rocks Beach', 'Indian Shores', 'Indiana', 'Indianapolis', 'Indianapolis ', 'Inglewood', 'Isla Vista', 'Ivyland', 'Jamison', 'Jefferson', 'Jeffersonville', 'Jenkintown', 'Jennings', 'Jobstown', 'Joelton', 'Kalispell', 'Kenner', 'Kenneth', 'Kenneth City', 'Kennett Square', 'Kimberton', 'Kimmswick', 'King Of Prussia', 'King of Prussia', 'Kingston Springs', 'Kirklyn', 'Kirkwood', 'Kulpsville', 'Kuna', 'LANGHORNE', 'LANSDALE', 'LARGO', 'LITHIA', 'LOWER MERION', 'LOWER PROVIDENCE', 'La Vergne', 'Ladue', 'Lafayette Hill', 'Lahaska', 'Lambertville', 'Land O Lakes', "Land O' Lakes", "Land O'Lakes", "Land O'lakes", 'Land o Lakes', 'Land o lakes', 'Langhorne', 'Lansdale', 'Lansdale ', 'Lansdowne', 'Largo', 'Largo (Walsingham)', 'Laurel Springs', 'Lawnside', 'Lawrence', 'Lawrence Township', 'Lawrenceville', 'Lebanon', 'Lederach', 'Lemay', 'Lester', 'Levittown', 'Lima', 'Limerick', 'Lindenwold', 'Line Lexington', 'Linfield', 'Linwood', 'Lionville', 'Lithia', 'Liverpool', 'Logan Township', 'London Grove', 'Lower Southampton Township', 'Lula Lula', 'Luling', 'Lumberton', 'Lutz', 'Lutz fl', 'MADISON', 'MEDIA', 'Madeira Beach', 'Madison', 'Magnolia', 'Malaga', 'Malvern', 'Manayunk', 'Manchester', 'Mango', 'Mansfield', 'Mantua', 'Mantua Township', 'Maple Glen', 'Maple Shade', 'Maple Shade Township', 'Maplewood', 'Marana', 'Marcus Hook', 'Marlborough', 'Marlton', 'Marrero', 'Marshallton', 'Martinsville', 'Maryland Heights', 'Maryville', 'Masaryktown', 'Mascoutah', 'Mc Cordsville', 'McCordsville', 'Mccordsville', 'Medford', 'Medford Lakes', 'Media', 'Mehlville', 'Melrose Park', 'Mendenhall', 'Meraux', 'Mercerville', 'Merchantville', 'Meridian', 'Meridian ', 'Merion Station', 'Metairie', 'Metarie', 'Middletown', 'Millstadt', 'Milmont Park', 'Monroe Township', 'Monroeville', 'Mont Clare', 'Montchanin', 'Montecito', 'Montgomery', 'Montgomeryville', 'Moorestown', 'Moorestown-Lenola', 'Mooresville', 'Morrisville', 'Morton', 'Mount Ephraim', 'Mount Holly', 'Mount Holly,', 'Mount Juliet', 'Mount Laurel', 'Mount Laurel Township', 'Mount Lemmon', 'Mount Royal', 'Mt Holly', 'Mt Juliet', 'Mt Laurel', 'Mt Laurel Twp, NJ', 'Mt. Holly', 'Mt. Juliet', 'Mt. Laurel', 'Mt.Juliet', 'Mt.Laurel', 'Mullica Hill', 'N Redngtn Bch', 'N.Wales', 'NASHVILLE', 'NEW ORLEANS', 'NEW PORT RICHEY', 'NORRISTOWN', 'NORTH WALES', 'NW Edmonton', 'Nampa', 'Narberth', 'Nashville', 'Nashville ', 'Nashville-Davidson metropolitan government (balance)', 'National Park', 'New Britain', 'New Castle', 'New Hope', 'New Orleans', 'New Palestine', 'New Port Richey', 'New Whiteland', 'Newark', 'Newfield', 'Newport', 'Newportville', 'Newton', 'Newtown', 'Newtown Sqaure', 'Newtown Square', 'Noblesville', 'Nolensville', 'Normandy', 'Norristown', 'North Coventry Township', 'North Redington Bch', 'North Redington Beach', 'North Wales', 'Norwood', 'O Fallon', "O' Fallon", "O'Fallon", "O'fallon", 'Oaklyn', 'Oaks', 'Oakville', 'Odessa', 'Old Hickory', 'Oldmans Township', 'Oldsmar', 'Olivette', 'Oreland', 'Oro Valley', 'Overland', 'Ozona', 'PHILA', 'PINELLAS PARK', 'POTTSTOWN', 'Palm Harbor', 'Palm harbor', 'Palmetto', 'Palmyra', 'Paoli', 'Parkside', 'Pass-a-Grille Beach', 'Paulsboro', 'Peerless Park', 'Pemberton', 'Penndel', 'Pennington', 'Penns Grove', 'Pennsauken', 'Pennsauken Township', 'Pennsburg', 'Pennsville', 'Pennsville Township', 'Pennsylvania', 'Perkasie', 'Perkiomenville', 'Phila', 'Philadelphia', 'Philadelphia ', 'Philadephia', 'Philly', 'Phoenixville', 'Picture Rocks', 'Pike Creek', 'Pilesgrove', 'Pine Forge', 'Pine HIll', 'Pine Hill', 'Pinecrest West Park', 'Pinellas', 'Pinellas Park', 'Pinellas park', 'Pineville', 'Pipersville', 'Pitman', 'Pittsgrove', 'Pittsgrove Township', 'Plainfield', 'Plainfiled', 'Plant City', 'Pleasant Township', 'Pleasant View', 'Plumsteadville', 'Plymouth Meeting', 'Pontoon Beach', 'Port Richey', 'Pottstown', 'Primos', 'Prospect Park', 'Quakertown', 'Quinton', 'RADNOR', 'RENO', 'RIVERVIEW', 'Radnor', 'Red Hill', 'Redingtn Shor', 'Redington Shore', 'Redington Shores', 'Reno', 'Richboro', 'Richmond Heights', 'Ridley', 'Ridley Park', 'River Ridge', 'Riveridge', 'Riverside', 'Riverton', 'Riverview', 'Riverview Fl', 'Rock Hill', 'Rockledge', 'Roebling', 'Rosemont', 'Rosewood Heights', 'Roslyn', 'Royersford', 'Royersford ', 'Runnemede', 'Rural Hill', 'Ruskin', 'S.Pasadena', 'SPRINGHILL', 'ST LOUIS', 'ST. Louis', 'ST. PETE BEACH', 'ST. PETERSBURG', 'Safety Harbor', 'Sahuarita', 'Saint Albert', 'Saint Ann', 'Saint Bernard', 'Saint Charles', 'Saint John', 'Saint Leo', 'Saint Louis', 'Saint Louis,', 'Saint Pete Beach', 'Saint Peters', 'Saint Petersburg', 'Saint Petersburg Beach', 'Saint Rose', 'Saintt Petersburg', 'Salem', 'San Antonio', 'Sanatoga', 'Santa  Barbara', 'Santa Barbara', 'Sappington', 'Sassamansville', 'Sauget', 'Schwenksville', 'Scott AFB', 'Scott Afb', 'Scott Air Force Base', 'Secane', 'Seffner', 'Sellersville', 'Seminole', 'Sewell', 'Shamong', 'Sharon Hill', 'Sherwood', 'Sherwood Park', 'Shiloh', 'Shrewsbury', 'Sicklerville', 'Silverdale', 'Skippack', 'Skippack Village', 'Smithton', 'Smyrna', 'Solebury', 'Somerdale', 'Souderton', 'South Cinnaminson', 'South Pasadena', 'South Tampa', 'South Tucson', 'Southampton', 'Southampton Township', 'Southeast Edmonton', 'Southport', 'Southwest Philadelphia', 'Southwest Tampa', 'Spanish Springs', 'Sparks', 'Speedway', 'Spring City', 'Spring Hill', 'Spring House', 'Springfield', 'St Albert', 'St Ann', 'St Charles', 'St Louis', 'St Louis County', 'St Louis Downtown', 'St Pete', 'St Pete Beach', 'St Petersburg', 'St Petersurg', 'St.  Charles', 'St. Albert', 'St. Ann', 'St. Charles', 'St. Davids', 'St. Leo', 'St. Louis', 'St. Louis County', 'St. Pete Beach', 'St. Peters', 'St. Petersburg', 'St. Rose', 'St.Ann', 'St.Charles', 'St.Louis', 'St.Petersburg', 'St.Rose', 'Stanton', 'Stead', 'Stowe', 'Stratford', 'Sullivan', 'Summerland', 'Sumneytown', 'Sun City', 'Sun City Center', 'Sun Valley', 'Sunset Hills', 'Swansea', 'Swarthmore', 'Swedeland', 'Swedesboro', 'TAMPA', 'TEMPLE TERR', 'TRENTON', 'TRINITY', 'TUCSON', 'Tabernacle', 'Talleyville', 'Tampa', 'Tampa Bay', 'Tampa Florida', 'Tampa Palms', 'Tampa,Fl', 'Tarpon Springs', 'Tarpon springs', 'Telford', 'Telford ', 'Temple Terr', 'Temple Terrace', 'Terrytown', 'Thonosassa', 'Thonotosassa', 'Thorndale', 'Thornton', 'Thorofare', 'Tierra Verde', 'Tierre Verde', 'Tinicum', 'Titusville', 'Toughkenamon', 'Town & Country', "Town 'N' Country", "Town 'n' Country", 'Town And Country', 'Town and Country', 'Town and Country ', 'Town n Country', 'Trainer', 'Trappe', 'Treasure Island', 'Tren', 'Trenton', 'Trevose', 'Trinity', 'Trolley Square', 'Trooper', 'Troy', 'Truckee', 'Tucson', 'Turnersville', 'Tuscon', 'Twin Oaks', 'Twn N Cntry', 'Tylersport', 'UPPER MORELAND', 'Unionville', 'University City', 'Upland', 'Upper Chichester', 'Upper Darby', 'Upper Gwynedd', 'Upper Pittsgrove', 'Upper Pottsgrove', 'Upper Southampton', 'Vail', 'Valencia West', 'Valley Park', 'Valrico', 'Verdi', 'View', 'Villanova', 'Vincentown', 'Vineland', 'Violet', 'Virginia City', 'Voorhees', 'Voorhees Township', 'W Cherry Hill', 'W. Berlin', 'W.Chester', 'WEST CHESTER', 'WILLOW GROVE', 'Wallingford', 'Wanamaker', 'Warminster', 'Warrington', 'Warrington Township', 'Warson Woods', 'Washington Crossing', 'Washington Park', 'Washington Township', 'Washington Twp', 'Waterford Works', 'Waterloo', 'Wayne', 'Webster Groves', 'Wenonah', 'Wesley Chapel', 'Wesley chapel', 'West Berlin', 'West Bradford Township', 'West Chester', 'West Chester PA', 'West Collingswood Heights', 'West Conshohocken', 'West Deptford', 'West Deptford Townsh', 'West Edmonton', 'West Mount Holly', 'West Point', 'West Trenton', 'Westampton', 'Westampton Township', 'Westchase', 'Westhampton', 'Westmont', 'Westmont - Haddon Towsship', 'Westtown', 'Westville', 'Westwego', 'White House', 'Whiteland', 'Whites Creek', 'Whitestown', 'Williamstown', 'Willingboro', 'Willingboro Township', 'Willow Grove', 'Wilmington', 'Wilmington ', 'Wilmington Manor', 'Wimauma', 'Winchester', 'Winslow Township', 'Wood River', 'Woodbury', 'Woodbury Heights', 'Woodbury Hts.', 'Woodlyn', 'Woodson Terrace', 'Woodstown', 'Woolwich Township', 'Woolwich Twp', 'Woolwich Twp.', 'Worcester', 'Wrightstown', 'Wycombe', 'Wyncote', 'Wyndlake Condominium', 'Wyndmoor', 'Wynnewood', 'Yardley', 'Yeadon', 'Zephyrhills', 'Zieglerville', 'Zionsville']

#Funciones

def nombreAmigos():
    if(len(user.friends) > 0):
        nombres = []
        for amigo in user.friends:
            useraux = UsuarioAux(amigo, session)
            print(useraux.name)
            nombres.append(useraux.name)
    else:
        print("No tienes amigos")
    return nombres

def buscarUsuarios(lista):
    listaUsers = []
    for u in lista:
        contador = 0
        encontrado = False
        while (encontrado == False):
            if(u == user.listaUsuarios[contador].name):
                listaUsers.append(user.listaUsuarios[contador])
                encontrado = True
            else:
                contador += 1
    return listaUsers
        

def SeleccionarAmigos():
    amigosSeleccionados = []
    print("Selecciona a los amigos: ")
    nombres = nombreAmigos()
    if(len(user.friends) > 0):
        todosAmigos = False
        print ("Introduce el id de los usuarios(Fin = Ya): ")
        while(todosAmigos == False):
            amigoSeleccionado = input()
            if(amigoSeleccionado != "Ya"):
                if(nombres.count(amigoSeleccionado)>0):
                    amigosSeleccionados.append(amigoSeleccionado)
            else:
                todosAmigos = True
    return amigosSeleccionados
    #Hacer el seleccionador de amigos
    """
    Obtener los amigos de la lista de amigos del usuario
    Imprimirlos todos
    Elegirlos
        - Introducirlos por input()
            - Comprobar que los introducidos estén en la lista
        - Hacer el seleccionador cuando sepa hacerlo con la vista
    """



def SeleccionarCiudad():
    repetir = True
    while(repetir):
        print("Elige la ciudad en la que quieras que esté el restaurante: ")
        print (ciudades)
        ciudad = input()
        if (ciudades.count(ciudad)>0):
            repetir = False
        else:
            print("La ciudad introducida es erronea")
    return ciudad

def repetirRecomendacion():
    valida = False
    while(valida == False):
        print("Recomendar de nuevo S/N")
        respuesta = input()
        if(respuesta == 'S'): 
            elegir = True
            valida = True
        elif (respuesta == 'N'):
            elegir = False
            valida = True
    return elegir

def perteneceUsuario(grupo, usuario):
    pertenece = False
    i = 0
    while ((pertenece == False) and i < len(grupo)):
        if(grupo[i].user_id == usuario):
            pertenece = True
        i += 1
    return pertenece

def perteneceRestaurante(lista, restaurante):
    pertenece = False
    i = 0
    while(i<len(lista) and pertenece==False):
        if(lista[i].restaurante_id == restaurante.restaurante_id):
            pertenece = True
        i += 1
    return pertenece


#Programa
#Introducir el id
idCorrecto = False
while(idCorrecto == False):
    print("Introduce tu userId: ")
    #idUsuario = input()                                            #####################################
    idUsuario = 'Q3Y0AjsTpuJuQ-TWZOlVzg'
    print(idUsuario)
    user = Usuario(idUsuario, session)
    if(user.existeUsuario() == False):
        print("El id introducido es erroneo")
    else:
        idCorrecto = True
#Elegir amigos
elegir = True
algoritmo = Algoritmo()
while (elegir == True):   
    #Selecciona los amigos a los que hacer la recomendación
    seleccionados=[]
    while(len(seleccionados)==0 and len(user.friends)>0):
        #seleccionados = SeleccionarAmigos()                        #####################################
        seleccionados = ["Justin", "Mike"]
    listaGrupo = buscarUsuarios(seleccionados)
    listaGrupo.append(user)
    #Seleccionar el estado
    ciudad = ""
    while (len(ciudad)==0): 
        #ciudad = SeleccionarCiudad()                                      #####################################
        ciudad = "Zionsville"
    #Hacer el seleccionador de ciudad

    print("Amigos seleccionados: ")
    for s in seleccionados:
        print(" - ", s)
    print("Ciudad seleccionada:", ciudad)

    #Generar recomendación

    #Crear grupo
    grupo = Grupo(listaGrupo, session)
    
    mejoresRestaurantes =[]

    for i in grupo.listaFinal:
        r = Restaurante(i.restaurante_id, session)
        mejoresRestaurantes.append(r)
    

    usuariosAfines = []

    for i in mejoresRestaurantes:
        for j in i.listaUsuarios:
            if(perteneceUsuario(grupo.listaUsuarios, j.user_id)==False):
                usuariosAfines.append(j)

    #######################
    ########JACCARD########
    #######################

    listaJaccard = []
    listaJaccardFinal = []

    for i in usuariosAfines:
        listaJaccard.append(algoritmo.jaccard(grupo, i))

    valMaxJaccard = max(listaJaccard)
    
    n = 0
    for i in listaJaccard:
        if (i == valMaxJaccard):
            listaJaccardFinal.append(usuariosAfines[n])
        n += 1


    #######################
    #######SIMILITUD#######
    #######################

    similitudes = []
    listaSimilitudesFinal = []

    for i in listaJaccardFinal:
        similitudes.append(algoritmo.similitud(grupo, i))
    
    valMaxSimilitudes = max(similitudes)

    ########################
    #######PREDICCION#######
    ########################

    listaRestaurantes = []
    listaValoraciones = []
    n = 0

    for i in listaJaccardFinal:
        for j in i.listaReviewsInicializadas:
            restaurante = RestauranteAux(j.restaurante_id, session)
            listaRestaurantes.append(restaurante)
            listaValoraciones.append(algoritmo.prediccion(grupo, i, restaurante, similitudes[n]))
        n += 1

    listaRestaurantesFinales = []
    listaValoracionesFinales = []
    n = 0

    for i in listaRestaurantes:
        if (perteneceRestaurante(listaRestaurantesFinales, i) == False):
            if(i.ciudad == ciudad):
                listaRestaurantesFinales.append(i)
                listaValoracionesFinales.append(listaValoraciones[n])
        n += 1

    n = 0
    for i in listaRestaurantesFinales:
        print(i.name, ": ", listaValoracionesFinales[n])
        n += 1

    elegir = False
    #elegir = repetirRecomendacion()                            #####################################
    

session.close()
