# coding=utf-8
from bs4 import BeautifulSoup
import requests
import csv

cabeceras =['url','Nombre', 'Pedania', 'Municipio', 'Provincia', 'Coordenadas', 'Cuenca', 'Subcuenca', 'Rio', 'Masa_agua', 'ENP', 'Lugar', 'Naturaleza','Tipo', 'Descripcion', 'campo_vacio', 'Caudal', 'Se_agota', 'Uso_agua', 'Acceso', 'Uso_publico','valoracion_acceso','Conservacion', 'Amenazas', 'Cientifico', 'Minero', 'Paisajistico', 'Otros', 'Medioambiental', 'Recreativo', 'Historico', 'Arquitectonico', 'Economico', 'Arraigo', 'Valoracion', 'Autor', 'Fecha', 'Advertencia']
with open('Fuentes.csv', 'a',newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_NONE, escapechar="\\")
    writer.writerow(cabeceras)
    for i in range(368, 13099):
        url = "http://www.conocetusfuentes.com/datos_fuente_" + str(i) + ".html"

        # Realizamos la petición a la web
        req = requests.get(url)

        # Comprobamos que la petición nos devuelve un Status Code = 200
        status_code = req.status_code
        if status_code == 200:

            # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")
    
            # Obtenemos todos los div y span donde están las entradas
            entradas = html.find_all(['div','span'], {'class': 'valor_campo'})

            output_rows = [url]

            # Recorremos todas las entradas para extraer el título, autor y fecha
            for j, entrada in enumerate(entradas):
            # almacenar cada entrada en el csv
                txt = entrada.getText().strip().replace('\n', '').replace('\t','').replace('\x93','').replace('\x94','').replace('\r','').replace('\x96','').replace('\x85','').replace('\u2282','').replace('\x91','').replace('\x92','').replace('\u2a5d','').replace('\x95d','').replace('\x9d','').replace('\x95','').replace('\u03bc','').replace('\u1d52','').replace('\u012c','').replace('\x81','').replace('\x90','').replace('\x88','').replace('\u0144','').replace('\u200b','').replace('\u012d','').replace('\x97','')
                output_rows.append(txt)
     
            print(str(i) + ":")
            print(output_rows)
            writer.writerow(output_rows)
        
    