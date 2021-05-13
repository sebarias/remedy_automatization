import utils
import time

rfc = utils.RFC()
time.sleep(3)
rfc.create_new_rfc()
time.sleep(1)
rfc.set_rfc_id()
#
rfc.setting_data_mobile()
time.sleep(1)
#rfc.save_rfc()
time.sleep(1)
rfc.cerrar_sesion()
time.sleep(2)
rfc.close_page()