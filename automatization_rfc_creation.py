import utils
import time
headless = True
rfc = utils.RFC(headless)
time.sleep(3)
rfc.create_new_rfc()
#time.sleep(1)
rfc.set_rfc_id()
#
rfc.setting_data_mobile()
#rfc.set_grupo_coordinador()
time.sleep(2)
#rfc.calendar_action()
rfc.save_rfc()
time.sleep(1)
#rfc.set_riesgo_values()
#time.sleep(2)
rfc.add_nota(True, '/Users/sariasc/GonzaloBarra.png')
time.sleep(2)
rfc.cerrar_sesion()
time.sleep(2)
rfc.close_page()