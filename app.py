from model.Conexion import Conexion
from view.Menu import Menu


def main():
    try:
        Menu().mostrar_menu()
    except RuntimeError as exc:
        print(f"Error de configuracion: {exc}")
    finally:
        Conexion.close()


if __name__ == "__main__":
    main()
