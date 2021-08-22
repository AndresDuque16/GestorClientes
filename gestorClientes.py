from tkinter import *
from tkinter import messagebox
from tkinter import ttk #treeview
import sqlite3

root = Tk()
root.title('Libreta de Clientes')

conn = sqlite3.connect('gestorCliente.db') #coneccion a la base de datos
c = conn.cursor() #cursor para ejecutar consultas

#creación de base de datos
c.execute("""
        CREATE TABLE if not exists cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT NOT NULL,
        nombre TEXT NOT NULL,
        empresa TEXT NOT NULL
        );
    """)
#defincion de funciones

#funcion que renderiza los clientes
def render_clientes():
    rows = c.execute("SELECT * FROM cliente").fetchall() #consulta de clientes en la bd
    tree.delete(*tree.get_children())#elimina los elementos de la tabla y luego se insertan nuevamente

    for row in rows:
        tree.insert('',END, row[0], values=(row[1],row[2], row[3])) # el primer argumento es la tabla misma '',
        # en donde se agrega el registro en el final de la tabla END, el ID del registro row[0],
        # luego se indica los valores a insertar en values
    


#funcion que guarda los datos de nuevos clientes en la BD
def insertar(cliente):
    c.execute("""
            INSERT INTO cliente(cedula, nombre, empresa) VALUES (?,?,?)
            """, (cliente['cedula'], cliente['nombre'], cliente['empresa'])) #se crea una tupla
    conn.commit() #se compromete la consulta en la base de datos
    render_clientes() #para que actualice los clientes que se visualizan en la tabla
def new_cliente():
    #se define funcion
    def guardar():
        if not cedula.get(): #valida de que tenga un dato almacenado en el entry de cedula
            messagebox.showerror('Error', 'La cedula es obligatoria')
            return #corta la ejecucion de la funcion guardar
        if not nombre.get(): #valida de que tenga un dato almacenado en el entry de nombre
            messagebox.showerror('Error', 'El nombre es obligatorio')
            return #corta la ejecucion de la funcion guardar
        if not empresa.get(): #valida de que tenga un dato almacenado en el entry de nombre
            messagebox.showerror('Error', 'La empresa es obligatoria')
            return #corta la ejecucion de la funcion guardar

        #se crea un diccionario de cliente para almacenar los datos
        cliente = { 
        'cedula': cedula.get(),
        'nombre': nombre.get(),
        'empresa': empresa.get()
        }
        insertar(cliente) #funcion definida para almacenar el diccionario creado al guardar nuevo cliente
        top.destroy()#permite cerrar la ventana de nuevo cliente una vez insertado el cliente


    top = Toplevel()
    top.title('Nuevo Cliente')

    #creacion de los label
    lcedula = Label(top, text='Cedula')
    lcedula.grid(row=0, column=0)
    cedula = Entry(top, width=40)
    cedula.grid(row=0, column=1)

    lnombre = Label(top, text='Nombre')
    lnombre.grid(row=1, column=0)
    nombre = Entry(top, width=40)
    nombre.grid(row=1, column=1)

    lempresa = Label(top, text='Empresa')
    lempresa.grid(row=2, column=0)
    empresa = Entry(top, width=40)
    empresa.grid(row=2, column=1)

    #creacion de boton guardar
    guardar = Button(top, text='Guardar', command=guardar)
    guardar.grid(row=3, column=1)


    top.mainloop()

#FUNCION DE ELIMINAR CLIENTE
def del_cliente():
    id_cliente = tree.selection()[0]
    cliente = c.execute("SELECT * FROM cliente WHERE id = ?",(id_cliente, )).fetchone()
    respuesta = messagebox.askokcancel('Confirmación', '¿Estas seguro de querer eliminar el cliente ' + cliente[2] + '?') 
    #confirmacion
    if respuesta:
        c.execute("DELETE FROM cliente WHERE id = ?",(id_cliente, )) #eliminar el cliente en la base de datos
        conn.commit() #ejecutar en la bd la eliminacion
        render_clientes() #renderiza la tabla
    else:
        pass #pasa y no ejecuta nada



btn_new = Button(root, text='Nuevo Cliente', command=new_cliente)
btn_new.grid(row=0, column=0, padx=5,pady=5)

btn_del = Button(root, text='Eliminar Cliente', command=del_cliente)
btn_del.grid(row=0, column=1, padx=5,pady=5)

tree = ttk.Treeview(root) #representancion de informacion en forma jerarquica en una tabla
tree['columns'] =('Cedula', 'Nombre', 'Empresa')   #columnas
tree.column('#0', width=0, stretch=NO)# ES LA COLUMNA INICIAL PERO SE COLOCA STRETCH PARA QUE NO APARESCA y width de 0
tree.column('Cedula') #configuracion de los nombres que va a tener cada columna
tree.column('Nombre')#configuracion de los nombres que va a tener cada columna
tree.column('Empresa')#configuracion de los nombres que va a tener cada columna

tree.heading('Cedula', text='Cedula') #los textos de heading que van a tener las tablas
tree.heading('Nombre', text='Nombre')#los textos de heading que van a tener las tablas
tree.heading('Empresa', text='Empresa')#los textos de heading que van a tener las tablas
tree.grid(row=1, column=0, columnspan=2)



render_clientes() #con el objetivo de que actualice los clientes en la tabla
root.mainloop()


