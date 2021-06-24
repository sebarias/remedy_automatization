import utils
import time
import sys

def main():
    headless = False
    rfc = utils.RFC(headless)
    time.sleep(3)
    rfc.create_new_rfc()
    time.sleep(1)
    rfc.set_rfc_id()
    time.sleep(2)
    rfc.setting_data_mobile()
    time.sleep(2)
    rfc.save_rfc()
    time.sleep(4)
    rfc.cerrar_sesion()
    time.sleep(2)
    rfc.close_page()

def main_uploadfile():
    headless = True
    rfc = utils.RFC(headless)
    time.sleep(3)
    rfc.create_new_rfc()
    time.sleep(1)
    rfc.set_rfc_id()
    time.sleep(2)
    rfc.set_detalle_trabajo()
    #rfc.save_rfc()
    #time.sleep(4)
    rfc.cerrar_sesion()
    time.sleep(2)
    rfc.close_page()

def main_without_save():
    headless = False
    rfc = utils.RFC(headless)
    time.sleep(3)
    rfc.create_new_rfc()
    time.sleep(1)
    rfc.set_rfc_id()
    time.sleep(2)
    #rfc.setting_data_mobile()
    time.sleep(2)
    rfc.set_detalle_trabajo()
    time.sleep(2)
    # rfc.save_rfc()
    # time.sleep(4)
    rfc.cerrar_sesion()
    time.sleep(2)
    rfc.close_page()

def main_search():
    print('ingrese RFC a buscar:')
    rfc_id = str(input())
    headless = False
    rfc = utils.RFC(headless)
    time.sleep(3)
    rfc.select_search_rfc()
    
    time.sleep(2)
    rfc.find_rfc(rfc_id)
    time.sleep(2)
    time.sleep(2)
    rfc.cerrar_sesion()
    time.sleep(2)
    rfc.close_page()

if __name__ == "__main__":
    print("Python version")
    print (sys.version)
    print("Version info.")
    print (sys.version_info)
    #main_uploadfile()
    #main_without_save()
    main_search()
    # main()