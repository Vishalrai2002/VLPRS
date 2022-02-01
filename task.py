from flask import Flask, render_template
import cv2
import pytesseract
import numpy as np
import os

path= 'C:/Users/Shambhu Jha/Desktop/DSA/project/vlprs/static'
app= Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
vehicles= []


cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
# states={"AN":"Andaman and Nicobar","AP":"Andhra Pradesh","AR":"Arunachal Pradesh","AS":"Assam","BR":"Bihar","CH":"Chandigarh","DN":"Dadra and Nagar Haveli","DD":"Daman and Diu","DL":"Delhi","GA":"Goa","GJ":"Gujarat",
# "HR":"Haryana","HP":"Himachal Pradesh","JK":"Jammu and Kashmir","KA":"Karnataka","KL":"Kerala","LD":"Lakshadweep","MP":"Madhya Pradesh","MH":"Maharashtra","MN":"Manipur","ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland","OD":"Odissa","PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan","SK":"Sikkim","TN":"TamilNadu","TR":"Tripura","UP":"Uttar Pradesh", "WB":"West Bengal","CG":"Chhattisgarh","TS":"Telangana","JH":"Jharkhand","UK":"Uttarakhand"}

def extract_num(img_name):
    img = cv2.imread(img_name) ## Reading Image
    # Converting into Gray
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    # Detecting plate
    nplate = cascade.detectMultiScale(gray,1.1,4)
    for (x,y,w,h) in nplate:
        # Crop a portion of plate
        a,b = (int(0.02*img.shape[0]), int(0.025*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b, :]
        # make image more darker to identify the LPR
        ## iMAGE PROCESSING
        kernel = np.ones((1, 1), np.uint8)
        plate = cv2.dilate(plate, kernel, iterations=1)
        plate = cv2.erode(plate, kernel, iterations=1)
        plate_gray = cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)
        (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)
        # Feed Image to OCR engine
        read = pytesseract.image_to_string(plate)
        # path = os.path.join(parent_dir, read)
        read = ''.join(e for e in read if e.isalnum())
        # os.mkdir(path)
        print(read)
        vehicles.append(read)
        stat = read[0:2]
        print(read)
        cv2.rectangle(img, (x,y), (x+w, y+h), (51,51,255), 2)
        cv2.rectangle(img, (x, y - 40), (x + w, y),(51,51,255) , -1)
        cv2.putText(img,read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        str= read+ ".jpg"
        # cv2.imshow('PLate',plate)
        # Save & display result image
        cv2.imwrite(os.path.join(path , str), plate)

    # cv2.imshow("Result", img)
    cv2.imwrite('result.jpg',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Let's make a function call
extract_num('./t30.jpeg')

# print("Success")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<vehID>")
def veh_details(vehID):
    return render_template("details.html", plate=vehID)
    



if __name__== "__main__":
    app.run(debug=True)
