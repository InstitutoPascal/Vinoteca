# -*- coding: utf-8 -*-

def index():
    titulo = T(' Administración de XXXXXXXX' )
    grid = SQLFORM.grid(db.bodega, deletable = False, csv = False)
    return locals()

##################################################################################
######## verificar luego como se utilizaria esto #################################
######## onvalidation=None, oncreate=None, onupdate=True,ondelete=None, ##########

def myonvalidation(form):
    print "In onvalidation callback"
    print form.vars
    form.errors= True  #this prevents the submission from completing

    #...or to add messages to specific elements on the form
    form.errors.first_name = "Do not name your child after prominent deities"
    form.errors.last_name = "Last names must start with a letter"
    response.flash = "I don't like your submission"

def myoncreate(form):
    print 'create!'
    print form.vars

def myonupdate(form):
    print 'update!'
    print form.vars

def myondelete(table, id):
    print 'delete!'
    print table, id
