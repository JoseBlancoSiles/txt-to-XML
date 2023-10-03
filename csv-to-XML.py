import pandas as pd

def TXTtoXML(inputfile, outputfile):
  if not inputfile.lower().endswith('.txt'):
    print('Expected a TXT File')
    return 0
  if not outputfile.lower().endswith('.xml'):
    print('Expected an XML file')
    return 0

  try:
    df = pd.read_csv(inputfile, sep=' ', header=None, encoding='iso-8859-1')
  except FileNotFoundError as err:
    print(f'ERROR {err}')
    return 0

  entireop = '<parking>\n'
  
  for _, row in df.iterrows():
    num_cliente = row[0]
    entireop += f'    <cliente num_cliente="{num_cliente}">\n'
    entireop += f'        <nif>{row[1]}</nif>\n'
    entireop += f'        <nombre>{row[2]}</nombre>\n'
    entireop += f'        <apellidos>{row[3]}</apellidos>\n'
    
    marca = row[5]
    entireop += f'        <coche marca="{marca}">\n'
    entireop += f'            <modelo>{row[6]}</modelo>\n' # Preguntar a Alberto si el order importa tal y como sale en el PDF.
    entireop += f'            <color>{row[7]}</color>\n'
    entireop += f'            <matricula>{row[4]}</matricula>\n'
    entireop += f'            <bola>{row[8]}</bola>\n'
    entireop += '        </coche>\n'
    
    entireop += f'        <fecha_alta>{row[9]}</fecha_alta>\n'
    entireop += f'        <fecha_baja>{row[10]}</fecha_baja>\n'
    entireop += '    </cliente>\n'

  entireop += '</parking>'
  
  with open(outputfile, 'w') as f:
    f.write(entireop)

import xml.etree.ElementTree as ET

def XMLtoTXT(inputfile, outputfile, encoding='iso-8859-1'):
  try:
    tree = ET.parse(inputfile)
    root = tree.getroot()
  except FileNotFoundError as err:
    print(f'ERROR {err}')
    return 0

  with open(outputfile, 'w', encoding='iso-8859-1') as f:
    for cliente in root.findall('cliente'):
      num_cliente = cliente.get('num_cliente')
      nif = cliente.find('nif').text
      nombre = cliente.find('nombre').text
      apellidos = cliente.find('apellidos').text

      coche = cliente.find('coche')
      marca = coche.get('marca')
      modelo = coche.find('modelo').text
      color = coche.find('color').text
      matricula = coche.find('matricula').text
      bola = coche.find('bola').text

      fecha_alta = cliente.find('fecha_alta').text
      fecha_baja = cliente.find('fecha_baja').text

      f.write(f'{num_cliente} {nif} {nombre}{apellidos} {matricula} {modelo} {color} {bola} {fecha_alta} {fecha_baja}\n')


if __name__ == "__main__":
  print('\n****************')
  print('Menú de opciones')
  print('****************\n')
  while True:
    print('1.- Cnvertir de TXT a XML')
    print('2.- Convertir de XML a TXT')
    print('0.- Salir\n')
    option = input('Selecciona una opción: ')
    
    if option == '1':
      TXTtoXML('ClientesParking.txt', 'ClientesParking.xml')
      print('XML creado a partir del txt')
      
    elif option == '2':
      XMLtoTXT('ClientesParking.xml', 'ClientesParking_new.txt')
      print('txt creado a partir del XML')
      
    elif option == '0':
      print('saliendo del programa')
      break
    
    else:
      print('\nOpción no valida, por favor introduce una opción indicada en el menú:\n')
    

# def addRecordToXML(inputfile, outputfile, new_record):
#     try:
#         tree = ET.parse(inputfile)
#         root = tree.getroot()
#     except FileNotFoundError as err:
#         print(f'ERROR {err}')
#         return 0

#     # Create a new "cliente" element
#     new_cliente = ET.Element('cliente')

#     # Add attributes and sub-elements for the new record
#     for key, value in new_record.items():
#         if key == 'coche':
#             coche = ET.SubElement(new_cliente, 'coche')
#             for sub_key, sub_value in value.items():
#                 ET.SubElement(coche, sub_key).text = sub_value
#         else:
#             new_cliente.set(key, value)

#     # Append the new "cliente" element to the root
#     root.append(new_cliente)

#     # Write the updated XML to the output file
#     tree.write(outputfile)


# new_record = {}
# new_record['num_cliente'] = input('Número de cliente: ')
# new_record['nif'] = input('NIF: ')
# new_record['nombre'] = input('Nombre: ')
# new_record['apellidos'] = input('Apellidos: ')
# new_record['coche'] = {
#     'marca': input('Marca del coche: '),
#     'modelo': input('Modelo del coche: '),
#     'color': input('Color del coche: '),
#     'matricula': input('Matrícula del coche: '),
#     'bola': input('Bola del coche: ')
# }
# new_record['fecha_alta'] = input('Fecha de alta: ')
# new_record['fecha_baja'] = input('Fecha de baja: ')

# addRecordToXML('ClientesParking.xml', 'ClientesParking_updated.xml', new_record)

    
