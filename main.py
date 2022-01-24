from selenium import webdriver
import time
import pandas as pd

### IF POR SI NO SE COMPLETAN LOS DATOS DE ENRUTAMIENTO ###
# Completar las variables "path_series" y "path_pelis" con la ruta donde se guardan los CSV# - sino se ejecuta default
# Ejemplo: 'C:\Users\Mariano\Desktop\BBVision\dataseries.csv' / 'C:\Users\Mariano\Desktop\BBVision\datapelis.csv'
path_series = r''
path_pelis = r''

# Completar la variable "executable_path" con la ruta donde tenemos Geckodriver# - sino se ejecuta default
# Ejemlo 'C:\Users\Mariano\Desktop\BBVision\geckodriver.exe'
executable_path = r''

if path_series == '':
    path_series = 'dataseries.csv'
if path_pelis == '':
    path_pelis = 'datapelis.csv'
if executable_path == '':
    browser = webdriver.Firefox()
else:
    browser = webdriver.Firefox(executable_path = executable_path)
### FIN IF POR SI NO SE COMPLETAN LOS DATOS DE ENRUTAMIENTO ###

pelis_data = [] # Lista de diccionarios para el CSV
linkP = "https://www.starz.com/ar/es/view-all/blocks/1523534"
browser.get(linkP)
time.sleep(5) # Tiempo de carga a la web
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll sobre la página para cargar cada película
time.sleep(5) # Tiempo de carga al scroll


# PELIS SCRAP #

# COMIENZA RECORRIDO AL GRID DE PELÍCULAS #
pelisCont = browser.find_element_by_tag_name("virtual-scroller") # Grid de todas las películas
pelisInd = pelisCont.find_elements_by_class_name("content-title") # Contenido individual de cada película
listaP = [] # Lista de películas (links append)


for pelicula in pelisInd: # COMIENZA APPEND #
    href = pelicula.find_element_by_tag_name("a").get_attribute("href")
    if href not in listaP: # if para que no se repitan elementos
        listaP.append(href)
# FIN DEL APPEND A LA LISTA DE LAS PELICULAS #


# COMIENZA RECORRIDO INDIVIDUAL DE CADA PELÍCULA
for direccionP in listaP: # Recorrido individual de cada link
    browser.get(direccionP)
    time.sleep(3) # Tiempo de carga de cada película


    try: # Se bajaba mal la información de la sinopsis ya que había un botón de "Ver Más"
        browser.find_element_by_class_name("more-link").click() # Click botón "Ver más"
    except:
        pass


    nombreP = browser.find_element_by_class_name("movie-title").text.replace('Ver ', '').replace(' online', '')
    sinopsisP = browser.find_element_by_class_name("logline").find_element_by_tag_name("p").text.strip()
    añoP = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-movie-details/div/div/section/div[1]/div[2]/section/ul/li[4]').text.strip()
    duracionP = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-movie-details/div/div/section/div[1]/div[2]/section/ul/li[2]').text.strip()
    generoP = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-movie-details/div/div/section/div[1]/div[2]/section/ul/li[3]').text.strip()
    aptoP = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-movie-details/div/div/section/div[1]/div[2]/section/ul/li[1]').text.strip()
    sonoraP = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-movie-details/div/div/section/div[1]/div[2]/section/ul/li[5]').text.strip()


    pelis_data.append({"Nombre": nombreP, # Append a pelis_data para luego pasarlo a CSV
    "Sinopsis": sinopsisP,
    "Año": añoP,
    "Duración": duracionP,
    "Género": generoP,
    "Apto":aptoP,
    "Sonido": sonoraP})
    print(nombreP) # Print para ubicar errores

# FIN DEL SCRAP A LAS PELÍCULAS #



# SERIES SCRAP #

series_data = [] # Lista de diccionarios para el CSV
linkS = "https://www.starz.com/ar/es/view-all/blocks/1523514"
browser.get(linkS)
time.sleep(5) # Tiempo de carga a la web
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll sobre la página para cargar cada serie
time.sleep(5) # Tiempo de carga al scroll


# COMIENZA RECORRIDO AL GRID DE SERIES #
seriesCont = browser.find_element_by_tag_name("virtual-scroller") # Grid de todas las series
seriesInd = seriesCont.find_elements_by_class_name("content-title") # Contenido individual de cada serie
listaS = [] # Lista de series (links append)


for serie in seriesInd: # COMIENZA APPEND #
    href = serie.find_element_by_tag_name("a").get_attribute("href")
    if href not in listaS: # if para que no se repitan elementos
        listaS.append(href)
# FIN DEL APPEND A LA LISTA DE LAS SERIES #


# COMIENZA RECORRIDO INDIVIDUAL DE CADA CAPÍTULO
for direccionS in listaS: # Recorrido individual de cada link
    browser.get(direccionS)
    time.sleep(3) # Tiempo de carga de cada serie


    try: # Se bajaba mal la información de la sinopsis ya que había un botón de "Ver Más"
        browser.find_element_by_class_name("overlay").find_element_by_class_name("more-button").click() # Click botón "Ver más"
    except:
        pass


    nombreS = browser.find_element_by_id("seriesDetailsH1").text.strip()
    print(nombreS)
    sinopsisS = browser.find_element_by_class_name("logline").find_element_by_tag_name("p").text.strip()
    añoS = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-series-details/div[1]/section/div[1]/div[2]/ul/li[4]').text.strip()
    episodiosS = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-series-details/div[1]/section/div[1]/div[2]/ul/li[2]').text.strip()
    generoS = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-series-details/div[1]/section/div[1]/div[2]/ul/li[3]').text.strip()
    aptoS = browser.find_element_by_class_name("meta-list").find_element_by_xpath('//*[@id="subview-container"]/starz-series-details/div[1]/section/div[1]/div[2]/ul/li[1]').text.strip()


    tempCont =  browser.find_elements_by_class_name("season-number") # Container de temporadas para continuar con los episodios
    tempNum = [temp.find_element_by_tag_name("a").get_attribute('href') for temp in tempCont] # Lista de temporadas (href)
    for temp in tempNum: # ITERA LA LISTA DE TEMPORADAS #
        browser.get(temp)
        time.sleep(3)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll sobre las temporadas para cargar correctamente
        time.sleep(1) # Time por posible error


        episodiosInd = browser.find_elements_by_class_name("episode-container") # Contenido individual de cada episodio
        for episodio in episodiosInd: # Recorrido de cada capítulo

            try:
                episodio.find_element_by_class_name("episode-link").click() # Click a episodio para obtener sus datos (debido a overlay)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll sobre las temporadas para cargar correctamente
                time.sleep(2) # Time por posible error
            except:
                pass


            try: # Se bajaba mal la información de la sinopsis ya que había un botón de "Ver Más"
                vermas = browser.find_element_by_class_name("more-link").click() # Click botón "Ver más"
                time.sleep(2)
            except:
                pass


            nombreEp = browser.find_element_by_class_name("episode-title").text.strip()
            print(nombreEp) # Print para ubicar errores
            sinopsisEp = browser.find_element_by_class_name("logline").find_element_by_tag_name("p").text.strip()
            duracionEp = browser.find_element_by_class_name("meta-list").find_element_by_xpath('/html/body/starz-root/starz-base-modal/div/div/div/div[2]/starz-episode-details-modal/div/section/div/div[1]/div[2]/ul/li[2]').text.strip()
            añoEp = browser.find_element_by_class_name("meta-list").find_element_by_xpath('/html/body/starz-root/starz-base-modal/div/div/div/div[2]/starz-episode-details-modal/div/section/div/div[1]/div[2]/ul/li[3]').text.strip()
            sonoraEp = browser.find_element_by_class_name("meta-list").find_element_by_xpath('/html/body/starz-root/starz-base-modal/div/div/div/div[2]/starz-episode-details-modal/div/section/div/div[1]/div[2]/ul/li[4]').text.strip()


            browser.find_element_by_class_name("close-button").click() # Click al close de cada capítulo (debido a overlay)
            time.sleep(2) # Time por posible error


            series_data.append({"Nombre": nombreS, # Append a series_data para luego pasarlo a CSV
            "Sinopsis": sinopsisS,
            "Año": añoS,
            "Cantidad de episodios": episodiosS,
            "Género": generoS,
            "Apto":aptoS,
            "Nombre del Episodio": nombreEp,
            "Duración": duracionEp,
            "Sinopsis del episodio": sinopsisEp,
            "Año del episodio": añoEp,
            "Sonido": sonoraEp})

# FIN DEL SCRAP A CADA EPISODIO #

browser.close()

pelis_data = pd.DataFrame(pelis_data) # Lectura de lista con Pandas
pelis_data.to_csv(path_pelis, columns=["Nombre", "Sinopsis", "Año", "Duración", "Género", "Apto", "Sonido"],encoding='utf8', index= False) # Guardo la estructura de datos en un CSV

series_data = pd.DataFrame(series_data) # Lectura de lista con Pandas
series_data.to_csv(path_series, columns=["Nombre", "Sinopsis", "Año", "Cantidad de episodios", "Género", "Apto", "Nombre del Episodio", "Duración", "Sinopsis del episodio", "Año del episodio", "Sonido"],encoding='utf8', index= False) # Guardo la estructura de datos en un CSV