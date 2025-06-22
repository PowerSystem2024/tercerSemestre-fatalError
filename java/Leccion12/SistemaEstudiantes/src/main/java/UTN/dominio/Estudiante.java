package UTN.dominio;

public class Estudiante {
    private int idEstudiante;
    private String nombre;
    private String apellido;
    private String telefono;
    private String mail;

    public Estudiante() {} //constructor vacío

    public Estudiante(int idEstudiante){
        this.idEstudiante = idEstudiante;
    } //eliminar un estudiante

    public Estudiante(String nombre, String apellido, String telefono, String mail) {
        this.nombre = nombre;
        this.apellido = apellido;
        this.telefono = telefono;
        this.mail = mail;
    }//insertar estudiante

    public Estudiante(int idEstudiante, String nombre, String apellido, String telefono, String mail){
        this.idEstudiante = idEstudiante;
        this.nombre = nombre;
        this.apellido = apellido;
        this.telefono = telefono;
        this.mail = mail;
    } // modificar estudiante

    public int getIdEstudiante() {
        return idEstudiante;
    }

    public void setIdEstudiante(int idEstudiante) {
        this.idEstudiante = idEstudiante;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public void setApellido(String apellido) {
        this.apellido = apellido;
    }

    public String getTelefono() {
        return telefono;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    public String getMail() {
        return mail;
    }

    public void setMail(String mail) {
        this.mail = mail;
    }

    @Override
    public String toString() {
        return "Estudiante{" +
                "idEstudiante=" + idEstudiante +
                ", nombre='" + nombre + '\'' +
                ", apellido='" + apellido + '\'' +
                ", telefono='" + telefono + '\'' +
                ", mail='" + mail + '\'' +
                '}';
    }
}
