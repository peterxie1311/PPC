import imaplib
import email
import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime
import pandas as pd
import os   
import tkinter as tk
import threading
import numpy as nb 
from datetime import timedelta
from math import sin, cos, pi
from tkinter import filedialog
import matplotlib.pyplot as plt



#----------------------------filled dataframes --------------------------------------


def ppcCheck(op52,in32,wp01c):

    #fillednannostock = om25d.fillna('')
    filledop52 = op52.fillna('')
    filledin32 = in32.fillna('')
    filledwp01c = wp01c.fillna('')

    consolidations=filledin32[filledin32['ident'].str.contains('PICK_MOVE')]
    consolidations = consolidations.drop_duplicates(subset=['tu Ident'])

    print('------------------------------SO FAR WE DO NOT CHECK FOR AIO PPC-----------------------------')



    consolPallets=[]

    for index, row in consolidations.iterrows():
        if not row['tu Ident'].startswith('3'):

            consolPallets.append([row['tu Ident'],row['rouName']])
            consolPallets.append([row['tuIdentTo'],row['rouName']])



    tu=[]
    rou=[]
    fbr=[]
    restpalOwn=[]
    restpal=[]
    notMax=[]
    revoked=[]
    invest=[]
    







    #--------------------- consol pallet check -----------------

    with open("PPCReasons.txt", "w") as correctPPC:
        with open("investigationPPC.txt", "w") as investigation:


            outputPPC = ''
            investigationPPC=''
            for i in consolPallets:

                focusop52 = filledop52[filledop52['pallet *'] == i[0]]
                # print(f'THIS IS BUNDLE FOCUS op52{focusop52['bundle *']}')
                routeop52 = filledop52[filledop52['route ident *'] == i[1]]
                bundleop52 = routeop52[routeop52['bundle *'].isin(focusop52['bundle *'].unique())]
                routewp01c = filledwp01c[filledwp01c['route ident']== i[1]]
                focuswp01c = filledwp01c[filledwp01c['wo tu ident']== i[0]]


                tu.append(str(i[0]))
                rou.append(str(i[1]))
                
                

                if 'MAXFILL' not in str(focusop52['PPC profile key *']) and 'SEPARATED' not in str(focusop52['PPC profile key *']) and 'UPSTACK' not in str(focusop52['PPC profile key *'])  :
                    outputPPC +=  f'\n\ntu: {i[0]} route: {i[1]} is of profile: {focusop52['PPC profile key *'].to_string(index=False)} so it is not considered in this analysis'
                    notMax.append(1)
                    fbr.append(0)
                    restpalOwn.append(0)
                    restpal.append(0)
                    revoked.append(0)
                    invest.append(0)



                elif focusop52['work station *'].str.contains('FBR').any():
                    outputPPC += f'\n\ntu: {i[0]} (FBR) is of DISPSTRAT FBR ppc'    
                    fbr.append(1) 
                    notMax.append(0)
                    restpalOwn.append(0)
                    restpal.append(0)
                    revoked.append(0)
                    invest.append(0)


                elif len(bundleop52) == 1:
                    outputPPC +=  f'\n\ntu: {i[0]} route: {i[1]} bundle:{focusop52['bundle *'].to_string(index=False)} (REST PALLET) own bundle'
                    restpalOwn.append(1)
                    notMax.append(0)
                    fbr.append(0)
                    restpal.append(0)
                    revoked.append(0)
                    invest.append(0)


                elif (bundleop52['fill level *'] > 25).all() and (bundleop52['ppcCalcDate *'] == bundleop52['ppcCalcDate *'].iloc[0]).all():
                    outputPPC += f'\n\ntu: {i[0]} route: {i[1]} bundle: {focusop52['bundle *'].to_string(index=False)} (REST PALLET) pallets in this bundle have a high fillgrade and was calculated at the same time'
                    restpal.append(1)
                    notMax.append(0)
                    fbr.append(0)
                    restpalOwn.append(0)
                    revoked.append(0)
                    invest.append(0)


                elif routewp01c['wo tu ident'].str.contains(i[0]).any():
                    #if focuswp01c['com press state'].str.contains('REVOKED').any():
                    investigationPPC += f'\n\nTU: {i[0]} WO State: {focuswp01c['wo state'].to_string(index=False)} has upstack revoked'
                    revoked.append(1)
                    notMax.append(0)
                    fbr.append(0)
                    restpalOwn.append(0)
                    restpal.append(0)
                    invest.append(0)
                    

                else:
                    investigationPPC+= f'\n\nTree Path -> is maxfill -> not rest pallet -> not upstack -> TU: {i[0]} Route: {i[1]}'
                    invest.append(1)
                    notMax.append(0)
                    fbr.append(0)
                    restpalOwn.append(0)
                    restpal.append(0)
                    revoked.append(0)






                #check if max fill
                
                #check for op52 bundle rest pallet

                #output += f'\n {i[0]}'

            
            correctPPC.write(outputPPC)
            investigation.write(investigationPPC)






    rows=[tu,rou,fbr,restpalOwn,restpal,notMax,revoked,invest]
    pie=[sum(fbr),sum(restpalOwn),sum(restpal),sum(notMax),sum(revoked),sum(invest)]





    columns = ['TU', 'Rou Ref', 'FBR','Own Bundle','RestPal','Unused Profile','Revoked','Investigate']
    columns1 = ['FBR','Own Bundle','RestPal','Unused Profile','Revoked','Investigate']

    transposed_rows = list(zip(*rows))


    print(f'tu: {len(tu)}, rou: {len(rou)} , fbr: {sum(fbr)} , ownbundle {sum(restpalOwn)} , restpal: {sum(restpal)} , notmax {sum(notMax)} , revoked: {sum(revoked)} , invest : {sum(invest)}')
    
    df = pd.DataFrame(transposed_rows, columns=columns)
    print(tu)
    for element in tu:
        print(type(element))

    plt.figure(figsize=(6, 6))
    plt.pie(pie, labels=columns1, autopct='%1.1f%%', startangle=90)
    plt.ylabel('')  # Remove the ylabel
    plt.title('Pie Chart of Categories')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.show()

    df.to_excel('stusucks.xlsx', index=False)

#--------------------------------------------------






   #print(f'this is your route table \n\n {route}')

#----------------------------GUI--------------------------------------



things = []





def op52():
    global op52File
    file_path = filedialog.askopenfilename()
    if file_path:
        op52File=file_path
        print(file_path)

def in32():
    global in32File
    file_path = filedialog.askopenfilename()
    if file_path:
        in32File=file_path

def wp01c():
    global wp01cFile
    file_path = filedialog.askopenfilename()
    if file_path:
        wp01cFile=file_path

def confirmFiles():
    global op52File, in32File, wp01cFile , op52, in32,wp01c
    if 'csv' in op52File and 'csv' in in32File and 'csv' in wp01cFile:
        confirm.set('Confirmed!')
        op52=pd.read_csv(op52File, sep=',', skiprows=1, skipinitialspace=True, encoding='ISO-8859-1')
        in32=pd.read_csv(in32File, sep=',', skiprows=1, skipinitialspace=True, encoding='ISO-8859-1')
        wp01c=pd.read_csv(wp01cFile, sep=',', skiprows=1, skipinitialspace=True, encoding='ISO-8859-1')

    else:
        confirm.set('Not Confirmed!')
        print(f'{wp01cFile} , {in32File} , {op52File}')










root = tk.Tk()
root.title("PPC Analysis")


op52File = ''
in32File=''
wp01cFile=''

op52 
in32
wp01c 
confirm=tk.StringVar()


label = tk.Label(root, text="PPC Analysis \n Please Include ALL files \n MUST be CSV")
label.pack()

confirmLabel = tk.Label(root, textvariable=confirm)
confirmLabel.pack()

bop52 = tk.Button(root, text="op52", command=op52)
bin32 = tk.Button(root, text="in32", command=in32)
bwp01c = tk.Button(root, text="wp01c", command=wp01c)
bcfiles = tk.Button(root, text="Confirm Files", command=confirmFiles)
bppc = tk.Button(root, text="PPC", command=lambda: ppcCheck(op52=op52,in32=in32,wp01c=wp01c))
bop52.pack(side=tk.LEFT)
bin32.pack(side=tk.LEFT)
bwp01c.pack(side=tk.LEFT)

bcfiles.pack(side=tk.LEFT)
bppc.pack(side=tk.LEFT)


root.mainloop()









   


   
   
   
   



