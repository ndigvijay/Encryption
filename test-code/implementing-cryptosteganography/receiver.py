from tkinter import *
from PIL import Image


def generateKey(string, key):

    key = list(key)
    if len(string) == len(key):
        return key
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def originalText(cipher_text, key):

    orig_text = []
    for i in range(len(cipher_text)):
        if ord(cipher_text[i]) == 32:
            orig_text.append(chr(32))
        else:
            x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
            x += ord("A")
            orig_text.append(chr(x))
    return "".join(orig_text)


def decode(image_name):

    new_name = image_name + ".png"
    image = Image.open(new_name, "r")

    data = ""
    imgdata = iter(image.getdata())
    while True:
        pixels = [
            value
            for value in imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
        ]

        # for the string of binary data
        binstr = ""

        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += "0"
            else:
                binstr += "1"

        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data


def password():

    username = str(uname_entry.get())
    password = str(pass_entry.get())
    verify_entry.delete(0, END)
    if username == "admin" and password == "123":
        verify_entry.insert(0, "successful")
        return True
    else:
        verify_entry.insert(0, "Unsuccessful")
        return False


def main():

    if password():

        def proceed1():

            image_name = t4.get()
            string = str(decode(image_name))

            def proceed2():

                keyword = keyword_entry.get()
                key = generateKey(string, keyword)
                Pt = originalText(string, key)

                l7 = Label(root, text="Original/Decrypted Text:")
                l7.place(x=00, y=120)

                t6 = Entry(root)
                t6.place(x=200, y=120)

                t6.delete(0, END)
                t6.insert(0, str(Pt))

            keyword_label = Label(root, text="Enter the decryption keyword:")
            keyword_label.place(x=0, y=100)

            keyword_entry = Entry(root, show="*", width=10)
            keyword_entry.place(x=200, y=100)

            b3 = Button(root, text="Process key", command=proceed2)
            b3.place(x=400, y=100)

        l4 = Label(root, text="Enter the name of image:")
        l4.place(x=0, y=80)

        t4 = Entry(root)
        t4.place(x=200, y=80)

        b2 = Button(root, text="Process image", command=proceed1)
        b2.place(x=400, y=80)


root = Tk()
root.geometry("500x200")
root.title("Receiver")

uname_label = Label(root, text="Enter the username:")
uname_label.place(x=0, y=20)

uname_entry = Entry(root)
uname_entry.place(x=200, y=20)

pass_label = Label(root, text="Enter the password:")
pass_label.place(x=0, y=40)

pass_entry = Entry(root, show="*", width=10)
pass_entry.place(x=200, y=40)

verify_label = Label(root, text="Verification")
verify_label.place(x=0, y=60)

verify_but = Button(root, text="Verify", command=main)
verify_but.place(x=400, y=60)

verify_entry = Entry(root)
verify_entry.place(x=200, y=60)

mainloop()
