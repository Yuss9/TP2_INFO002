from PIL import Image

MAX_LENGTH_MESSAGE = 500
MAX_LENGTH_BITS = 4000


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
 

def write_message(img, message):
    """
    Write a message in an image.
    """
    pixels = img.load()

    size = len(message)
    if  size > MAX_LENGTH_MESSAGE:
        raise ValueError("Message trop long pour être caché dans l'image")

    for i in range(MAX_LENGTH_MESSAGE - size):
        message += ' '

    message_bits = string_to_bits(message)

    if img.height * img.width < len(message_bits):
        raise ValueError("Message trop long pour être caché dans l'image")

    bit_index = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            r = (r & 0b11111110) | int(message_bits[bit_index])

            pixels[x, y] = r, g, b

            bit_index += 1
            if bit_index == len(message_bits):
                return

def read_message(img):
    """
    Read a message hide inside an image.
    """
    pixels = img.load()
    message_bits = []
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            message_bits.append(str(r & 1))
            if len(message_bits) == MAX_LENGTH_BITS:
                message = bits_to_string(''.join(message_bits))                     
                finalMessage = message.rstrip()
                return finalMessage


def invert_half(img):
    """
    Invert the second half of an image.
    """
    m = img.height // 2             # milieu de l'image
    pixels = img.load()             # tableau des pixels

    for y in range(m, img.height):
        for x in range(0, img.width):
            r, g, b = pixels[x, y]  # on récupère les composantes RGB du pixel (x,m)
            r = r ^ 0b11111111      # on les inverse bit à bit avec un XOR
            g = g ^ 0b11111111      # ...
            b = b ^ 0b11111111      # ...
            pixels[x, y] = r, g, b  # on remet les pixels inversés dans le tableau


def main(filename, output):
    img = Image.open(filename) 
      
    input_message = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
    consequat.  Duis aute irure dolor in reprehenderit in voluptate velit esse
    cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
    proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""  
    
    write_message(img, input_message)
    img.save(output)
    
    output_img = Image.open(output)    
    #len_bit = len(string_to_bits(input_message))
    message = read_message(output_img)
    
    print(message)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: {} image output".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])