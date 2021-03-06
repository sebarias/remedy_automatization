from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path 
from datetime import date, timedelta
import time
import json
import os

#set Global Variables
lang_en = 'en-US'


#xpath
xp_menu_fix = '//*[@id="WIN_0_304327070"]'

#cambiar para headless mode.
xp_menu_gdc_hm = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[6]/a'
xp_menu_gdc_nchange = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[10]/div/div[2]/a'
xp_menu_gdc_schange = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[10]/div/div[3]/a'

xp_menu_gdc_nchange_hm = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[6]/div/div[2]/a'
xp_menu_gdc_schange_hm = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[6]/div/div[3]/a'

#IDs
id_appmenu = 'WIN_0_304316340'
id_appmenu_op_to_validate = 'WIN_0_80077'
id_rfc_txtare = 'arid_WIN_3_1000000182'


resumen_txt = 'cambio rfc'
notas_txt = 'cambio_rfc_notas'

dic_txt = {}
dic_txt['arid_WIN_3_1000000000'] = resumen_txt
dic_txt['arid_WIN_3_1000000151'] = notas_txt
dic_txt['arid_WIN_3_303924000'] = None

dic_date_init = {}
dic_date_init['arid_WIN_3_1000000350'] = None
dic_date_init['arid_WIN_3_1000000348'] = None
dic_date_init['arid_WIN_3_1000000349'] = None

dic_date_end = {}
dic_date_end['arid_WIN_3_1000000362'] = None
dic_date_end['arid_WIN_3_1000000364'] = None
dic_date_end['arid_WIN_3_1000000363'] = None

dic_tab = {}
dic_tab['categorizacion'] = 2
dic_tab['fecha_sistema'] = 5
dic_tab['detalle'] = 1

class RFC():
    xp_menu_gdc = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[10]/a'
    
    hide : bool
    user : str
    password : str
    remedy_url : str
    rfc_id : str
    driver : None
    languague : None
    delay : int
    basic_filename : str


    def __init__(self, hide = False, filename = None, rfc = None):
        """
        metodo de inicializaci??n de RFC. 
        por defecto busca la informaci??n de inicio en el archivo config.json
        """
        data = load_data()
        self.hide = hide
        self.user = data['user']
        self.password = data['pass']
        self.remedy_url = data['remedy_url']
        self.delay = data['delay']
        self.rfc_id = ''
        self.basic_filename = data['basic_filename']
        self.rfc_id = rfc
        self.detalle_trabajo_filename = data['detalle_trabajo_filename']
        self.categorizacion_filename = data['categorizacion_filename']
        
    
    def open_menu(self):
        try:
            #abrir menu de aplicaciones
            app_menu = self.driver.find_element_by_id('WIN_0_304316340').click()
            #Si cuando abro el menu de aplicaciones, este viene vac??o
            #shunk sigueinte
            #esta acci??n se ejecuta para llevar el foco al menu
            #en caso de que se pierda en otro objeto de la pagina.

            app_menu = self.driver.find_element_by_xpath(xp_menu_fix)

            ActionChains(self.driver).double_click(app_menu).perform()  
            #app_menu = driver.find_element_by_id('WIN_0_80098')

            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'WIN_0_80077')))
            print('myelem: ', myElem.text)

            #print("Page is ready!")

        except TimeoutException:
            print("Error al cargar la lista de opciones")
            return False
        return True

    def select_opcion_gdc(self, opcion='new'):

        if opcion == 'new':
            op_hm = xp_menu_gdc_nchange_hm
            op = xp_menu_gdc_nchange
        else:
            op_hm = xp_menu_gdc_schange_hm
            op = xp_menu_gdc_schange

        if self.is_headlessmode():
            print('headlessmode detected')
        
        if self.language == lang_en:
            self.xp_menu_gdc = xp_menu_gdc_hm
            op = op_hm

        WebDriverWait(self.driver, self.delay)
        #seleccionar un nuevo cambio
        gdc_op = self.driver.find_element_by_xpath(self.xp_menu_gdc)
        change = self.driver.find_element_by_xpath(op)

        ActionChains(self.driver).move_to_element(gdc_op).click(change).perform()
        valida_alert(self.driver,self.delay,'sesi??n al crear/buscar rfc')
        print('rfc created/search: ', self.driver.title)
        return True

    def select_search_rfc(self):
        if self.open_menu():
            self.select_opcion_gdc('search')
        return None
    
    def create_new_rfc(self):
        if self.open_menu():
            return self.select_opcion_gdc()
            
        return None

    def create_new_basic_rfc(self, servicio="MIBANCO"):
        print('entrando a crear nuevo rfc')
        self.login_remedy() 
        if self.create_new_rfc() is not None:
            time.sleep(4)
            self.set_rfc_id()
            data = load_data(self.basic_filename)
            #set resumen
            if data is not None:
                try:
                    data_basic = data['data_basic']
                    date_data = data['date_data']
                    riesgo_data = data['riesgo']
                    elecciones_basicas = data['elecciones_basicas']
                    self.complete_txt(data_basic)
                    self.set_grupo_coordinador()
                    servicio_dic = data['servicios'][servicio]
                    elecciones_basicas['servicio'] = servicio_dic
                    self.choose_op(elecciones_basicas)
                    self.set_riesgo_values(riesgo_data)
                    self.sel_fecha_sistema()
                    self.complete_txt(date_data)
                    
                    self.save_rfc()
                    return True
                except Exception as e:
                    print(e)
                    print('error: al crear nuevo RFC')
                    return False
                finally:
                    self.close_sesion()
                    print('goodbye')
        else:
            return False

    def search_rfc(self):
        try:
            rfc_found = False
            self.login_remedy()
            self.select_search_rfc()
            time.sleep(2)
            
            print('rfc: ',self.rfc_id)
            
            #coloca RFC id
            self.driver.find_element_by_id('arid_WIN_3_1000000182').clear()
            self.set_txt('arid_WIN_3_1000000182', self.rfc_id)
            #bton buscar
            elm = self.driver.find_elements_by_link_text('Buscar')
            print(len(elm))
            #self.driver.find_element_by_class_name('searchsavechanges').click() #searchsavechanges
            elm[0].click()
            time.sleep(2)
            result_box = self.driver.find_element_by_id('WIN_3_1020')
            if result_box is not None:
                #print(result_box.get_attribute('outerHTML'))
                results = result_box.find_element_by_class_name('TableFtrR')
                if results.text is not "":
                    print("find text", results.text)
                    rfc_found = True
            return rfc_found
            
        except Exception as e:
            print('error al buscar rfc', e)
            return False
    def update_detalle_trabajo(self):
        try:
            if self.search_rfc():
                data = load_data(self.detalle_trabajo_filename)
                self.set_detalle_trabajo(data['detalle_trabajo'])
                print('trabajo actualizado')
                return True
        except Exception as e:
            print('error al actualizar el detalle de trabajo rfc', e)
            return False

        finally:
            self.close_sesion()
            print('goodbye!')

        return True

    def update_categorizacion(self):
        try:
            if self.search_rfc():
                data = load_data(self.categorizacion_filename)
                categorizacion = data['categorizacion']
                self.sel_categorizacion()
                self.choose_op(categorizacion)
                print('data de categorizaci??n ingresada')
                self.save_rfc(new=False)
                return True
            else:
                raise Exception('No se encontr?? RFC')
        except Exception as e:
            print('error al actualizar categorizacion', e)
            return False
        finally:
            self.close_sesion()
            print('goodbye!')

    def close_sesion(self, save=False):
        if save:
            time.sleep(2)
            self.save_rfc()
        time.sleep(2)
        self.cerrar_sesion()
        print('sesion cerrada')
        time.sleep(2)
        self.close_page()
        print('pagina cerrada')


    def is_headlessmode(self):
        return self.driver.execute_script("return navigator.plugins.length == 0")

    def save_riesgo(self):
        save_id = 'WIN_0_300994900'
        self.driver.find_element_by_id(save_id).click()

    def set_riesgo_values(self, data_riego):
        print('setting riesgo values')
        original_wind=self.driver.current_window_handle
        parent_han  = self.driver.window_handles[0]
        assert len(self.driver.window_handles) == 1
        btn = self.driver.\
           find_element_by_id('WIN_3_301346600')
        btn.click()
        
        WebDriverWait(self.driver, 5).until(EC.number_of_windows_to_be(2))
        all_handles=self.driver.window_handles
        print(len(all_handles))
        print(all_handles)
        new_han = [x for x in all_handles if x != parent_han][0]
        print(new_han)
        print(parent_han)
        self.driver.switch_to.window(new_han)
        
        WebDriverWait(self.driver, 5).until(EC.title_contains("Pregunta de riesgo de cambios"))
        print(self.driver.current_window_handle)
        self.choose_op(data_riego)
        self.save_riesgo()
        self.driver.switch_to.window(parent_han)
 
    
    def set_dic_date(self):
        date_ini = self.get_date_start()
        date_end = self.get_date_end()
        dic_txt['arid_WIN_3_303924000'] = date_ini
        for key in dic_date_init:
            dic_date_init[key] = date_ini
        for key in dic_date_end:
            dic_date_end[key] = date_end

    def get_date_add(self, dias):
        fecha = date.today() + timedelta(days=dias)
        if self.language == lang_en:
            #formato gringo
            fecha = fecha.strftime('%m/%d/%Y %H:%M:%S')
        else:
            fecha = fecha.strftime('%d/%m/%y %H:%M:%S')
        print(fecha)
        return fecha

    def get_date_start(self):
        return self.get_date_add(1)

    def get_date_end(self):
        return self.get_date_add(2)

    def set_rfc_id(self):
        self.rfc_id = self.get_rfc_number()
        print('RFC: ', self.rfc_id)

    def get_rfc_number(self):
        rfc = self.driver.find_element_by_id('arid_WIN_3_1000000182').get_attribute('value')
        return(rfc)
        
    def get_last_menu_outer_div(self):
        div = self.driver.find_elements_by_class_name('MenuOuter')[-1]
        return div

    def get_count_last_menu(self):
        print(len(self.driver.find_elements_by_class_name('MenuOuter')))
        return len(self.driver.find_elements_by_class_name('MenuOuter'))

    def set_grupo_coordinador(self):
        self.driver.find_element_by_id("WIN_3_1000003229").find_element_by_tag_name('a').click()
        time.sleep(self.delay)
        div_id = self.get_count_last_menu() + 2
        xp = '/html/body/div[{}]/div[2]/table/tbody/'.format(div_id)
        self.driver.find_element_by_xpath(xp + 'tr/td[1]').click()
        time.sleep(self.delay)

        div_id = self.get_count_last_menu() + 2
        xp = '/html/body/div[{}]/div[2]/table/tbody/'.format(div_id)
        self.driver.find_element_by_xpath(xp + 'tr[16]/td[1]').click()
        time.sleep(self.delay)

        div_id = self.get_count_last_menu() + 2
        xp = '/html/body/div[{}]/div[2]/table/tbody/'.format(div_id)
        self.driver.find_element_by_xpath(xp + 'tr[1]/td[1]').click()
        grup_coor = self.driver.find_element_by_id('arid_WIN_3_1000003229').get_attribute('value')
        print(grup_coor)


    def scroll_down(self, t):
        for i in range(0,t):
            self.driver.find_elements_by_class_name('MenuScrollDown')[-1].click()

    def get_data_combo(self,dic):
        element_id = dic['id']
        print(element_id)
        
        div = self.get_div_by_id(element_id)
        coords = self.for_div(div)
        print(coords)
        print('exportando data de coordinadores a json')
        write_data(coords)
        return coords

    def get_div_by_id(self,id, is_service=False):
        """
        obtiene un div a partir del id del elemento que lo continene.
        especial para sacar data de combos.
        """
        op = self.driver.find_element_by_id(id)
        #print(op.get_attribute('outerHTML'))
        op = op.find_element_by_tag_name('a')
        op = op.click()
        time.sleep(self.delay)
        if is_service:
            self.scroll_down(60)
        #print('opciones: ', len(self.driver.find_elements_by_class_name('MenuOuter')))
        #print(self.driver.find_elements_by_class_name('MenuOuter').get_attribute('outerHTML'))
        time.sleep(self.delay)
        div = self.driver.find_elements_by_class_name('MenuOuter')[-1]
        div = div.\
            find_elements_by_class_name('MenuTableRow')
        return div

    def choose_op(self, dic):
        for key in dic:
            element_id = dic[key]['id']
            op_id = dic[key]['op_id']
            op_name = dic[key]['op_name']

            if 'service' in dic[key]:
                is_service = dic[key]['service']
            else:
                is_service = False

            print(element_id, " ", op_name)
            op = self.driver.find_element_by_id(element_id)
            #print(op.get_attribute('outerHTML'))
            op = op.find_element_by_tag_name('a')
            op = op.click()
            time.sleep(self.delay)
            if is_service:
                self.scroll_down(150)
            #print('opciones: ', len(self.driver.find_elements_by_class_name('MenuOuter')))
            #print(self.driver.find_elements_by_class_name('MenuOuter').get_attribute('outerHTML'))
            time.sleep(self.delay)
            div = self.driver.find_elements_by_class_name('MenuOuter')[-1]
            div = div.\
                find_elements_by_class_name('MenuTableRow')
            
            print('opciones: ', len(div))
            #print(div[op_id-1].get_attribute('outerHTML'))
            div[op_id-1].click()
        return div

    def for_div(self,div):
        arr = []
        for i, val in enumerate(div):
            coords = {}
            coords['id'] = i
            coords['name'] = val.find_element_by_class_name('MenuEntryName').text
            
            arr.append(coords)
        return arr

    def set_txt(self, txt_id, txt_value):
        txt = self.driver.find_element_by_id(txt_id)
        txt.clear()
        txt.send_keys(txt_value)
        print('text ingresado: ',txt.get_attribute('value'))

    def get_txt(self, txt_id):
        self.driver.find_element_by_id(txt_id).get_attribute('value')

    def complete_txt(self, dic):
        for key in dic:
            self.set_txt(key, dic[key])

    def select_tab(self, tab_id):
        self.driver.find_elements_by_class_name('Tab')[tab_id].click()

    def sel_categorizacion(self):
        self.select_tab(dic_tab['categorizacion'])

    def sel_fecha_sistema(self):
        self.select_tab(dic_tab['fecha_sistema'])

    def sel_detalle(self):
        self.select_tab(dic_tab['detalle'])

    def save_rfc(self, new=True):
        try:
            if new:
                save_id = 'WIN_3_1001'
            else:
                save_id = 'WIN_3_1003'
            btn_ = self.driver.find_element_by_id(save_id)
            #btn_ = self.driver.find_element_by_class_name('searchsavechanges')
            btn_.click()
        except Exception as e:
            print('error al guardar rfc: ', e)
        
        time.sleep(self.delay)
        if self.print_error_txt():
            return False
        return True


    def print_error_txt(self):
        div_err = self.driver.find_element_by_id('PromptBar')
        print(div_err.get_attribute('outerHTML'))
        try:
            pr = self.driver.find_element_by_class_name('prompttext')
            print(pr.text)
            return True
        except (NoSuchElementException) as py_ex:
            print('no se encuentra elemento <<error>> en pagina')
            return False

    def cerrar_sesion(self):
        if self.language != 'en-US':
            self.driver.find_element_by_link_text('Cerrar sesi??n').click()
        else:
            self.driver.find_element_by_id('WIN_0_300000044').click()
        #self.driver.find_element_by_id('WIN_0_300000044').click()
        self.aceptar_save_session_alert()
        print('cierre sesi??n ok: page title >', self.driver.title)
        

    def close_page(self):
        self.driver.close()

    def sel_tipo_trabajo(self,op):
        try:
            self.driver.find_element_by_id('WIN_4_304247210')\
                .find_element_by_tag_name('a').click()
            txt = self.get_txt('arid_WIN_4_304247210')
            print(txt)
        except Exception as e:
            print('error al seleccionar tipo trabajo')
            print(e)

    def set_detalle_trabajo(self,detalle_trabajo):
        trabajos = detalle_trabajo
        for trabajo in trabajos:
            up_file = False
            url = None
            notas = trabajo['trabajo_data']['trabajo_notas']
            print('trabajo: ', trabajo)
            if trabajo['trabajo_data']['file'] == True:
                url = trabajo['trabajo_data']['url_file']
                up_file = True
                if 'detalle_tipo' not in trabajo['trabajo_data']:
                    tipo = 'default'
                else:
                    tipo = trabajo['trabajo_data']['detalle_tipo']
                
                print('tipo: ', tipo)
                
            self.add_detalle_trabajo(notas, up_file ,url)
                

    def aceptar_save_session_alert(self):
        """Se valida si aparece el alert que indica guardar antes de cerrar sesion"""
        iframe = self.driver.find_elements_by_tag_name('iframe')
        if len(iframe) > 1:
            print('se detecta alert', len(iframe), iframe)
            for i in iframe:
                print('switch a iframe:', i)
                self.driver.switch_to.frame(i)
                print('en iframe')
                #buscar div
                try:
                    popup = self.driver.\
                    find_element_by_id('PopupMsgFooter')
                except:
                    popup = None
                print('popup', popup)
                if popup is not None:
                    #click en popup
                    popup.\
                    find_elements_by_class_name('PopupBtn')[0].click()
                #switch al contentedor
                print('switch to default')
                self.driver.switch_to.default_content()
                time.sleep(self.delay)
            
        else:
            print('no se encontr?? alert.')

    

    def upload_file(self, url_file):
        try:
            time.sleep(self.delay)
            self.driver.find_element_by_id('reg_img_304247100').click()
            #cambiar de iframe
            iframe = self.driver.find_elements_by_tag_name('iframe')
            for ifr in iframe:
                print(ifr.get_attribute('outerHTML'))
                self.driver.switch_to.frame(ifr)
                try:
                    self.set_txt('PopupAttInput',url_file)
                    self.driver.\
                    find_element_by_id('PopupAttFooter').\
                    find_elements_by_class_name('PopupBtn')[0].click()
                    time.sleep(self.delay * 2)
                    #switch al contentedor
                    
                    print('upload file ok')
                    break
                except (NoSuchElementException) as ex:
                    print('en este iframe no est?? el popup')
                    #next
                finally:
                    self.driver.switch_to.default_content()
          
            return True
        except Exception as e:
            print('error al subir archivo')
            print(e) 
            return False
        

    def add_detalle_trabajo(self, nota, up_file=False, url_file = None):
        try:
            #add nota
            self.set_txt('arid_WIN_3_304247080', nota)
            #upload_file
            if up_file:
                if validate_file(url_file):
                    self.upload_file(url_file)
                    
                else:
                    print('file upload problem')
            #btn agregar
            time.sleep(self.delay)
            self.driver.find_element_by_id('WIN_3_304247110').click()
            print('add detalle trabajo ok')
            return True
        except Exception as e:
            print('error al agregar detalle trabajo')
            print(e)
            return False

    def login_remedy(self):
        #set the nav
        
        chrome_options = set_chrome_options(self.hide)
        PATH="/Users/sariasc/Projects/python/chromedriver"
        self.driver = webdriver.Remote("http://127.0.0.1:9515")
        #self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
        self.language = self.driver.execute_script("return window.navigator.userLanguage || window.navigator.language")
        
        print('lang:', self.language)
        self.driver.get(self.remedy_url)
        #valida que se haya cargado la p??gina.

        if valida_load_page(self.driver, self.delay) == False:
            print("Error al cargar p??gina de remedy")
            return False

        #abrir sesi??n en Remedy
        print('ingresando datos de login. user: ' + self.user)
        user_element = self.driver.find_element_by_id('username-id').send_keys(self.user)
        password_element = self.driver.find_element_by_id('pwd-id').send_keys(self.password)
        #elem = driver.find_element_by_xpath(xp_login_submit)
        self.driver.find_element_by_xpath(".//input[@name='login' and @type='button']").click()


        #verifica si aparece un alert con la sesi??n tomada y si aparece m??s de una vez
        if valida_alert(self.driver, self.delay, 'otra sesi??n') == False:
            return False
        
        print('continua a validaci??n de promt')
        if valida_prompt(self.driver, self.delay) == False:
            return False

        print('validacion de error finalizada')
        #verifica que el error de la sesi??n tomada, aparezca como promtext

        print('Usuario con sesi??n, en p??gina: ', self.driver.title)
        return True

    
        

def valida_alert(driver, delay, message = 'default'):
    alert_ap = True
    #verifica si aparece un alert con la sesi??n tomada y si aparece m??s de una vez
    while alert_ap:
        try:
            WebDriverWait(driver, delay).until(EC.alert_is_present(),
                                           message)
            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")

        except (NoAlertPresentException, TimeoutException) as py_ex:
            print("Alert not present")
            print (py_ex)
            print (py_ex.args)
            alert_ap = False
    return True


def valida_prompt(driver, delay):
   
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'prompttext')))
        print(driver.find_element_by_class_name('prompttext').text)
        #TODO cerrar sesion, y volver a entrar.
    except TimeoutException:
        print("no encontr?? error")
        return True
    
    return False

def valida_load_page(driver, delay):

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'controlBox')))
        print("Page is ready! : ", driver.title)
        return True
    except TimeoutException:
        print("Loading took too much time!")
        
    return False

def validate_file(url_file):
        try:
            size = os.path.getsize(url_file) 
            print('Size of file is', size, 'bytes')
        except OSError as e:
            print(e)
            return False
        return True

def load_data(filename = 'config.json'):
    with open(filename, 'r') as j:
        data = json.load(j)
        return data
def write_data(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
        print('data guardada en data.json')

def set_chrome_options(hide=False) -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    if hide:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2, "intl.accept_languages":'es'}
    #chrome_prefs["intl.accept_languages"] = {'es'}
    #chrome_options.experimental_options["prefs"] = chrome_prefs
    #chrome_options.binary_location = "/Users/sariasc/opt/anaconda3/lib/python3.7/site-packages/chromedriver"


    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'es'})
    #options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    return chrome_options