from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import sys
MAX_LENGTH_MESSAGE = 600
MAX_LENGTH_BITS = 4800

def string_to_bits(message):
    """
    Convert string to bits (as string).
    """
    # Convertir la chaîne en une séquence d'octets (encodage UTF-8 par défaut)
    bytes_data = message.encode()
    # Convertir chaque octet en sa représentation binaire
    binary_representation = [bin(byte)[2:].zfill(8) for byte in bytes_data]
    # Joindre les représentations binaires pour obtenir la chaîne binaire complète
    bits_string = ''.join(binary_representation)
    return bits_string


def bits_to_string(bits):
    """
    Convert bits to string
    """
    # Diviser la chaîne binaire en groupes de 8 bits
    chunks = [bits[i:i+8] for i in range(0, len(bits), 8)]
    # Convertir chaque groupe en un entier et ensuite en un caractère
    characters = [chr(int(chunk, 2)) for chunk in chunks]
    # Concaténer les caractères pour obtenir la chaîne d'origine
    result_string = ''.join(characters)
    return result_string
 

def write_message(img, message, composante):
    """
    Write a message in an image.
    """
    pixels = img.load()

    size = len(message)
    if  size > MAX_LENGTH_MESSAGE:
        raise ValueError("Message trop long pour être caché dans l'image")

    for _ in range(MAX_LENGTH_MESSAGE - size):
        message += ' '

    message_bits = string_to_bits(message)

    if img.height * img.width < len(message_bits):
        raise ValueError("Message trop long pour être caché dans l'image")

    bit_index = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            
            if composante == 'r':
                r = (r & 0b11111110) | int(message_bits[bit_index])
            if composante == 'b':
                b = (b & 0b11111110) | int(message_bits[bit_index])

            pixels[x, y] = r, g, b

            bit_index += 1
            if bit_index == len(message_bits):
                return
            
            

def read_message(img, composante):
    """
    Read a message hide inside an image.
    """
    pixels = img.load()
    message_bits = []
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            
            if composante == 'r':
                message_bits.append(str(r & 1))
            if composante == 'b':
                message_bits.append(str(b & 1))
                
            
            if len(message_bits) == MAX_LENGTH_BITS:
                message = bits_to_string(''.join(message_bits))                     
                finalMessage = message.rstrip()
                return finalMessage
            
#### QUESTION 2 START 
def generate_key_pair(private_key_filename='private_key.pem', public_key_filename='public_key.pem'):
    try:
        # Essayer de charger les clés à partir des fichiers existants
        with open(private_key_filename, 'r') as private_file, open(public_key_filename, 'r') as public_file:
            private_key = private_file.read()
            public_key = public_file.read()
    except FileNotFoundError:
        # Si les fichiers n'existent pas, générer une nouvelle paire de clés
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        # Écrire les clés dans les fichiers
        with open(private_key_filename, 'wb') as private_file, open(public_key_filename, 'wb') as public_file:
            private_file.write(private_key)
            public_file.write(public_key)

    return private_key, public_key

def sign_image(private_key, image_path):
    key = RSA.import_key(private_key)
    
    # Lire les données binaires de l'image
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Calculer le hachage des données de l'image
    h = SHA256.new(image_data)

    # Signer les données hachées
    signature = pkcs1_15.new(key).sign(h)
    return signature

def verify_image_signature(public_key, image_path, signature):
    key = RSA.import_key(public_key)

    # Lire les données binaires de l'image
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Calculer le hachage des données de l'image
    h = SHA256.new(image_data)

    # Vérifier la signature avec la clé publique
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False


def sign_data(private_key, data):
    key = RSA.import_key(private_key)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return signature

def verify_signature(public_key, data, signature):
    key = RSA.import_key(public_key)
    h = SHA256.new(data.encode())
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False


### QUESTION 2 END

### QUESTION 3 START

def add_text(img, text, x, y, font_size, font_color=(255, 255, 255)):
    """
    Ajoute du texte à une image.

    Args:
        img (PIL.Image.Image): L'image sur laquelle ajouter le texte.
        text (str): Le texte à ajouter.
        x (int): La coordonnée x du coin supérieur gauche du texte.
        y (int): La coordonnée y du coin supérieur gauche du texte.
        font_size (int, optional): La taille de la police. Par défaut, 12.
        font_color (tuple, optional): La couleur du texte en format RGB. Par défaut, blanc (255, 255, 255).
        font_path (str, optional): Le chemin vers le fichier de police TrueType (ttf). Si non spécifié, utilise une police par défaut.

    Returns:
        PIL.Image.Image: L'image avec le texte ajouté.
    """
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=font_size)
    draw.text((x, y), text, font=font, fill=font_color)

    return img

### QUESTION 3 END



### QUESTION 4 START
def signData(data_to_sign):
    private_key, public_key = generate_key_pair()
    return sign_data(private_key, data_to_sign)

def hideData(img_input_file_path, img_output_file_path, input_message, composante):
    img = Image.open(img_input_file_path)   
    write_message(img, input_message, composante)
    img.save(img_output_file_path)
    
def generateDiploma(img_file_path, output_file_name, num_INE, nom, prenom, moyenne, id_diplome):
    input_message = nom + ' ' + prenom + ' ' + moyenne + '/20'
    data = id_diplome + ' ' + num_INE + ' ' + input_message

    # 1. sign data
    signature = signData(data)

    # # 2. generate image
    img = Image.open(img_file_path) 
    img = img.convert("RGB")
    img = add_text(img, input_message, 600, 565, 80, (0, 0, 0))
    
    # seprarate signature in 4 lines
    signature = signature.hex()
    part_length = len(signature) // 4
    parts = [signature[i:i + part_length] for i in range(0, len(signature), part_length)]

    img = add_text(img, parts[0], 450, 1335, 15, (0, 0, 0))
    img = add_text(img, parts[1], 450, 1355, 15, (0, 0, 0))
    img = add_text(img, parts[2], 450, 1375, 15, (0, 0, 0))
    img = add_text(img, parts[3], 450, 1395, 15, (0, 0, 0))
    
    img.save(output_file_name) 

    # # 3. add data    
    hideData(output_file_name, output_file_name, data, 'r')
    hideData(output_file_name, output_file_name, signature, 'b')
    
    print("Diploma generated at " + output_file_name)


def verifyDiploma(img_path):
    img = Image.open(img_path) 
    print("\n INFORMATION DE L'ELEVE : \n")
    message = read_message(img, 'r')
    print(message)
    signature = read_message(img, 'b')
    # trasnform signature in bytes
    signature = bytes.fromhex(signature)
    private_key, public_key = generate_key_pair()
    if verify_signature(public_key, message, signature): 
        print("La signature est valide")
    else :
        print("La signature n'est pas valide")
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""
            python main.py --generate ./diplome.png ./diplome_output.png 095462187AP CHAVANCE Remi 15.5 1548A9G8ER
            to generate a diploma
            or 
            python main.py --verify ./diplome_output.png'
            to verify the diploma
        """)
        sys.exit()
    
    if sys.argv[1] == '--generate':
        if len(sys.argv) != 9:
            print('Not enough arguments, try :')
            print('python main.py --generate ./diplome.png ./diplome_output.png 095462187AP CHAVANCE Remi 16.5 1548A9G8ER')
            sys.exit()
        generateDiploma(
            img_file_path=sys.argv[2],
            output_file_name=sys.argv[3],
            num_INE=sys.argv[4],
            nom=sys.argv[5],
            prenom=sys.argv[6],
            moyenne=sys.argv[7],
            id_diplome=sys.argv[8]
        )
    elif sys.argv[1] == '--verify':
        if len(sys.argv) != 3:
            print('Not enough arguments, try :')
            print('python main.py --verify ./diplome_output.png')
            sys.exit()
        verifyDiploma(img_path=sys.argv[2])
    else:
        print("""
            python main.py --generate ./diplome.png ./diplome_output.png 095462187AP CHAVANCE Remi 16.5 1548A9G8ER
            to generate a diploma
            or 
            python main.py --verify ./diplome_output.png'
            to verify the diploma
        """)