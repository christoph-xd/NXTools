import math

werkzeugachsen_vektor = [0, 0, 1]
rundachse_b = [0, 1, 0]
rundachse_c = [0, 0, 1]

# Berechne den Winkel zwischen dem Werkzeugachsenvektor und der Rundachse B
cos_b = (
    werkzeugachsen_vektor[0] * rundachse_b[0]
    + werkzeugachsen_vektor[1] * rundachse_b[1]
    + werkzeugachsen_vektor[2] * rundachse_b[2]
)
sin_b = math.sqrt(1 - cos_b**2)
winkel_b = math.degrees(math.atan2(sin_b, cos_b))

# Berechne den Winkel zwischen dem Werkzeugachsenvektor und der Rundachse C
cos_c = (
    werkzeugachsen_vektor[0] * rundachse_c[0]
    + werkzeugachsen_vektor[1] * rundachse_c[1]
    + werkzeugachsen_vektor[2] * rundachse_c[2]
)
sin_c = math.sqrt(1 - cos_c**2)
winkel_c = math.degrees(math.atan2(sin_c, cos_c))

# Gib die Ergebnisse aus
print(f"Winkel zwischen Werkzeugachsenvektor und Rundachse B: {winkel_b} Grad")
print(f"Winkel zwischen Werkzeugachsenvektor und Rundachse C: {winkel_c} Grad")
