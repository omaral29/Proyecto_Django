import sqlite3 as sql
from django.shortcuts import render,HttpResponse,redirect
from django.template import loader
from django.contrib.auth import login
from django.template import RequestContext
import stripe
from django.conf import settings
from django.http import FileResponse
import os




def my_view(request):
    # Get the path to the PDF file.
    path_to_pdf_file = 'REPORTESDEMASRESERVASCONMAYORRESERVACION.pdf'

    response = FileResponse(open(path_to_pdf_file, 'rb'))

    return response

def my_view2(request):
    # Get the path to the PDF file.
    path_to_pdf_file = 'REPORTESDEEDAD.pdf'

    response = FileResponse(open(path_to_pdf_file, 'rb'))

    return response

def my_view3(request):
    # Get the path to the PDF file.
    path_to_pdf_file = 'REPORTESDEFECHA.pdf'

    response = FileResponse(open(path_to_pdf_file, 'rb'))

    return response





# Create your views here.
def index(request):
    template=loader.get_template('index.html')
    response = HttpResponse(template.render())
    response.set_cookie("Precio", 32)
    return response
    
def login(request):
    if request.method == "GET":
         return render(request, 'sisa.html')
    else:
        if request.POST['Oculto'] == "Usuario":
            db = sql.connect('db_royalpalm.db')
            cursor = db.cursor()
            validar = f"SELECT * FROM usuario WHERE cedula='{request.POST['cedula']}' AND clave='{request.POST['clave']}'"
            cursor.execute(validar)
            datos = list(cursor)
            db.commit()
            db.close
            validar = False
            name = str
            for x in datos:
                name = x[1]
                if request.POST['cedula'] == x[0]: validar = True
                else: validar = False
        
            if validar == True: 
                template=loader.get_template('menu_habitaciones.html')
                response = redirect('/menu/')
                response.set_cookie("nombre", name)
                response.set_cookie("cedula", request.POST['cedula'])
                response.set_cookie("clave", request.POST['clave'])
                response
                return response
            else: 
                return render(request, 'sisa.html',{
                'show':"Cedula o contrasena invalida"
                 })
        if request.POST['Oculto'] == "Administrador": 
            db = sql.connect('db_royalpalm.db')
            cursor = db.cursor()
            validar = f"SELECT * FROM usuario WHERE cedula='{request.POST['cedula']}' AND clave='{request.POST['clave']}'"
            cursor.execute(validar)
            datos = list(cursor)
            db.commit()
            db.close
            validar = False
            validar2 = False
            name = str
            show = ""
            for x in datos:
                name = x[1]
                if request.POST['cedula'] == x[0]: 
                    validar = True
                    if x[5] != "Administrador" : 
                        show = "No tienes rango administrador"
                        validar2 = True
                else: validar = False

            if validar == True or validar2 == True: 
                template=loader.get_template('crudusuarios.html')
                response = redirect('/habitacionescrud/')
                response.set_cookie("nombre", name)
                response.set_cookie("cedula", request.POST['cedula'])
                response.set_cookie("clave", request.POST['clave'])
                response
                return response
            else: 
                if validar == False: show = "No tienes rango administrador"
                else: show = "Cedula o contrasena invalida"
                return render(request, 'sisa.html',{
                'show': show
                 })

def registro(request):
    if request.method == "GET":
        return render(request, 'registro.html')
    else:
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM usuario WHERE cedula='{request.POST['cedula']}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        validar = True
        for x in datos:
            if request.POST['cedula'] == x[0]: validar = False
            else: validar = True

        if validar == False:
            return render(request, 'registro.html',{
                 'show':"Este usuario ya esta registrado"
             })
        
        else:
            db = sql.connect('db_royalpalm.db')
            cursor = db
            registrar = f"INSERT INTO usuario VALUES ('{request.POST['cedula']}','{request.POST['nombre']}','{request.POST['apellido']}','{request.POST['email']}','{request.POST['password']}','Usuario')"
            cursor.execute(registrar)
            db.commit()
            db.close()
            return redirect('/index/',{
                 'show':"Usuario registrado de forma exitosa"
             })
        


def menu_habitaciones(request):
    db = sql.connect('db_royalpalm.db')
    cursor = db.cursor()
    validar = f"SELECT * FROM habitaciones"
    cursor.execute(validar)
    datos = list(cursor)
    db.commit()
    db.close

    return render(request, 'menu_habitaciones.html',{
        'show': request.COOKIES['nombre'],
        'codigo': request.COOKIES['cedula'],
        'datos': datos
    })


def actualizar_datos_usuario(request):
    return render(request, 'actualizar_datos_usuario.html')

def reservar_habitacion(request, codigo, precio):

    if request.method == 'POST':

        token = request.POST.get('stripeToken')
        referencia = random.randint(0, 10000000000000000)
        reserva = random.randint(0, 10000000000000000)
        amount = request.POST['montototal'] # Monto en centavos (ejemplo: $10.00)
        days = request.POST['days']
        llegada = request.POST['start-date']
        salida = request.POST['end-date']

        db = sql.connect('db_royalpalm.db')
        cursor = db
        registrar = f"INSERT INTO pagos VALUES ('{referencia}','{request.COOKIES['cedula']}','Tarjeta','{llegada}','VISA')"
        cursor.execute(registrar)
        db.commit()
        

        cursor = db
        registrar = f"INSERT INTO Reservas VALUES ('{reserva}','{llegada}','{salida}','{referencia}','{request.POST['habitacion']}')"
        cursor.execute(registrar)
        db.commit()
        db.close()



        stripe.api_key = settings.STRIPE_API_KEY
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
            )
            # Procesar el pago exitoso
            return render(request, 'success.html',{
                'amount': amount,
                'days': days,
                'llegada': llegada,
                'salida': salida,
                'token': token

            })
        except stripe.error.CardError as e:
            # Manejar errores de tarjeta
            return render(request, 'error.html', {'error': e.error.message})
        
    return render(request, 'reservar_habitacion.html',{
                  'show': request.COOKIES['nombre'],
                  'codigo': request.COOKIES['cedula'],
                  'codigo': codigo,
                  'precio': precio,
                  'key': 'pk_test_51NA1bPC7tEcg5o67U21vadVCd1T3Zy5mfN9tnfeK1oAx9Mtv4p7Sr3nHiZKVS7JNa0xHukCWwwpkOeftjJp2Am89003pmglQ5j'
                  })
    

def logout(request):
    response = redirect('/index/')
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

def crudusersshow(request):
    if request.method == "GET":
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM usuario"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close()
        return render(request, 'actualizar_u_admin.html', {
            'users': datos
        })
    else: 
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM usuario WHERE cedula='{request.POST['cedula']}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        validar = True
        for x in datos:
            if request.POST['cedula'] == x[0]: validar = False
            else: validar = True

        if validar == False:
            db = sql.connect('db_royalpalm.db')
            cursor = db.cursor()
            validar = f"SELECT * FROM usuario"
            cursor.execute(validar)
            datos = list(cursor)
            db.commit()
            db.close
            return render(request, 'actualizar_u_admin.html',{
                 'show':"Este usuario ya esta registrado",
                 'users': datos
             })
        else:
            db = sql.connect('db_royalpalm.db')
            cursor = db
            registrar = f"INSERT INTO usuario VALUES ('{request.POST['cedula']}','{request.POST['nombre']}','{request.POST['apellido']}','{request.POST['correo']}','{request.POST['clave']}','Administrador')"
            cursor.execute(registrar)
            db.commit()
            db.close()
            return render('/crudusers',{
                 'show':"Usuario registrado de forma exitosa"
             })
        

    
def eliminarusuario(request, codigo):
    db = sql.connect('db_royalpalm.db')
    cursor = db.cursor()
    validar = f"DELETE FROM usuario WHERE cedula='{codigo}'"
    cursor.execute(validar)
    datos = list(cursor)
    db.commit()
    db.close
    return redirect('/crudusers')

def actualizarusuario(request, codigo):
    if request.method == "GET":
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM usuario WHERE cedula='{codigo}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        dato = datos[0] 
        return render(request, 'actualizar_u_ads.html',{
            'user': dato
        })
    else:
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"UPDATE usuario SET nombre='{request.POST['nombre']}', apellido='{request.POST['apellido']}', correo='{request.POST['email']}', clave='{request.POST['password']}' WHERE cedula='{codigo}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return redirect('/menu/')
    

def actualizarusuario1(request, codigo):
    if request.method == "GET":
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM usuario WHERE cedula='{codigo}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        dato = datos[0] 
        return render(request, 'actualizar_u_ads.html',{
            'user': dato
        })
    else:
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"UPDATE usuario SET nombre='{request.POST['nombre']}', apellido='{request.POST['apellido']}', correo='{request.POST['email']}', clave='{request.POST['password']}' WHERE cedula='{codigo}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return redirect('/menu/')



def habitacionescrud(request):
    if request.method == "GET":
        #Sentencia 1
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM habitaciones"
        cursor.execute(validar)
        datoshabitacion = list(cursor)
        db.commit()
        #Sentencia 2
        validar = f"SELECT * FROM tipo"
        cursor.execute(validar)
        datostipo = list(cursor)
        db.commit()
        db.close
        return render(request, "crudhabitaciones.html",{
            'tipo':datostipo,
            'habitacion': datoshabitacion     
            })
    else:
    
         #Sentencia 1
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM habitaciones"
        cursor.execute(validar)
        datoshabitacion = list(cursor)
        db.commit()
        #Sentencia 
        validar = f"SELECT * FROM tipo"
        cursor.execute(validar)
        datostipo = list(cursor)
        db.commit()
        
       
        validar = f"INSERT INTO habitaciones VALUES ('{request.POST['num_habitacion']}','{request.POST['precio']}','{request.POST['tipo']}')"
        cursor.execute(validar)
        db.commit()
        db.close() 
        return render(request, "crudhabitaciones.html",{
            'tipo':datostipo,
            'habitacion': datoshabitacion   
        
        })
    




def actualizarhabitacion(request, codigo):
     if request.method == "GET":
        #Sentencia 1
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM habitaciones WHERE num_habitacion='{codigo}'"
        cursor.execute(validar)
        datoshabitacion = list(cursor)
        db.commit()
        #Sentencia 2
        validar = f"SELECT * FROM tipo"
        cursor.execute(validar)
        datostipo = list(cursor)
        db.commit()
        db.close
        dato = datoshabitacion[0] 
        return render(request, 'actualizar_habitacion.html',{
            'habitacion': dato,
            'tipo':datostipo,
        })
     else:
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"UPDATE habitaciones SET Precio='{request.POST['precio']}', tipo='{request.POST['tipoin']}' WHERE cedula='{codigo}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return redirect('/habitacionescrud/')
     
def eliminarhabitacion(request, codigo):
    db = sql.connect('db_royalpalm.db')
    cursor = db.cursor()
    validar = f"DELETE FROM habitaciones WHERE num_habitacion='{codigo}'"
    cursor.execute(validar)
    datos = list(cursor)
    db.commit()
    db.close
    return redirect('/habitacionescrud')


def crudtipos(request):
    if request.method == "GET":
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM tipo"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        return render(request, "crudtipos.html",{
            'tipos': datos
        })
    
    else:
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM tipo WHERE id='{request.POST['id']}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        validar = True
        for x in datos:
            if request.POST['id'] == x[0]: validar = False
            else: validar = True

        if validar == False:
            db = sql.connect('db_royalpalm.db')
            cursor = db.cursor()
            validar = f"SELECT * FROM tipo"
            cursor.execute(validar)
            datos = list(cursor)
            db.commit()
            db.close
            return render(request, 'crudtipos.html',{
                 'show':"Este tipo de habitacion ya esta registrada",
                 'tipos': datos
             })
        else:
            db = sql.connect('db_royalpalm.db')
            cursor = db
            registrar = f"INSERT INTO tipo VALUES ('{request.POST['id']}','{request.POST['tiene_cocina']}','{request.POST['ocupacion']}','{request.POST['camas_dobles']}','{request.POST['camas_individuales']}','{request.POST['baños']}')"
            cursor.execute(registrar)
            db.commit()
            db.close()
            return render('/crudtipos',{
                 'show':"Usuario registrado de forma exitosa"
             })

def eliminartipo(request, codigo):
    db = sql.connect('db_royalpalm.db')
    cursor = db.cursor()
    validar = f"DELETE FROM tipo WHERE id='{codigo}'"
    cursor.execute(validar)
    datos = list(cursor)
    db.commit()
    db.close
    return redirect('/crudtipos')

def actualizartipo(request, codigo):
    if request.method == "GET":
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM tipo WHERE id='{codigo}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        dato = datos[0] 
        return render(request, 'actualizar_tipo.html',{
            'tipo': dato
        })
    else:
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"UPDATE tipo SET tiene_cocina='{request.POST['tiene_cocina']}', ocupacion='{request.POST['ocupacion']}', camasdobles='{request.POST['camas_dobles']}', camassencillas='{request.POST['camas_individuales']}', baños='{request.POST['baños']}' WHERE id='{codigo}'"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return redirect('/crudtipos')
    

def reportes(request):
    return render(request, "reportes.html")

def reporteusuario(request):
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM usuario"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return render(request, 'reporteusuario.html', {
            'users': datos
        })

def reportehabitaciones(request):
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM habitaciones"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return render(request, 'reportehabitaciones.html', {
            'y': datos
        })

def reportereserva(request):
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM Reservas"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return render(request, 'reportereserva.html', {
            'x': datos
        })

def reportepagos(request):
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"SELECT * FROM Pagos"
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        db.close
        return render(request, 'reportepagos.html', {
            'x': datos
        })

def reportetomadedecisiones(request):
        #Sentencia 1 
        db = sql.connect('db_royalpalm.db')
        cursor = db.cursor()
        validar = f"""SELECT Metodo_de_Pago, COUNT(Metodo_de_Pago) AS total
                        FROM  Pagos
                        GROUP BY Metodo_de_Pago
                        ORDER BY total DESC 
        """
        cursor.execute(validar)
        datos = list(cursor)
        db.commit()
        #Sentencia 2
        cursor = db.cursor()
        validar = f"""SELECT Num_habitacion, COUNT(Num_habitacion) AS total
                        FROM  Reservas
                        GROUP BY Num_habitacion
                        ORDER BY total DESC 
        """
        cursor.execute(validar)
        datos2 = list(cursor)
        db.commit()
        db.close
        return render(request, 'reportetomadedecisiones.html', {
            'x': datos,
            'z': datos2
        })

def misreportes(request):
    db = sql.connect('db_royalpalm.db')
    cursor = db.cursor()
    validar = f"SELECT r.* FROM Reservas r INNER JOIN Pagos p ON r.Num_referencia = p.num_referencia WHERE p.cedula_cliente = '{request.COOKIES['cedula']}'"
    cursor.execute(validar)
    datos = list(cursor)
    db.commit()
    db.close
    return render(request, 'misreservas.html', {
            'show': request.COOKIES['nombre'],
            'codigo': request.COOKIES['cedula'],
            'x': datos
        })


def process_payment(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        amount = 1000  # Monto en centavos (ejemplo: $10.00)

        stripe.api_key = settings.STRIPE_API_KEY
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
            )
            # Procesar el pago exitoso
            return render(request, 'success.html')
        except stripe.error.CardError as e:
            # Manejar errores de tarjeta
            return render(request, 'error.html', {'error': e.error.message})

    return render(request, 'checkout.html', {
        'key': stripe.api_key 

    })
def ads1(request):
    return render(request, "ads1.html")
def ads2(request):
    return render(request, "ads2.html")
def ads3(request):
    return render(request, "ads3.html")