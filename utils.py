from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import time
import json
import os




#set Global Variables
lang_en = 'en-US'

#xpath
xp_menu_fix = '//*[@id="WIN_0_304327070"]'
xp_menu_gdc = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[10]/a'
#cambiar para headless mode.
xp_menu_gdc_hm = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[6]/a'
xp_menu_gdc_nchange = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[10]/div/div[2]/a'
xp_menu_gdc_nchange_hm = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[6]/div/div[2]/a'

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
    def __init__(self, hide = False):
        data = load_data()
        self.hide = hide
        self.user = data['user']
        self.password = data['pass']
        self.remedy_url = data['remedy_url']
        self.rfc_id = ''
        self.resumen = data['resumen']
        self.notas = data['notas']
        self.delay = data['delay']
        self.data_basic = data['basic']
        self.data_categ = data['categorizacion']
        self.data_riesgo = data['riesgo']
        self.detalle_trabajo = data['detalle_trabajo']
        self.driver, self.language = login_remedy(hide,self.user,self.password,self.remedy_url,self.delay)        
        self.set_dic_date()
        
    def create_new_rfc(self):
        try:
            #abrir menu de aplicaciones
            app_menu = self.driver.find_element_by_id('WIN_0_304316340').click()
            #Si cuando abro el menu de aplicaciones, este viene vacío
            #shunk sigueinte
            #esta acción se ejecuta para llevar el foco al menu
            #en caso de que se pierda en otro objeto de la pagina.

            app_menu = self.driver.find_element_by_xpath(xp_menu_fix)

            ActionChains(self.driver).double_click(app_menu).perform()  
            #app_menu = driver.find_element_by_id('WIN_0_80098')

            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'WIN_0_80077')))
            print('myelem: ', myElem.text)

            #print("Page is ready!")

        except TimeoutException:
            print("Error al cargar la lista de opciones")
        
        
        if self.is_headlessmode():
            print('headlessmode detected')
        
        if self.language == lang_en:
            gestion_cambio_op = xp_menu_gdc_hm
            nuevo_cambio_op = xp_menu_gdc_nchange_hm
        else:
            gestion_cambio_op = xp_menu_gdc
            nuevo_cambio_op = xp_menu_gdc_nchange

        WebDriverWait(self.driver, self.delay)
        #seleccionar un nuevo cambio
        gdc_op = self.driver.find_element_by_xpath(gestion_cambio_op)
        change = self.driver.find_element_by_xpath(nuevo_cambio_op)

        ActionChains(self.driver).move_to_element(gdc_op).click(change).perform()
        valida_alert(self.driver,self.delay,'sesión al crear rfc')
        print('rfc created: ', self.driver.title)

    def search_rfc(self):
        return None

    def is_headlessmode(self):
        return self.driver.execute_script("return navigator.plugins.length == 0")

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
        
    def calendar_action(self):
        btn = self.driver.find_element_by_id('WIN_3_303924000')
        btn = btn.find_element_by_tag_name('a')
        btn.click()
        time.sleep(self.delay)
        cal = self.driver.find_element_by_id('popup303924000_3')
        days = cal.find_elements_by_class_name('weekday')
        print('days:', len(days))
        days[15].click()
        time.sleep(self.delay)
        self.driver.find_elements_by_tag_name('button')[0].click()
        time.sleep(self.delay)
        cal_txt = self.driver.find_element_by_id('arid_WIN_3_303924000').get_attribute('value')
        print(cal_txt)

      
    def setting_data_mobile(self):
        try:
            self.set_grupo_coordinador()
            #set opciones data 
            print('grupo coordinador elegido')
            self.choose_op(self.data_basic)
            print('opciones básicas elegidas')
            #set txt
            self.complete_txt(dic_txt)
            print('data descriptiva de RFC ingresada')
            #seleccionar y completar tab de fechas
            self.sel_fecha_sistema()
            self.complete_txt(dic_date_init)
            self.complete_txt(dic_date_end)
            print('fechas de tab fechas ingresadas')
            #seleccionar y completar tab de categorizacion
            self.sel_categorizacion()
            self.choose_op(self.data_categ)
            print('data de categorización ingresada')
            #seleccionar y completar popup de riesgos.
            #self.set_riesgo_values()
            #add detalle de trabajo
            self.sel_detalle()
            self.set_detalle_trabajo()
            
        except Exception as e:
            print(e)
            print('error: cerraremos sesión y pagina')
            self.cerrar_sesion()
            time.sleep(self.delay)
            self.close_page()
        
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
            print(op.get_attribute('outerHTML'))
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
            print('opciones: ', len(div))
            #print(div[op_id-1].get_attribute('outerHTML'))
            div[op_id-1].click()

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

    def save_rfc(self):
        save_id = 'WIN_3_1001'
        btn_ = self.driver.find_element_by_id(save_id)
        btn_.click()
        
        time.sleep(self.delay * 3)
        if self.print_error_txt():
            return False
        else:
            return self.valida_save_rfc()
            
    def valida_save_rfc(self):
        nu_rfc = self.get_rfc_number()
        if nu_rfc == self.rfc_id:
            print(nu_rfc, self.rfc_id,' : error al guardar RFC.')
            return False
        else:
            print(nu_rfc, self.rfc_id, ' :: RFC Guardado OK')
            return True

    def save_riesgo(self):
        save_id = 'WIN_0_300994900'
        self.driver.find_element_by_id(save_id).click()

    def set_riesgo_values(self):
        print('here')
        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        original_wind=self.driver.current_window_handle
        assert len(self.driver.window_handles) == 1
        #WIN_3_303900300
        #reg_img_301346600
        #WIN_3_301346600
        btn = self.driver.\
           find_element_by_id('WIN_3_301346600')
        print(btn.get_attribute('value'))
        print(btn.get_attribute('outerHTML'))
        #btn.send_keys(Keys.CONTROL + 't')
        btn.click()
        #self.driver.execute_script("document.getElementById('WIN_3_301346600').click()")
        time.sleep(self.delay)
        
        all_handles=self.driver.window_handles
        print(len(all_handles))
        print(all_handles)
        for handle in all_handles:
            if handle !=original_wind:
                print(handle)
                window_after = self.driver.switch_to.window(handle)
                print(window_after.title)
                self.driver.switch_to.window(window_after)
                self.choose_op(self.data_riesgo)
                self.save_riesgo()
                self.driver.switch_to.window(original_wind)
                

        # original_wind = self.driver.current_window_handle
        # assert len(self.driver.window_handles) == 1
        # self.driver.\
        #     find_element_by_id('WIN_3_301346600').click()
        # time.sleep(self.delay)
        # print(len(self.driver.window_handles))
        # window_after = self.driver.window_handles[1]
        # self.driver.switch_to.window(window_after)
        # self.choose_op(self.data_riesgo)
        # self.save_riesgo()
        # self.driver.switch_to.window(original_wind)

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
        self.driver.find_element_by_id('WIN_0_300000044').click()
        self.aceptar_save_session_alert()
        print('cierre sesión ok: page title >', self.driver.title)
        

    def close_page(self):
        self.driver.close()

    def sel_tipo_trabajo(self,op):
        try:
            self.driver.find_element_by_id('WIN_4_304247210')\
                .find_element_by_tag_name('a').click()
                # /html/body/div[3]/div[2]/table/tbody/tr[14]/td[1]
                # /html/body/div[3]/div[2]/table/tbody/tr[14]/td[1]
                # /html/body/div[3]/div[2]/table/tbody/tr[14]/td[1]
                # /html/body/div[4]/div[2]/table/tbody/tr[14]/td[1]
            txt = self.get_txt('arid_WIN_4_304247210')
            print(txt)
        except Exception as e:
            print('error al seleccionar tipo trabajo')
            print(e)

    def set_detalle_trabajo(self):
        trabajos = self.detalle_trabajo
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
            print('se detecta alert')
            self.driver.switch_to.frame(iframe[1])
            #presionar aceptar
            self.driver.\
                find_element_by_id('PopupMsgFooter').\
                find_elements_by_class_name('PopupBtn')[0].click()
            #switch al contentedor
            self.driver.switch_to.default_content()
            time.sleep(self.delay)
        else:
            print('no se encontró alert.')

    

    def upload_file(self, url_file):
        try:
            time.sleep(self.delay)
            self.driver.find_element_by_id('reg_img_304247100').click()
            #cambiar de iframe
            iframe = self.driver.find_elements_by_tag_name('iframe')
            self.driver.switch_to.frame(iframe[1])
            self.set_txt('PopupAttInput',url_file)
            #presionar aceptar
            self.driver.\
                find_element_by_id('PopupAttFooter').\
                find_elements_by_class_name('PopupBtn')[0].click()
            time.sleep(self.delay * 2)
            #switch al contentedor
            self.driver.switch_to.default_content()
            print('upload file ok')
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
                    time.sleep(self.delay)
                else:
                    print('file upload problem')
            #btn agregar
            self.driver.find_element_by_id('WIN_3_304247110').click()
            print('add detalle trabajo ok')
        except Exception as e:
            print('error al agregar detalle trabajo')
            print(e)
            return False
        

def valida_alert(driver, delay, message = 'default'):
    alert_ap = True
    #verifica si aparece un alert con la sesión tomada y si aparece más de una vez
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
        print("no encontró error")
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


def login_remedy(hide=False,user='',password='',remedy_url='',delay=0):
    #set the nav
    
    chrome_options = set_chrome_options(hide)
    op=None
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", options=chrome_options)
    language = driver.execute_script("return window.navigator.userLanguage || window.navigator.language")
    
    print('lang:', language)
    #driver.set_window_size(1920, 1080)
    #driver.manage().window().maximize()
    driver.get(remedy_url)
    #valida que se haya cargado la página.
    #TODO: agregar flujo de error.

    if valida_load_page(driver, delay) == False:
        print("Error al cargar página de remedy")
        return False

    #abrir sesión en Remedy
    print('ingresando datos de login. user: ' + user)
    user = driver.find_element_by_id('username-id').send_keys(user)
    password = driver.find_element_by_id('pwd-id').send_keys(password)
    #elem = driver.find_element_by_xpath(xp_login_submit)
    driver.find_element_by_xpath(".//input[@name='login' and @type='button']").click()


    #verifica si aparece un alert con la sesión tomada y si aparece más de una vez
    if valida_alert(driver, delay, 'otra sesión') == False:
        return False
    
    print('continua a validación de promt')
    if valida_prompt(driver, delay) == False:
        return False

    print('validacion de error finalizada')
    #verifica que el error de la sesión tomada, aparezca como promtext

    print('Usuario con sesión, en página: ', driver.title)
    return driver, language

def validate_file(url_file):
        try:
            size = os.path.getsize(url_file) 
            print('Size of file is', size, 'bytes')
        except OSError as e:
            print(e)
            return False
        return True

def load_data():
    with open('config.json', 'r') as j:
        data = json.load(j)
        return data

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

    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'es'})
    #options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    return chrome_options