import utils
import time
headless = False
rfc = utils.RFC(headless)
time.sleep(3)
rfc.create_new_rfc()
time.sleep(1)
rfc.set_rfc_id()
#
rfc.setting_data_mobile()

time.sleep(1)
rfc.save_rfc()
time.sleep(1)
#rfc.set_riesgo_values()
time.sleep(2)
rfc.cerrar_sesion()
time.sleep(2)
rfc.close_page()