import utils
import time

def main():
    headless = True
    rfc = utils.RFC(headless)
    time.sleep(3)
    rfc.create_new_rfc()
    time.sleep(1)
    rfc.set_rfc_id()
    time.sleep(2)
    rfc.save_rfc()
    time.sleep(4)
    rfc.cerrar_sesion()
    time.sleep(2)
    rfc.close_page()

if __name__ == "__main__":
    main()