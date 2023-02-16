from PIL import Image

def encode_image(img, message):
    """
    Codificar un mensaje en una imagen

    :Parámetro img: El nombre del archivo de la imagen.
    :Parámetro message: El mensaje a ser codificado.
    :return: Un archivo de imágen que ya tiene codificado el mensje.
    """
    # Convierte el mensaje a binario
    binary_message = ''.join(format(ord(i), '08b') for i in message)

    # añade padding interno al mensaje binario
    padding = 8 - len(binary_message) % 8
    binary_message += '0' * padding

    #abre la imágen
    with Image.open(img) as image:
        #Obtiene los datos de la imagen
        image_data = image.load()

        #proceso de codificación de imágen
        binary_index = 0
        for row in range(image.height):# recorre el alto de la imagen
            for col in range(image.width): #recorre el ancho de la imagen
                r, g, b = image_data[col, row] 
                if binary_index < len(binary_message):
                    # Encode the message in the least significant bit
                    r = (r & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                if binary_index < len(binary_message):
                    g = (g & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                if binary_index < len(binary_message):
                    b = (b & ~1) | int(binary_message[binary_index])
                    binary_index += 1
                image_data[col, row] = (r, g, b)

        # Save the image
        image.save("encoded_" + img)

def decode_image(img):
    """Decode a message from an image.

    :param img: The input image file.
    :return: The decoded message.
    """
    # Open the image
    with Image.open(img) as image:
        # Get image data
        image_data = image.load()

        # Decode the message
        binary_message = ''
        for row in range(image.height):
            for col in range(image.width):
                r, g, b = image_data[col, row]
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)

        # Remove padding from binary message
        padding = binary_message.find('0' * 8)
        binary_message = binary_message[:padding]

        # Convert binary to message
        message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

        return message

# Example usage
message = "This is a secret message"
encode_image("image.jpg", message)
decoded_message = decode_image("encoded_image.jpg")
print(decoded_message)
