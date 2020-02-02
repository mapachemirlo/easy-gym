# -*- coding: utf-8 -*-
# EASY-GYM - Sistema de gestión de clientes para gimnasio
# version 1.0
# Desarrollador - Claudio Herrera
# Empresa - Procyon
# Septiembre 2019

import sys
import calendar
import imagenes
from datetime import datetime, date, time, timedelta
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QPushButton, QMessageBox 
from PyQt5 import QtCore, QtGui, QtWidgets
from db import Run_query
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from db import Run_query


    
######################################## VENTANA PRINCIPAL ####################################################
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('principal.ui', self)

        menu = self.menuBar()
        menu_archivo = menu.addMenu("&Archivo")
        menu_ayuda = menu.addMenu("&Ayuda")

        menu_archivo_salir = QAction(QIcon(), "&Cerrar", self)
        menu_archivo_salir.setShortcut('Ctrl+E')
        menu_archivo_salir.setStatusTip("Cerrar")
        menu_archivo_salir.triggered.connect(self.SalirPrincipal)
        menu_archivo.addAction(menu_archivo_salir)

        menu_archivo_asist = QAction(QIcon(), "&Asistencias", self)
        menu_archivo_asist.setStatusTip("Asistencias")
        menu_archivo_asist.triggered.connect(self.abrirVentanaAsistencia)
        menu_archivo.addAction(menu_archivo_asist)

        menu_ayuda_acerca = QAction(QIcon(), "&Acerca de", self)
        menu_ayuda_acerca.setStatusTip("Acerca de")
        menu_ayuda_acerca.triggered.connect(self.abrirVentanaAcercade)
        menu_ayuda.addAction(menu_ayuda_acerca)


        self.lineEditPrinNumSocio.setValidator(QtGui.QDoubleValidator())
        self.lineEditPrinNumSocio.setMaxLength(5)
        #self.lineEditPrinNumSocio.setCursorPosition(0)

        self.btnPrinAltaSocio.clicked.connect(self.abrirVentanaAlta)
        self.btnPrinConsultaSocio.clicked.connect(self.abrirVentanaConsulta)
        self.btnPrinBuscarSocio.clicked.connect(self.BuscarNumSocio)
        self.btnPrinConfPago.clicked.connect(self.ConfirmaPago)
        self.btnPrinIngresoAsist.clicked.connect(self.RegistroAsistencia)

        fechalog = datetime.today()
        fechalog = str(fechalog)
        archiv = open('log.txt', 'a+')
        archiv.write(str(fechalog) + '\n')
        archiv.close()

        logueo = fechalog.split(".")
        log = ("SESIÓN INICIADA: " + logueo[0])
        self.statusBar().showMessage(log)

    def closeEvent(self, event):
        reply = QMessageBox.question(self,'SALIR', "Realmente desea cerrar la aplicacion",QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.BuscarNumSocio()
    
    def SalirPrincipal(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("DESEA CERRAR?")
        msgBox.setWindowTitle("Cerrar Aplicación")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)        
        returnValue = msgBox.exec_()
        if returnValue == QMessageBox.Ok:
            app.quit()
        else:
            print('Cancel')

    def abrirVentanaAlta(self):
        #self.hide()
        ventana_alta = VentanaAlta(self)
        ventana_alta.show()
        #self.close()

    def abrirVentanaConsulta(self):
        #self.hide()
        ventana_consulta = VentanaConsulta(self)
        ventana_consulta.show()

    def abrirVentanaAsistencia(self):
        ventana_asist = VentanaAsistencia(self)
        ventana_asist.show()

    def abrirVentanaAcercade(self):
        ventana_acerca = VentanaAcercade(self)
        ventana_acerca.show()
     
    def BuscarNumSocio(self):
        imput = self.lineEditPrinNumSocio.text()
        if imput == "":
            VentanaAlta.messagebox(self, "NO Ingresó N°", "INGRESE N° SOCIO!!")
        else:
            self.Buscar()
    # Acá está la variable global ---> my_id
    def Buscar(self):
        num_socio = self.lineEditPrinNumSocio.text()
        try:
            #query_bus_prin_id = "SELECT id, fecha_vence, actividad, promo FROM socios WHERE id='%s'" %num_socio
            query_bus_prin_id = "SELECT id, apellido, nombre, fecha_vence, actividad, promo FROM socios WHERE id='%s'" %num_socio
            resul_id = Run_query(query_bus_prin_id)
            resul_id = str(resul_id).split("'")
            print(resul_id)
            print(resul_id[0]) #id
            print(resul_id[1]) #apellido
            print(resul_id[3]) #nombre
            print(resul_id[5]) #vencimiento
            print(resul_id[7]) #actividad
            print(resul_id[9]) #promo

            id_limpio = resul_id[0].split(" ' ")
            id_2 = id_limpio[0].split('(')
            id_final = id_2[2].split(',')
            id_final = id_final[0] #ID FINAL 
            apellido = resul_id[1]
            nombre = resul_id[3]
            actividad = resul_id[7]
            promo = resul_id[9]

            global my_id #VARIABLE GLOBAL!!
            my_id = id_final

            self.labelPrintMostrarNumSocio.setText(id_final)
            self.labelPrinMostrarNombre.setText(nombre)
            self.labelPrinMostrarApellido.setText(apellido)
            self.labelPrinMostrarActividad.setText(actividad)
            self.labelPrinMostrarPromoSocio.setText(promo)

            # Busqueda si está vigente
            if resul_id[5] == "1":
                self.labelPrinMostrarEstado.setText("NO VIGENTE")
            else:
                fechi = resul_id[5]  # ESTADO
                fechi_vence = datetime.strptime(fechi, '%Y-%m-%d')
                fecha_actual = datetime.today()
                if fecha_actual > fechi_vence:
                    self.labelPrinMostrarEstado.setText("NO VIGENTE")
                    print("\nNO VIGENTE")
                else:
                    self.labelPrinMostrarEstado.setText("VIGENTE")
                    print("\nVIGENTE")
            self.lineEditPrinNumSocio.clear()
        except:
            #self.labelPrinMostrarEstado.setText("NO EXISTE EL NUMERO")
            VentanaAlta.messagebox(self, "ERROR!", "NO EXISTE EL SOCIO")
            self.lineEditPrinNumSocio.clear()

    def InsertarPago(self):
        id_ = my_id
        actividad = ""
        promo = ""
        #cuota = ""

        fecha_alta = datetime.now()
        fecha_vence = date.today() + timedelta(days=30)
        fecha_alta = str(fecha_alta)
        fecha_vence = str(fecha_vence)
        fecha_pago = fecha_alta

        if self.radioButtonPrinMusculacion.isChecked():
            actividad = "MUSC"
        elif self.radioPrinButtonFitness.isChecked():
            actividad = "FIT"
        elif self.radioButtonPrinPaseLibre.isChecked():
            actividad = "LIBRE"
        elif self.radioPrinButtonPilates.isChecked():
            actividad = "PILAT"
        else: 
            self.radioButtonPrinBoxeo.isChecked()
            actividad = "BOX"

        if self.radioButtonPrinPromo.isChecked():
            promo = "PROMO"

        query_pagar = "UPDATE socios SET actividad='%s', promo='%s', fecha_pago='%s', fecha_vence='%s' WHERE id='%s'" %(actividad, promo, fecha_pago, fecha_vence, id_)

        Run_query(query_pagar)
        if(query_pagar):
            VentanaAlta.messagebox(self, "Bien!!!", "PAGO CONFIRMADO!") #ESTE MÉTODO ESTÁ DENTRO DE LA CLASE DE ALTA DE USUARIOS, SIEMPRE PIDE SELF
            print("Datos guardados!")


    # Método confirmar PAGO EN VENTANA PRINCIPAL
    def ConfirmaPago(self):
        if self.lineEditPrinNumSocio.text() == '':            
            VentanaAlta.messagebox(self, "ERROR", "INGRESE SOCIO")
        else:
            try:
                if self.lineEditPrinNumSocio.text() != my_id:
                    VentanaAlta.messagebox(self, "ERROR", "N° SOCIO MAL")
                else:
                    confi = QMessageBox()
                    confi.setIcon(QMessageBox.Information)
                    confi.setText("Desea confirmar el pago??")
                    confi.setWindowTitle("CONFIRMA PAGO")
                    confi.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retorno = confi.exec_()
                    if retorno == QMessageBox.Ok:
                        VentanaPrincipal.InsertarPago(self)
                        VentanaPrincipal.RegistroAsistencia(self)
                        self.radioButtonPrinPromo.setChecked(False)
                        self.lineEditPrinNumSocio.clear(), self.labelPrintMostrarNumSocio.clear(),
                        self.labelPrinMostrarNombre.clear(), self.labelPrinMostrarApellido.clear(),
                        self.labelPrinMostrarActividad.clear(), self.labelPrinMostrarPromoSocio.clear(),
                        self.labelPrinMostrarEstado.clear()
                        print('OK Clicked')
                    else:
                        print('Cancel')
            except:
                VentanaAlta.messagebox(self, "ERROR", "NO BUSCÓ EL SOCIO")

    def RegistroAsistencia(self):
        try:    
            id_asis = my_id
                
            fecha_today = date.today()
            fecha_asist = str(fecha_today)
                
            query_asist = "UPDATE socios SET fecha_asist='%s' WHERE id='%s'" %(fecha_asist, id_asis)
        
            Run_query(query_asist)
            if(query_asist):
                VentanaAlta.messagebox(self, "Bien!!!", "INGRESO OK!")
                print("INGRESO OK!")
        except:
            VentanaAlta.messagebox(self, "ERROR", "NO BUSCÓ EL SOCIO")

############################################ ASISTENCIA ######################################################
class VentanaAsistencia(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaAsistencia, self).__init__(parent)
        loadUi('asistencia.ui', self)

        #def LeerRegistroAsistencia(self):
        fecha_today = date.today()
        fecha_asist = str(fecha_today)

        query_ver_asist = "SELECT id, apellido, nombre, actividad, promo FROM socios WHERE fecha_asist='%s'" %(fecha_asist)
        resul_asist = Run_query(query_ver_asist)
        self.tableWidgetConAsistencia.setRowCount(0)

        for row_number, row_data in enumerate(resul_asist):
            self.tableWidgetConAsistencia.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                self.tableWidgetConAsistencia.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

############################################ ALTA SOCIO #######################################################   
class VentanaAlta(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaAlta, self).__init__(parent)
        loadUi('altasocio.ui', self)

        self.btnAltaSalir.clicked.connect(self.SalirAlta)
        self.btnAltaConfirmar.clicked.connect(self.Confirma)
        self.lineEditDNI.setValidator(QtGui.QDoubleValidator()) #validar solo números
        self.lineEditCelular.setValidator(QtGui.QDoubleValidator())
        self.lineEditTelLinea.setValidator(QtGui.QDoubleValidator())

        self.lineEditDNI.setMaxLength(8)
        self.lineEditCelular.setMaxLength(18)
        self.lineEditTelLinea.setMaxLength(18)

    # Método de mensaje que la Operación se realizó
    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.resize(400,280)
        mess.setIcon(QMessageBox.Information)
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    # Método confirmación Salir
    def SalirAlta(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Seguro que desea salir?")
        msgBox.setWindowTitle("Salir")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)        
        returnValue = msgBox.exec_()
        if returnValue == QMessageBox.Ok:
            self.parent().show()
            self.close()
        else:
            print('Cancel')

    # Método confirmar Operación
    def Confirma(self):
        apellido = self.lineEditApellido.text()
        nombre = self.lineEditNombre.text()

        if self.lineEditApellido.text() == '' or self.lineEditNombre.text() == '':      
            self.messagebox("ERROR", "DATOS INCOMPLETOS")
        if self.lineEditApellido.text() != '' and self.lineEditNombre.text() != '':
            ape_ = apellido[0]
            nom_ = nombre[0]
            if ape_ == ' ' or nom_ == ' ':
                self.messagebox("MAL ESCRITO", "NO EMPEZAR CON ESPACIOS")
            else:
                confi = QMessageBox()
                confi.setIcon(QMessageBox.Information)
                confi.setText("CONFIRMA?")
                confi.setWindowTitle("CONFIRMA ALTA")
                confi.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                retorno = confi.exec_()
                if retorno == QMessageBox.Ok:
                    VentanaAlta.InsertarAlta(self)
                    self.lineEditNombre.clear(),self.lineEditApellido.clear(),self.lineEditDNI.clear(),
                    self.lineEditDomicilio.clear(), self.lineEditLocalidad.clear(), self.lineEditCelular.clear(),
                    self.lineEditTelLinea.clear(),self.lineEditEmail.clear(),self.lineEditRedSocial.clear(),
                    self.lineEditObservacion.clear(),
                    self.radioButtonPromo.setChecked(False) 
                    print('OK Clicked')
                else:
                    print('Cancel')

    # Método insertar datos en la DB
    def InsertarAlta(self):
        fecha_alta = datetime.now()
        fecha_vence = date.today() + timedelta(days=30)
        fecha_alta = str(fecha_alta)
        fecha_pago = fecha_alta
        fecha_vence = str(fecha_vence)
       

        fecha_today = date.today()
        fecha_asist = str(fecha_today)

        sexo = ""
        actividad = ""
        promo = ""

        apellido = self.lineEditApellido.text()
        nombre = self.lineEditNombre.text()
        DNI = self.lineEditDNI.text()
        domicilio = self.lineEditDomicilio.text()
        localidad = self.lineEditLocalidad.text()
        celular = self.lineEditCelular.text()
        telelinea = self.lineEditTelLinea.text()
        email = self.lineEditEmail.text()
        redsocial = self.lineEditRedSocial.text()
        observacion = self.lineEditObservacion.text()

        if self.radioButtonMasculino.isChecked():
            sexo = "M"
        else: 
            self.radioButtonFemenino.isChecked()
            sexo = "F"

        if self.radioButtonMusculacion.isChecked():
            actividad = "MUSC"
        elif self.radioButtonFitness.isChecked():
            actividad = "FIT"
        elif self.radioButtonPaseLibre.isChecked():
            actividad = "LIBRE"
        elif self.radioButtonPilates.isChecked():
            actividad = "PILAT"
        else: 
            self.radioButtonBoxeo.isChecked()
            actividad = "BOX"

        if self.radioButtonPromo.isChecked():
            promo = "PROMO"

        query = ("INSERT INTO socios(apellido, nombre, DNI, domicilio, localidad, celular, telelinea, email, redsocial, observacion, sexo, actividad, promo, fecha_alta, fecha_pago, fecha_vence, fecha_asist) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(''.join(apellido), 
                ''.join(nombre),''.join(DNI),''.join(domicilio),''.join(localidad),''.join(celular),''.join(telelinea),''.join(email),''.join(redsocial),''.join(observacion),''.join(sexo),''.join(actividad),''.join(promo),''.join(fecha_alta),''.join(fecha_pago),''.join(fecha_vence),''.join(fecha_asist)))

        Run_query(query)    
        if(query):
            self.messagebox("Bien!!!", "ALTA EXITOSA!")
            print("Datos guardados!")

########################################### CONSULTA SOCIO ####################################################
class VentanaConsulta(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaConsulta, self).__init__(parent)
        loadUi('consulta.ui', self)

        self.lineEditConsultaNumSocio.setValidator(QtGui.QDoubleValidator())
        self.lineEditConsultaNumSocio.setMaxLength(5)
        self.lineEditAConsultaApellido.setMaxLength(30)
        self.lineEditConsultaNombre.setMaxLength(30)

        self.btnConsultaSalir.clicked.connect(self.SalirConsulta)
        self.btnConsultaActualizar.clicked.connect(self.abrirVentanaActualizar)
        self.btnConsultaBuscar.clicked.connect(self.ConsultaSocio)
        self.btnConsultaVerTodos.clicked.connect(self.VerSocios)
        self.btnConsultaEliminar.clicked.connect(self.ConfirmaEliminar)

        self.idsocio = ""

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.ConsultaSocio()

    def SalirConsulta(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("SEGURO DESEA SALIR?")
        msgBox.setWindowTitle("Salir")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)        
        returnValue = msgBox.exec_()
        if returnValue == QMessageBox.Ok:
            self.parent().show()
            self.close()
        else:
            print('Cancel')
        
    def abrirVentanaActualizar(self):
        if self.lineEditConsultaNumSocio.text() == "":
            VentanaAlta.messagebox(self, "Lo siento..", "INGRESE N° DE SOCIO!")
            print("NO IRÁS A ACTUALIZAR, EL CAMPO SOCIO ESTÁ VACIO")
        else:
            self.close()
            ventana_ac = VentanaActualizar(self)
            ventana_ac.show()

    def llevarID(self):
        idee = my_id
        return idee

    def ConsultaSocio(self):
        global my_id
        id_socio = self.lineEditConsultaNumSocio.text()
        apellido = self.lineEditAConsultaApellido.text()
        nombre = self.lineEditConsultaNombre.text()
        my_id = id_socio
        print("Consulta ID: ",my_id)
        
        query_socio = "SELECT * FROM socios WHERE id='%s' OR apellido='%s' OR nombre='%s'" %(id_socio, apellido, nombre)
        resul_socio = Run_query(query_socio)

        if resul_socio == ():
            VentanaAlta.messagebox(self, "Lo siento..", "NO EXISTE EL SOCIO!")
            print("NO EXISTE EL SOCIO")      

        self.tableWidgetConsulSocio.setRowCount(0)

        for fila_num, fila_dato in enumerate(resul_socio):
            self.tableWidgetConsulSocio.insertRow(fila_num)
            for colum_num, dato in enumerate(fila_dato):
                self.tableWidgetConsulSocio.setItem(fila_num, colum_num, QtWidgets.QTableWidgetItem(str(dato)))

        self.lineEditConsultaNumSocio.clear()
        self.lineEditAConsultaApellido.clear()
        self.lineEditConsultaNombre.clear()
        
    def VerSocios(self):
        query_all = "SELECT * FROM socios"
        resul = Run_query(query_all)
        self.tableWidgetConsulSociosAll.setRowCount(0)

        for row_number, row_data in enumerate(resul):
            self.tableWidgetConsulSociosAll.insertRow(row_number)
            for colum_number, data in enumerate(row_data):
                self.tableWidgetConsulSociosAll.setItem(row_number, colum_number, QtWidgets.QTableWidgetItem(str(data)))

    def EliminarSocio(self):
            id_socio = self.lineEditConsultaNumSocio.text()
            query_borrar = "DELETE FROM socios WHERE id='%s'" %id_socio
            Run_query(query_borrar)
            if(query_borrar):
                VentanaAlta.messagebox(self, "OK!.", "EL SOCIO HA SI DO BORRADO!")
                print("SOCIO BORRADO CON EXITO!")

    def ConfirmaEliminar(self):
        id_socio = self.lineEditConsultaNumSocio.text()
        if id_socio == '':
            VentanaAlta.messagebox(self, "Ingrese Socio.", "EL CAMPO ESTÁ VACÍO")
        else:
            confi = QMessageBox()
            confi.setIcon(QMessageBox.Information)
            confi.setText("ELIMINAR SOCIO?")
            confi.setWindowTitle("Confirme ..")
            confi.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retorno = confi.exec_()
            if retorno == QMessageBox.Ok:
                VentanaConsulta.EliminarSocio(self)
                self.lineEditConsultaNumSocio.clear()
                print('OK Clicked')
            else:
                print('Cancel')
        
########################################## ACTUALIZAR SOCIO ###################################################
class VentanaActualizar(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaActualizar, self).__init__(parent)
        loadUi('actualiza.ui', self)

        self.lineEditActualizaDNI.setValidator(QtGui.QDoubleValidator())
        self.lineEditActualizaCelular.setValidator(QtGui.QDoubleValidator())
        self.lineEditActualizaTelLinea.setValidator(QtGui.QDoubleValidator())

        self.lineEditActulizaNombre.setMaxLength(30)
        self.lineEditActualizaApellido.setMaxLength(30)
        self.lineEditActualizaDNI.setMaxLength(8)
        self.lineEditActualizaDomicilio.setMaxLength(30)
        self.lineEditActualizaLocalidad.setMaxLength(30)
        self.lineEditActualizaCelular.setMaxLength(18)
        self.lineEditActualizaTelLinea.setMaxLength(18)
        self.lineEditActualizaEmail.setMaxLength(40)
        self.lineEditActualizaRedSocial.setMaxLength(40)
        self.lineEditActualizaObservacion.setMaxLength(100)

        self.btnActualizaVolver.clicked.connect(self.abrirVentanaConsulta)
        self.btnActualizaSalir.clicked.connect(self.SalirActualizar)
        self.btnActualizaSocio.clicked.connect(self.ConfirmarActualizar)

        global id_ac
        try:
            id_ac = VentanaConsulta.llevarID(self) #ACÁ TENGO MI ID
            self.labelActualizaMostrarSocio.setText(id_ac)
            query = "SELECT * FROM socios WHERE id='%s'" %id_ac
            resul = Run_query(query)
            resul = str(resul).split("'")
            print(resul)
            print(str(resul[1]), resul[3], resul[4], resul[5], resul[7], resul[8], resul[9], resul[11], resul[13], resul[23])
            tel = str(resul[8]).split(",") # aca va coma
            tel2 = (str(tel).split(" ")) #acá va espacio
            print(tel2[2]) # va tel2[4]
            print(tel2[4])
            celu = str(tel2[2]).split("'")
            linea = str(tel2[4]).split("'")            
            dni = str(resul[4]).split(" ")
            
            self.lineEditActulizaNombre.setText(resul[3])
            self.lineEditActualizaApellido.setText(resul[1])
            self.lineEditActualizaDNI.setText(dni[1])
            self.lineEditActualizaDomicilio.setText(resul[5])
            self.lineEditActualizaLocalidad.setText(resul[7])
            self.lineEditActualizaCelular.setText(celu[0])
            self.lineEditActualizaTelLinea.setText(linea[0])
            self.lineEditActualizaEmail.setText(resul[9])
            self.lineEditActualizaRedSocial.setText(resul[11])
            self.lineEditActualizaObservacion.setText(resul[13])            

            print("Traje ID: ", id_ac)            
        except:           
            VentanaAlta.messagebox(self, "NO INGRESÓ SOCIO", "CONSULTE ANTES!")            
            VentanaActualizar.abrirVentanaConsulta(self)
            print("DEBERIA CONSULTAR PRIMERO")
            
    def SalirActualizar(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("DESEA SALIR?")
        msgBox.setWindowTitle("Salir")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)        
        returnValue = msgBox.exec_()
        if returnValue == QMessageBox.Ok:
            self.parent().show()
            self.close()
        else:
            print('Cancel')  

    def abrirVentanaConsulta(self):
        self.close()
        ventana_con = VentanaConsulta(self)
        ventana_con.show()

    def ActualizarSocio(self):
        id_ac
        apellido = self.lineEditActualizaApellido.text()
        nombre = self.lineEditActulizaNombre.text()
        DNI = self.lineEditActualizaDNI.text()
        domicilio = self.lineEditActualizaDomicilio.text()
        localidad = self.lineEditActualizaLocalidad.text()
        celular = self.lineEditActualizaCelular.text()
        telelinea = self.lineEditActualizaTelLinea.text()
        email = self.lineEditActualizaEmail.text()
        redsocial = self.lineEditActualizaRedSocial.text()
        observacion = self.lineEditActualizaObservacion.text()

        query_up = "UPDATE socios SET apellido='%s', nombre='%s', DNI='%s', domicilio='%s', localidad='%s', celular='%s', telelinea='%s', email='%s', redsocial='%s', observacion='%s' WHERE id='%s'" %(apellido, nombre, DNI, domicilio, localidad, celular, telelinea, email, redsocial, observacion, id_ac)
        Run_query(query_up)
        print(query_up)

        query_ver = "SELECT * FROM socios WHERE id='%s'" %id_ac
        resul_ver = Run_query(query_ver)
        print(resul_ver)
        self.tableWidgetActualizaSocio.setRowCount(0)

        for fila_num, fila_dato in enumerate(resul_ver):
            self.tableWidgetActualizaSocio.insertRow(fila_num)
            for colum_num, dato in enumerate(fila_dato):
                self.tableWidgetActualizaSocio.setItem(fila_num, colum_num, QtWidgets.QTableWidgetItem(str(dato)))

        if(query_up):
            VentanaAlta.messagebox(self, "OK!.", "SOCIO ACTUALIZADO!")
            print("SOCIO ACTUALIZADO!!")

    def ConfirmarActualizar(self):
        if self.lineEditActualizaApellido.text() == '' or self.lineEditActulizaNombre.text() == '':
            VentanaAlta.messagebox(self, "Apellido y Nombre:", "DATOS INCOMPLETOS!")
        else:
            confi = QMessageBox()
            confi.setIcon(QMessageBox.Information)
            confi.setText("ACTUALIZAR INFORMACIÓN?")
            confi.setWindowTitle("Confirme..")
            confi.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retorno = confi.exec_()
            if retorno == QMessageBox.Ok:
                VentanaActualizar.ActualizarSocio(self)
                self.lineEditActualizaApellido.clear(), self.lineEditActulizaNombre.clear(),
                self.lineEditActualizaDNI.clear(), self.lineEditActualizaDomicilio.clear(),
                self.lineEditActualizaLocalidad.clear(), self.lineEditActualizaCelular.clear(),
                self.lineEditActualizaTelLinea.clear(), self.lineEditActualizaEmail.clear(),
                self.lineEditActualizaRedSocial.clear(), self.lineEditActualizaObservacion.clear(),
                self.labelActualizaMostrarSocio.clear(),
                id_ac = ''
                print('OK Clicked')
            else:
                print('Cancel')
            
############################################# ACERCA DE ########################################################
class VentanaAcercade(QMainWindow):
    def __init__(self, parent=None):
        super(VentanaAcercade, self).__init__(parent)
        loadUi('acercad.ui', self)


app = QApplication(sys.argv)
main = VentanaPrincipal()
main.show()
sys.exit(app.exec_())