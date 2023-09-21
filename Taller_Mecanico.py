import datetime
import re
import csv
import ast
import openpyxl

def contiene_digitos(nombre):
    for caracter in nombre:
        if caracter.isdigit():
            return True
    return False

notas = dict()

try:
    with open("notas.csv","r") as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for row in lector:
            folio = row[0]
            fecha_str = row[1]
            cliente = row[2]
            rfc = row[3]
            correo = row[4]
            detalle_str = row[5]
            monto = row[6]
            estado =row[7]
            
            fecha = datetime.datetime.strptime(fecha_str, "%d-%m-%Y")
            detalle_lista = ast.literal_eval(detalle_str)
            
            notas[int(folio)] =[fecha,cliente,rfc,correo,detalle_lista,float(monto),ast.literal_eval(estado)]
except FileNotFoundError:
    print("\nEl archivo CSV no existe. No se han cargado notas previas ")

menu = """
╔═══════════════════════
║  Menú Principal      ║
╠═══════════════════════
║ 1. Registrar una nota║
║ 2. Consultas y       ║
║    reportes          ║
║ 3. Cancelar una nota ║
║ 4. Recuperar nota    ║
║ 5. Salir             ║
╚═══════════════════════
"""
menu_consulta = """
╔════════════════════════════╗
║      MENÚ DE CONSULTA      ║
╟────────────────────────────╢
║ 1. Consultar por período.  ║
║ 2. Consultar por folio.    ║
║ 3. Consulta por cliente    ║
╚════════════════════════════╝
"""
generador_folio=0
patron_fecha = r"^\d{2}-\d{2}-\d{4}$"
fecha_actual =datetime.datetime.now()


while True:
    print(menu)
    opcion=input("\nIngrese una opción:\n")
    if opcion=="1":#ANGEL MORALES VENTURA
        generador_folio=len(notas)
        generador_folio+=1
        folio=generador_folio
        
        while True:
            
            fecha_ingresada_str = input("\nFecha de la nota (dd-mm-aaaa): ").strip()
            
            if not fecha_ingresada_str:
                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
            elif not re.match(patron_fecha, fecha_ingresada_str):
                print("FORMATO DE FECHA INCORRECTO. DEBE SER DD-MM-AAAA")
            else:
                try:
                    fecha_ingresada = datetime.datetime.strptime(fecha_ingresada_str, "%d-%m-%Y")
                    if fecha_ingresada > fecha_actual:
                        print("LA FECHA NO DEBE SER POSTERIOR A LA FECHA ACTUAL DEL SISTEMA")
                    else:
                        break
                except ValueError:
                    print("LA FECHA NO ES VÁLIDA/NO EXISTE. INTENTE DENUEVO.")
        
        while True:
            cliente = input("\nNombre del cliente: ").strip()
            
            if cliente== "":
                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
            elif any(char.isdigit() for char in cliente):
                print("EL NOMBRE NO PUEDE CONTENER DÍGITOS. INTENTE NUEVAMENTE.")
            else:
                break
        
        while True:
            rfc_ingresado = input("\nIngrese un RFC (por ejemplo: XEXT990101NI4): ").strip().upper()
            
            if not rfc_ingresado:
                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
            elif not re.match(r'^[A-Z]{4}[0-9]{6}[A-Z0-9]{3}$', rfc_ingresado):
                print("EL RFC INGRESADO NO TIENE EL FORMATO CORRECTO. INTENTE NUEVAMENTE.")
            else:
                try:
                    fecha_rfc = datetime.datetime.strptime(rfc_ingresado[4:10], '%y%m%d')
                    break
                except ValueError:
                    print("LA FECHA EN EL RFC NO ES VÁLIDA. INTENTE NUEVAMENTE.")
        
        while True:
            correo = input("\nIngrese su correo electrónico gmail (por ejemplo: correo123@gmail.com): ").strip()

            if not correo:
                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
            elif not correo.endswith('@gmail.com'):
                print("EL CORREO ELECTRÓNICO DEBE SER DE DOMINIO 'gmail.com'. INTENTE NUEVAMENTE")  
            else:
                break
        
        detalle=list()
        monto=0.0
        notas[folio]=[fecha_ingresada,cliente,rfc_ingresado,correo,detalle,monto,True]
        
        while True:
            
            nombre_servicio = input("\nNombre del servicio: ").strip()
            if nombre_servicio == "":
                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
                continue

            while True:
                
                costo_servicio = input("\nCosto del servicio: ").strip()
                if costo_servicio == "":
                    print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
                    continue
                
                try:
                    costo_servicio = float(costo_servicio)
                    if costo_servicio <= 0:
                        print("EL COSTO DEBE SER MAYOR A 0 PESOS. INTENTE DENUEVO")
                        continue
                    else:
                        notas[folio][4].append((nombre_servicio, costo_servicio))
                        notas[folio][5] += costo_servicio
                        break
                except ValueError:
                    print("SE INGRESÓ UN CARÁCTER NO NUMÉRICO. INTENTE DENUEVO ")
        
            if input("\n¿Agregar otro servicio? (s/n):\n ").lower() != "s":
                print("\n**************************")
                print("         NOTA")
                print("**************************")
                print(f"Folio: {folio:04}")
                print(f"Fecha de la nota: {fecha_ingresada.strftime('%d-%m-%Y')}")
                print(f"Cliente: {cliente}")
                print(f"RFC: {rfc_ingresado}")
                print(f"Correo electrónico: {correo}")
                print("\nDetalles de los servicios:")
                for servicio, costo in notas[folio][4]:
                    print(f"  - {servicio:<20}: ${costo:.2f}")
                print("------------------------------")
                print(f"Monto total:          ${notas[folio][5]:.2f}")
                print("**************************")
                break
    elif opcion=="2":#MONTERO CASTILLO DAVID EDUARDO
        pass
    elif opcion=="3":#GONZALEZ INFANTE ALAN JAIR
        while True:
            folio_cancelar = input("\nIngrese el folio de la nota a cancelar/ 0 para ingresar al menú principal: ").strip()
            
            if folio_cancelar=="":
                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
                continue

            if folio_cancelar=="0":
                break

            try:
                folio_cancelar=int(folio_cancelar)
                
                if not folio_cancelar in notas:
                    print("\nNOTA NO ENCONTRADA EN EL SISTEMA.")
                    continue
            except Exception:
                print("CARÁCTER NO VÁLIDO. SOLO DÍGITOS NUMÉRICOS")
                continue

            if notas [folio_cancelar][6]==True:
                print("\n**************************")
                print("         NOTA")
                print("**************************")
                print(f"Folio: {folio_cancelar:04}")
                print(f"Fecha de la nota: {notas[folio_cancelar][0].strftime('%d-%m-%Y')}")
                print(f"Cliente: {notas[folio_cancelar][1]}")
                print(f"RFC: {notas[folio_cancelar][2]}")
                print(f"Correo electrónico: {notas[folio_cancelar][3]}")
                print("\nDetalles de los servicios:")
                for servicio, costo in notas[folio_cancelar][4]:
                    print(f"  - {servicio:<20}: ${costo:.2f}")
                print("-------------------------------")
                print(f"Monto total:      ${notas[folio_cancelar][5]:.2f}")
                print("**********************")
            else:
                print("NOTA NO ENCONTRADA EN EL SISTEMA.")
                continue
            while True:

                confirmacion = input("¿Confirmar la cancelación de esta nota? (s/n): ").lower().strip()
                
                if confirmacion=="":
                    
                    print("EL DATO NO PUEDE OMITIRSE. INTENTE NUEVAMENTE.")
                elif confirmacion== "s":

                    notas[folio_cancelar][6] = False
                    print(f"\nNota con folio {folio_cancelar} ha sido cancelada.\n")
                    break
                elif confirmacion=="n":
                    
                    print("\nNOTA NO CANCELADA\n")
                    break
                else:
                    
                    print("OPCIÓN NO VÁLIDA. INTENTE NUEVAMENTE.")
            break
        
    elif opcion=="4":#GONZALEZ INFANTE ALAN JAIR
        encontradas_canceladas = False

        for folio, nota in notas.items():
            if nota[6] == False:
                encontradas_canceladas = True

        if not encontradas_canceladas:
            print("\nNO SE ENCONTRARON NOTAS EN EL SISTEMA.\n")
            continue
        print("Folio   |   Fecha        |   Cliente              |   RFC          |   Correo                        |   Monto")
        print("-" * 100)

        for folio, nota in notas.items()
            if nota[6]==False:
                fecha = nota[0].strftime('%d-%m-%Y')
                cliente = nota[1]
                rfc = nota[2]
                correo = nota[5]
                monto = nota[5]
                
                cliente = clienteljust(23)
                rfc = rfc.ljust(15)
                correo = correo.ljust(30)
                
                print(f"{folio:<7} |   {fecha:<12} |   {cliente} |   {rfc} |   {correo} |   ${monto:.2f}")

        while True:

            folio_rescate = input("\nNota a recuperar(Indique número de folio)/0 para volver al menú principal:\n ").strip()
            
            if folio_rescate=="":
                print("EL DATO NO PUEDE OMITIRSE. INTENTE DENUEVO.")
                continue
                
            elif folio_rescate=="0":
                break
            else:
                try:
                    folio_rescate=int(folio_rescate)
                    if not folio_rescate in notas:
                        print("NOTA NO ENCONTRADA. INTENTE NUEVAMENTE")
                        continue
                except ValueError:
                    print("Ingrese un número de folio válido.\n")
                    continue
            if folio_rescate in notas and notas[folio_rescate][6]==False:
                print("\n**************************")
                print("         NOTA")
                print("**************************")
                print(f"Folio: {folio_rescate:04}")
                print(f"Fecha de la nota: {notas[folio_rescate][0].strftime('%d-%m-%Y')}")
                print(f"Cliente: {notas[folio_rescate][1]}")
                print(f"RFC: {notas[folio_rescate][2]}")
                print(f"Correo electrónico: {notas[folio_rescate][3]}")
                print("\nDetalles de los servicios.:")
                for servicio, costo in notas[folio_rescate][4]:
                    print(f"  - {servicio:<20}: ${costo:.2f}")
                print("**************************")
                while True:
                    confirmacion = input("¿Confirmar la recuperación de esta nota? (s/n): ").lower().strip()
                    
                    if confirmacion=="":
                     print("NO SE PUEDE OMITIR EL DATO")
                     continue
                    elif confirmacion=="n":
                        print("\nNOTA NO FUE RECUPERADA\n")
                        break
                    elif confirmacion=="s":
                        notas[folio_rescate][6] = True
                        print(f"\nNota con folio {folio_rescate:04} ha sido recuperada.\n")
                        break
                    else:
                        print("OPCIÓN NO VÁLIDA")
                        continue
               break
    else:
        print("FOLIO NO ENCONTRADO EN EL SISTEMA")
    elif opcion=="5":#ANGEL MORALES VENTURA
        if input("SEGURO DESEA SALIR DEL PROGRAMA? (S/N o Enter para volver a menu principal):\n ").upper()=="S":
            break
        else:
            continue 
    else:
        print("OPCIÓN NO VALIDA.INTENTE NUEVAMENTE.")
        
nombre_archivo = "notas.csv"
try:
    with open(nombre_archivo,"w",newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        for folio, datos in notas.items():
            fecha,cliente,rfc,correo,detalle,monto,estado = datos
            fecha_str = fecha.strftime('%d-%m-%Y')
            estado_str = estado
            escritor.writerow([folio,fecha_str,cliente,rfc,correo,detalle,monto,estado_str])
    print(f"Se han guardado los datos en {nombre_archivo}")
except Exception as e:
    print(f"ERROR AL GUARDAR LOS DATOS EN EL ARCHIVO CSV: {e}")
        
        
            
        
