from tkinter import *
from PIL import Image


def genData(data):

    newd = []
    for i in data:
        newd.append(format(ord(i), "08b"))
    return newd


def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [
            value
            for value in imdata.__next__()[:3]
            + imdata.__next__()[:3]
            + imdata.__next__()[:3]
        ]
        for j in range(0, 8):  # Pixel value should be made odd for 1 and even for 0
            if datalist[i][j] == "0" and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == "1" and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[
                        j
                    ] += 1  # Eighth pixel of every set tells whether to stop ot read further.0 means keep reading; 1 means the message is over.
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def stegoimage(newimg, data):

    w = newimg.size[0]
    (x, y) = (0, 0)
    print(newimg.getdata())

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)  # Putting modified pixels in the new image
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1


def generateKey(string, key):
    key = list(key)
    if len(string) == len(key):
        return key
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def cipherText(string, key):

    cipher_text = []
    for i in range(len(string)):
        if ord(string[i]) == 32:
            cipher_text.append(chr(32))
        else:
            x = (ord(string[i]) + ord(key[i])) % 26
            x += ord("A")
            cipher_text.append(chr(x))
    return "".join(cipher_text)


def call_encode():

    input_image_name = input_image_entry.get()
    info = input_data.get().upper()

    new_image_name = input_image_name + ".png"
    new_image = Image.open(new_image_name, "r")

    keyword = "INDIA"
    key = generateKey(info, keyword)
    data = cipherText(info, key)

    if len(data) == 0:
        raise ValueError("Data is empty")

    copy_image = new_image.copy()
    stegoimage(copy_image, data)
    copy_image.save(new_image_name, str(new_image_name.split(".")[1].upper()))


root = Tk()
root.geometry("500x200")
root.title("Sender")

input_image_label = Label(root, text="Enter the name of image:")
input_image_label.place(x=0, y=20)

data_label = Label(root, text="Enter data to be encoded:")
data_label.place(x=0, y=40)

input_image_entry = Entry(root)
input_image_entry.place(x=300, y=20)

input_data = Entry(root)
input_data.place(x=300, y=40)

Buttontop = Button(root, text="Proceed", command=call_encode)
Buttontop.place(x=210, y=120)

mainloop()
