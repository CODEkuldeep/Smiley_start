import cv2

def detect_smile(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    smiles = smile_cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=20)

    if len(smiles) > 0:
        # Assume biggest smile = strongest
        largest_smile = max(smiles, key=lambda s: s[2] * s[3])
        x, y, w, h = largest_smile
        smile_area = w * h
        total_area = img.shape[0] * img.shape[1]
        smile_percent = (smile_area / total_area) * 100
        return True, round(smile_percent, 2)
    return False, 0.0
