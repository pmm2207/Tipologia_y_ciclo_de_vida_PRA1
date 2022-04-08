# coding=ISO-8859-1
from bs4 import BeautifulSoup
import requests
import csv
import regex
import re
import time
import webtech
import whois
from urllib.request import urlopen

# Evaluación inicial
#############
# Tecnología utilizada por el sitio web
wt = webtech.WebTech(options={'json': True})

try:
    report = wt.start_from_url('http://www.conocetusfuentes.com')
    print(report['tech'])
except wt.utils.ConnectionException:
    print("Connection error")

# Propietario
w = whois.whois('http://www.conocetusfuentes.com')
print(w.org)
##############

# Extracción de la última página añadida
html = urlopen("http://www.conocetusfuentes.com/ultimas_fuentes.html")
bsObj = BeautifulSoup(html,"html.parser")
html_link = bsObj.find("div", {"class": "ultimas_fuentes"})

# Buscamos la url del último elemento y extraemos el id
try:
    for a in html_link.find_all('a', {'href': re.compile(r'datos_fuente.*[.html]$')}):
        ultimo_elemento = int(
            re.search(r'datos_fuente_(.*?).html', str(a)).group(1))
        print("Encontrada la URL del ultimo elemento:", a['href'])
except:
    print("No se ha encontrado la URL, asignamos un valor al id")
    ultimo_elemento = 13500

cabeceras = ['url', 'Nombre', 'Otros_nombres', 'Pedania', 'Municipio', 'Provincia', 'CoordX', 'CoordY', 'Cuenca', 'Subcuenca', 'Rio', 'Masa_agua', 'ENP', 'Lugar', 'Naturaleza', 'Tipo', 'Descripcion', 'Instalaciones_asociadas', 'Caudal', 'Se_agota', 'Uso_agua', 'Acceso', 'Uso_publico', 'valoracion_acceso', 'Conservacion',
             'Amenazas', 'Descripcion_hidrogeol�gica', 'Descripcion_arquitectonica',  'Antecedentes_historicos', 'Aspectos_culturales', ' Otra_informacion', 'Cientifico', 'Minero', 'Paisajistico', 'Otros', 'Medioambiental', 'Recreativo', 'Historico', 'Arquitectonico', 'Economico', 'Arraigo', 'Valoracion', 'Autor', 'Fecha', 'Imagenes']
with open('conocetusfuentes_04_22.csv',  'a',newline='',encoding="ISO-8859-1") as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_NONE, escapechar="\\")
    writer.writerow(cabeceras)
    for i in range(1, ultimo_elemento):
        url = "http://www.conocetusfuentes.com/datos_fuente_" + str(i) + ".html"

        # Modificación cabecera HTTP para parecer humano
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
                   "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
        # Realizamos la petición a la web
        # Creamos un delta para añadir un espaciado a las peticiones
        t0 = time.time()
        req = requests.get(url, headers=headers)
        response_delay = time.time() - t0

        # Comprobamos que la petición nos devuelve un Status Code = 200
        status_code = req.status_code
        if status_code == 200:

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")
    
            # Obtenemos todos los div y span donde están las entradas
            ficha_detalle = html.find(['div'], {'id': 'ficha_detalle'})
            columna_1 = ficha_detalle.findChild('div', {'id':'columna_1'})
            indice_titulos = 0
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos];
            output_rows = [url]
            camposDiv = columna_1.findChildren('div', {'class':'nombre_campo'})
            valoresDiv = columna_1.findChildren('div', {'class':'valor_campo'})
            valoresSpan = columna_1.findChildren('span', {'class':'valor_campo'})
            j=0
            diccionario = {'\u012d': '', '\u200b': '', '\u0144': '', '\u201d': '', '\u012c': '', '\u1d52': '', '\u03bc':'', '\u2a5d': '', '\u2282': '', '\xa0': '', '\r\n': ' ', '\n': ' ','\t': '', '\r': '', '<br/>': ' ', ";" : "-"}
            regex = re.compile("(%s)" % "|".join(map(re.escape, diccionario.keys())))
            
            if ("Localizaci�n" in titulo_h4): 
                indice_titulos = indice_titulos+1
                nombre = valoresDiv[0].getText().strip()
                nombre = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), nombre)
                i=1;
                otros_nombres = ""
                campo = camposDiv[1].getText()
                if (campo=="Otros nombres conocidos:"):
                    otros_nombres=valoresDiv[1].getText().strip()
                    otros_nombres = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), otros_nombres)
                    i=i+1
                pedania = valoresDiv[i].getText().strip()
                pedania = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), pedania)      
                i=i+1
                municipio = valoresDiv[i].getText().strip()
                municipio = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), municipio)
                i=i+1
                provincia = valoresDiv[i].getText().strip()
                provincia = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), provincia)
                i=i+1
                coordenadas = valoresDiv[i].getText()
                pos1 = coordenadas.index(":")+1
                pos2 = coordenadas.index("Y")-1
                coordX = coordenadas[pos1:pos2]
                coordX = coordX.replace(".",",").replace('\xa0','')
                coordenadas = coordenadas[pos2:len(coordenadas)-1]
                pos1 = coordenadas.index(":")+1
                pos2 = coordenadas.index("H")-1
                coordY = coordenadas[pos1:pos2]
                coordY = coordY.replace(".",",").replace('\xa0','')
                i=i+1
                cuenca = valoresDiv[i].getText().strip()
                cuenca = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), cuenca)
                i=i+1
                subcuenca = valoresDiv[i].getText().strip()
                subcuenca = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), subcuenca)
                i=i+1
                rio = valoresDiv[i].getText().strip()
                rio = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), rio)
                i=i+1
                masa_agua = valoresDiv[i].getText().strip()
                masa_agua = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), masa_agua)
                i=i+1
                ENP = valoresDiv[i].getText().strip()
                ENP = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), ENP)
                i=i+1
            else:
                nombre = ''
                otros_nombres=''
                pedania = ''
                municipio = ''
                provincia = ''
                coordX = 0
                coordY = 0
                cuenca = ''
                subcuenca = ''
                rio = ''
                masa_agua= ''
                ENP = ''
            output_rows.append(nombre)
            output_rows.append(otros_nombres)
            output_rows.append(pedania)
            output_rows.append(municipio)
            output_rows.append(provincia)
            output_rows.append(coordX)
            output_rows.append(coordY)
            output_rows.append(cuenca)
            output_rows.append(subcuenca)
            output_rows.append(rio)
            output_rows.append(masa_agua)
            output_rows.append(ENP)    
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Procedencia del agua subterr�nea" in titulo_h4):
                indice_titulos = indice_titulos+1
                lugar =  valoresDiv[i].getText().strip()
                lugar = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), lugar)
                i = i+1                
                naturaleza=  valoresDiv[i].getText().strip()
                naturaleza = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), naturaleza)
                i = i+1
            else:
                lugar  = ''
                naturaleza  = ''    
            output_rows.append(lugar)
            output_rows.append(naturaleza)
                
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ((titulo_h4.find("Tipo de surgencia"))!=-1):
                indice_titulos = indice_titulos+1
                tipo =  valoresDiv[i].getText().strip()
                tipo = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), tipo)
                i = i+1
            else:
                tipo = ''
            output_rows.append(tipo)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ((titulo_h4.find("Descripci�n"))!=-1):
                indice_titulos = indice_titulos+1
                descripcion =  valoresSpan[j].getText().strip()
                descripcion = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), descripcion)
                j = j+1
            else:
                descripcion = ''
            output_rows.append(descripcion)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ((titulo_h4.find("Instalaciones asociadas"))!=-1):
                indice_titulos = indice_titulos+1
                instalaciones =  valoresSpan[j].getText().strip()
                instalaciones = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), instalaciones)
                j = j+1
            else:
                instalaciones  = ''
            output_rows.append(instalaciones)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ((titulo_h4.find("Caudal medio"))!=-1):
                indice_titulos = indice_titulos+1
                caudal =  valoresSpan[j].getText().strip()
                caudal = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), caudal)
                j = j+1                
                se_agota =  valoresSpan[j].getText().strip()
                se_agota = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), se_agota)
                j = j+1
            else:
                caudal = ''
                se_agota = ''
            output_rows.append(caudal)
            output_rows.append(se_agota)
                
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Uso del agua" in titulo_h4):
                indice_titulos = indice_titulos+1
                uso_agua =  valoresSpan[j].getText().strip()
                uso_agua = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), uso_agua)
                j = j+1
            else:
                uso_agua = ''
            output_rows.append(uso_agua)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Acceso y uso p�blico actual" in titulo_h4):
                indice_titulos = indice_titulos+1
                acceso =  valoresSpan[j].getText().strip()
                acceso = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), acceso)
                j = j+1                
                uso_publico =  valoresSpan[j].getText().strip()
                uso_publico = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), uso_publico)
                j = j+1                
                valoracion_acceso =  valoresSpan[j].getText().strip()
                valoracion_acceso = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), valoracion_acceso)
                j = j+1
            else:
                acceso = ''
                uso_publico = ''
                valoracion_acceso = ''
            output_rows.append(acceso)    
            output_rows.append(uso_publico)
            output_rows.append(valoracion_acceso)
              
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Estado de conservaci�n" in titulo_h4):
                indice_titulos = indice_titulos+1
                estado_conservacion =  valoresSpan[j].getText().strip()
                estado_conservacion = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), estado_conservacion)
                j = j+1
            else:
                estado_conservacion = ''
            output_rows.append(estado_conservacion)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Amenazas, impactos y presiones" in titulo_h4):
                indice_titulos = indice_titulos+1
                amenazas =  valoresSpan[j].getText().strip()
                amenazas = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), amenazas)
                j = j+1
            else:
                amenazas = ''
            output_rows.append(amenazas)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Descripci�n hidrogeol�gica" in titulo_h4):
                indice_titulos = indice_titulos+1
                descripcion_hidrogeologica =  valoresSpan[j].getText().strip()
                descripcion_hidrogeologica = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), descripcion_hidrogeologica)
                j = j+1
            else:
                descripcion_hidrogeologica = ''
            output_rows.append(descripcion_hidrogeologica)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Descripci�n arquitect�nica" in titulo_h4):
                indice_titulos = indice_titulos+1
                descripcion_arquitectonica =  valoresSpan[j].getText().strip()
                descripcion_arquitectonica = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), descripcion_arquitectonica)
                j = j+1
            else:
                descripcion_arquitectonica = ''
            output_rows.append(descripcion_arquitectonica)            
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Antecedentes hist�ricos" in titulo_h4):
                indice_titulos = indice_titulos+1
                antecedentes_historicos =  valoresSpan[j].getText().strip()
                antecedentes_historicos = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), antecedentes_historicos)
                j = j+1
            else:
                antecedentes_historicos = ''
            output_rows.append(antecedentes_historicos)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Aspectos culturales y etnogr�ficos" in titulo_h4):
                indice_titulos = indice_titulos+1
                aspectos_culturales =  valoresSpan[j].getText().strip()
                aspectos_culturales = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), aspectos_culturales)
                j = j+1
            else:
                aspectos_culturales = ''
            output_rows.append(aspectos_culturales)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Otra informaci�n" in titulo_h4):
                indice_titulos = indice_titulos+1
                otra_informacion =  valoresSpan[j].getText().strip()
                otra_informacion = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), otra_informacion)
                j = j+1
            else:
                otra_informacion = ''
            output_rows.append(otra_informacion)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Valores sectoriales" in titulo_h4):
                indice_titulos = indice_titulos+1
                cientifico =  valoresSpan[j].getText().strip()
                cientifico = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), cientifico)
                j = j+1
                minero =  valoresSpan[j].getText().strip()
                minero = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), minero)
                j = j+1
                paisajistico =  valoresSpan[j].getText().strip()
                paisajistico = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), paisajistico)
                j = j+1
                otros =  valoresSpan[j].getText().strip()
                otros = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), otros)
                j = j+1
                medioambiental =  valoresSpan[j].getText().strip()
                medioambiental = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), medioambiental)
                j = j+1
                recreativo =  valoresSpan[j].getText().strip()
                recreativo = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), recreativo)
                j = j+1
                historico =  valoresSpan[j].getText().strip()
                historico = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), historico)
                j = j+1
                arquitectonico =  valoresSpan[j].getText().strip()
                arquitectonico = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), arquitectonico)
                j = j+1
                economico =  valoresSpan[j].getText().strip()
                economico = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), economico)
                j = j+1
                arraigo =  valoresSpan[j].getText().strip()
                arraigo = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), arraigo)
                j = j+1

            else:
                cientifico = ''
                minero = ''
                paisajistico = ''
                otros = ''
                medioambiental = ''
                recreativo = ''
                historico = ''
                arquitectonico = ''
                economico = ''
                arraigo = ''
            output_rows.append(cientifico)
            output_rows.append(minero)
            output_rows.append(paisajistico)
            output_rows.append(otros)
            output_rows.append(medioambiental)
            output_rows.append(recreativo)
            output_rows.append(historico)
            output_rows.append(arquitectonico)
            output_rows.append(economico)
            output_rows.append(arraigo)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Valoraci�n general" in titulo_h4):
                indice_titulos = indice_titulos+1
                valoracion_general =  valoresSpan[j].getText().strip()
                valoracion_general = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), valoracion_general)
                j = j+1
            else:
                valoracion_general = ''
            output_rows.append(valoracion_general)
            titulo_h4 = columna_1.findChildren(['h4'])[indice_titulos]
            if ("Nombre del autor/es y fecha de la ficha" in titulo_h4):
                indice_titulos = indice_titulos+1
                autor =  valoresSpan[j].getText().strip()
                autor = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), autor)
                j = j+1
                fecha =  valoresSpan[j].getText().strip()
                fecha = regex.sub(lambda x: str(diccionario[x.string[x.start() :x.end()]]), fecha)
                j = j+1
            else:
                autor = ''
                fecha = ''
            output_rows.append(autor)
            output_rows.append(fecha)

            # Añadimos todas las url de imágenes, ya sean de la fuente o de la ubicación
            for img in html.find_all("img", {'src': re.compile(r'fuente.*[.jpg]$|ubicacion.*[.jpg]$')}):
                images = img.attrs.get("src")
                output_rows.append(images)

            print(output_rows)
            if (len(nombre)>0):
                writer.writerow(output_rows)
            time.sleep(1)     
        # Aplicamos un espaciado entre peticiones    
        time.sleep(5 * response_delay)          
           
