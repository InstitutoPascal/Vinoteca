# -*- coding: utf-8 -*-
def index():
    titulo = T(' Listado de noticias' )
    grid = SQLFORM.grid(db.noticia, deletable = False, editable=False, details=True, csv = False)
    return locals()

def oncreateNoticia(form):
    #print form.vars
    envioMail('noticia', form.vars.id)
    return True

def admin():
    titulo = T(' Administración de noticias' )
    grid = SQLFORM.grid(db.noticia, deletable = False, csv = True, oncreate=lambda form: oncreateNoticia(form) )
    return locals()

##################################################################################
######## verificar luego como se utilizaria esto #################################
######## onvalidation=None, oncreate=None, onupdate=True, ondelete=None, ##########

def myonvalidation(form):
    print "In onvalidation callback"
    print form.vars
    form.errors= True  #this prevents the submission from completing

def myoncreate(form):
    print 'create!'
    print form.vars

def myonupdate(form):
    print 'update!'
    print form.vars

def myondelete(table, id):
    print 'delete!'
    print table, id
