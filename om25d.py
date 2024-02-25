#--------------------GUI-----------------------------------------------------
#def open_file_dialog(report):
    # Open file dialog and get selected file path
#    file_path = filedialog.askopenfilename()
    # Display the selected file path
#    if file_path:
#        label.config(text="Selected file: " + file_path)
#        report = file_path



#    else:
#        label.config(text="No file selected")

# Create the Tkinter application window
#root = tk.Tk()
#root.title("PPC Analysis")

# Create a button to open the file dialog
#button = tk.Button(root, text="OP52", command=lambda: open_file_dialog(op52File))
#button.pack(pady=10)
#button = tk.Button(root, text="IN32", command=lambda: open_file_dialog(in32File))
#button.pack(pady=10)
#button = tk.Button(root, text="OM25d", command=lambda: open_file_dialog(om25dFile))
#button.pack(pady=10)

# Label to display selected file path
#label = tk.Label(root, text="")
#label.pack()

# Run the Tkinter event loop
#root.mainloop()


#--------------------GUI-----------------------------------------------------






# Filter the DataFrame to show only the rows with unique values in the specified column





#----------------------------data inspecion of om25d --------------------------------------



#print('--------------------------------data inspection of om25d-------------------------------------')

#nostock= fillednannostock[fillednannostock['reason Detail'].str.contains('no stock') | fillednannostock['reason Text'].str.contains('no stock') ]


#reason text we should look for 
#


#print(f'this is drop duplicates for User Name \n \n ')
'''
for t,i in fillednannostock.drop_duplicates(subset=['User Name org']).iterrows():
    if 'WMS' not in i['User Name org']:
        print(i['User Name org'])

'''

'''
LBS#LORALD03
LBS#LORALD01
LBS#LORALD02
LBS#LHRCV_MQORH
LBS#LORALD04
LBS#LORALD05
LBS#LORALD06
'''

#nostock = nostock.fillna(0)




#print('-----------------------------------data inspection of------------------------------------')

#nostock=fillednannostock[fillednannostock['reason Detail'].str.contains('no stock') | fillednannostock['reason Text'].str.contains('no stock')]






#reason text we should look for 
#


#print(f'this is drop duplicates for consolidations \n \n {consolidations.drop_duplicates(subset=['tu Ident'])}')



'''
no stock
no stock - repl problem
canceled by ppc
unknown reasonCode in LAQTYM
LBS-loral (default reason)
'''

#nostock = nostock.fillna(0)

#print('----------------------------------------------------------------------------')
#print(f'this is no stock {nostock}')
#print(f'this is drop duplicates for reason Detail \n \n {fillednannostock.drop_duplicates(subset=['reason Detail'])}')

'''
cancel from dialogue - no stock 
no stock 
vanished
CEREPL_ERR_WAIT_RECALC
in modul COST
in modul CPS
stock found is already allocated
stock found has qty zero
existing stock not matches
rest-case pallet 
location or rack blocked / out of order
tu not in tray area
channel not pick loc
stock found is blocked by qState
stock found has another um
expired stock
late inbound (<4h)
CEREPL_ERR_STOCK_NOT_FOUND
location wrong configured
LBS-loral (default reason)
'''


#print(unique_values)

print('----------------------------------------------------------------------------')

'''

user_name_org_substring = 'LBS'
reason_text_substrings = ['no stock', 'no stock - repl problem', 'canceled by ppc', 'unknown reasonCode in LAQTYM', 'LBS-loral (default reason)']
reason_detail_substrings = ['cancel from dialogue - no stock', 'no stock', 'vanished', 'CEREPL_ERR_WAIT_RECALC', 'in modul COST', 'in modul CPS', 'stock found is already allocated', 'stock found has qty zero', 'existing stock not matches', 'rest-case pallet', 'location or rack blocked / out of order', 'tu not in tray area', 'channel not pick loc', 'stock found is blocked by qState', 'stock found has another um', 'expired stock', 'late inbound (<4h)', 'CEREPL_ERR_STOCK_NOT_FOUND', 'location wrong configured', 'LBS-loral (default reason)']

filtered_om25d = om25d[(om25d['User Name org'].str.contains(user_name_org_substring)) |
                 (om25d['reason Text'].str.contains('|'.join(reason_text_substrings))) |
                 (om25d['reason Detail'].str.contains('|'.join(reason_detail_substrings)))]

'''




#print(f'THIS IS WHAT THE FILTERED SCRATCHES LOOKS LIKE \n\n{filtered_om25d}')


