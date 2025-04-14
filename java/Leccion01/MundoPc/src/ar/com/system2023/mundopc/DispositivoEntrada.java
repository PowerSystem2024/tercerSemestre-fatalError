package ar.com.system2023.mundopc;

public class DispositivoEntrada {
    private String tipoEntrada;
    private String marca;
    
    public DispositivoEntrada(String entrada, String marca){
        this.tipoEntrada = entrada;
        this.marca = marca;   
    }

    public String getTipoEntrada() {
        return this.tipoEntrada; //ponemos el this. para mayor legibilidad
    }

    public void setTipoEntrada(String tipoEntrada) {
        this.tipoEntrada = tipoEntrada;
    }

    public String getMarca() {
        return this.marca; //ponemos el this. para mayor legibilidad        
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }

    @Override
    public String toString() {
        return "DispositivoEntrada{" + "tipoEntrada=" + tipoEntrada + ", marca=" + marca + '}';
    }
    
}
    