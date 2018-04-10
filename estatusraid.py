#!/usr/bin/python
import ctypes
import re
import os
import sys
import time

megaclipath='/opt/MegaRAID/MegaCli/MegaCli64'
telegramclipath='/home/lsvp/tg/bin/telegram-cli'

def getOutput(cmd):
    lines = []
    output = os.popen(cmd)
    for line in output:
        if not re.match(r'^$', line.strip()):
            lines.append(line.strip())
    return lines

def obtenTabla():

    '''cmd = '%s -adpCount -NoLog' % (megaclipath)
    output = getOutput(cmd)
    controllernumber = returnControllerNumber(output)
    '''
    controllernumber = 1
    controllerid = 0
    tabla = []
    status = 'Unknown'
    smart  = 'unknown'
    size = ''
    slot = 'Unknown'
    while controllerid < controllernumber:
        #cmd = '%s -PDList -a%d -NoLog' % (megaclipath, controllerid)
        cmd = 'cat /home/lsvp/salida1'
        output = getOutput(cmd)
        for line in output:
            if re.match(r'^Slot', line.strip()):
                slot = (line.split()[2] + ' ')
            if re.match(r'^Raw', line.strip()):
                size  = ('Size' + ' ' + line.split()[2])
            if re.match(r'^Firmware state', line.strip()):
                status = (line.split()[2].strip(','))
            expreg = re.compile(r'S\.M\.A\.R\.T', re.I)
            if not expreg.search(line.strip()) is None:
                smart = ('Alert: ' + line.split()[7])
                tabla.append([slot, str(controllerid), status, smart])
        controllerid += 1
    #for l in tabla:
    #    print ' '.join(l)
    return tabla


def tablaacadena(tabla):
    cad=''
    cad = cad + '*****************************************'+'\n'
    cad = cad + 'Slot\tCID\tStatus\tS.M.A.R.T' + '\n'
    cad = cad + '*****************************************'+'\n'
    for renglon in tabla:
        cad = cad + '\t'.join(renglon) + '\n'
    cad += '*****************************************'
    return cad


def checaestado(tabla):
    estado = 0
    mensaje = ''
    error = False
    for indice, renglon in enumerate(tabla):
        if renglon[2] not in ['Online', 'Unconfigured(good), Spun Up', 'Unconfigured(good), Spun down', 'JBOD',
                            'Hotspare, Spun Up', 'Hotspare, Spun down', 'Hotspare']:
            error = True
        if renglon[3] not in ['Alert: No']:
            error = True
            estado = 1
        if error:
            mensaje = 'Error en el disco en el Slot: %d Status %s S.M.A.R.T %s' %(int(renglon[0]), renglon[2], renglon [3])
            error = False
            estado = 1
    return estado, mensaje


def enviaestado(mensaje):
    '''
    cmd = '%s -R -e \"msg Jonathan_Alfaro %s\"' % (telegramclipath, mensaje)
    print cmd
    getOutput(cmd)'''
    pass


if __name__ == '__main__':
    '''
    try:
        root_or_admin = os.geteuid() == 0
    except AttributeError:
        root_or_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if not root_or_admin:
        print 'Este script necesita permisos de administrador'
        sys.exit(5)'''
    estado = 0
    while estado is 0:
        tabla = obtenTabla()
        estado, mensaje = checaestado(tabla)
        if estado != 0:
            enviaestado()
        time.sleep(10)
        print tablaacadena(tabla)