# Objetivo de converter valores de temperatura, Celsius para Fahrenheit e para Kelvin e vice-versa.
# Pegar a sigla e valor da medida escolhida e transformar para as outras medidas.

put_measure_abreviattion = input("Hello, put the measure abreviation(C for Celsius, F for Fahrenheit or K for Kelvin): \n")
put_measurement = int(input("Hello, put the desired temperature to convert: \n"))

if(put_measure_abreviattion == 'C'):
    F = 1.8 * put_measurement + 32
    K = put_measurement + 273
    print(f"Celsius to Fahrenheit is {F}")
    print(f"Celsius Kelvin is {K}")
elif(put_measure_abreviattion == 'F'):
    C = (put_measurement - 32) * .5556
    K = C + 273
    print(f"Fahrenheit to Celsius is {C}")
    print(f"Fahrenheit to Kelvin is {K}")
else:
    C = put_measurement - 273
    F = C * 1.8 + 32
    print(f"Kelvin to Fahrenheit is {F}")
    print(f"Kelvin to Celsius is {K}")