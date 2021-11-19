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

def main_2():
    headless = False
    rfc = utils.RFC(headless)
    time.sleep(3)
    if rfc.create_new_basic_rfc(servicio="miinversion"):
        print('create RFC ok')
        
    else:
        print('Problem to create RFC')

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

def main_update_categorizacion():
    rfc_id = 'CRQ000000205940'
    #rfc_id = 'CRQ000000505164'
    headless = False
    rfc = utils.RFC(headless, rfc = rfc_id)
    rfc.update_categorizacion()

def main_uploadfile_2():
    rfc_id = 'CRQ000000206371'
    #rfc_id = 'CRQ000000505164'
    headless = False
    rfc = utils.RFC(headless, rfc = rfc_id)
    rfc.update_detalle_trabajo()
    


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
    
    #rfc_id = 'CRQ000000205483'
    rfc_id = 'CRQ000000205940'
    headless = False
    rfc = utils.RFC(headless, rfc = rfc_id)
    time.sleep(3)
    if rfc.search_rfc():
        print("rfc encontrado")
    else: 
        print("rfc no encontrado")
    
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
    #main_search()
    main_2()
    #main_uploadfile_2()
    #main_update_categorizacion()