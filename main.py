from deepface import DeepFace


analyze = DeepFace.analyze("image.png", enforce_detection=False)

print(analyze)
