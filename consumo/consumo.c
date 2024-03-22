
int main(){
    int km, litros, consumo;

    scanf("Quantos quilômetros foram percorridos: %d\n", &km);
    scanf("Quantos litros foram utilizados para percorrer a distância total: %d\n", &litros);

    consumo = km / litros;
    printf(consumo);
    return 0;
}