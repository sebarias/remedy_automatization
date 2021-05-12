from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import time
import json


def get_date_add(dias):
    fecha = date.today() + timedelta(days=dias)
    fecha = fecha.strftime('%d/%m/%y %H:%M:%S')
    return fecha

def get_date_start():
    return get_date_add(1)

def get_date_end():
    return get_date_add(2)

#set Global Variables
#delay = 4

#USER = 'BCH_scarias'
#PASS = 'Banco05.'

#REMEDY_URL = 'https://sdserti.entel.cl/arsys/shared/login.jsp?/arsys'

#xpath
xp_menu_fix = '//*[@id="WIN_0_304327070"]'
xp_menu_gdc = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[10]/a'
xp_menu_gdc_nchange = '//*[@id="WIN_0_80077"]/fieldset/div/div/div/div[10]/div/div[2]/a'

#IDs
id_appmenu = 'WIN_0_304316340'
id_appmenu_op_to_validate = 'WIN_0_80077'
id_rfc_txtare = 'arid_WIN_3_1000000182'

tomorrow = date.today() + timedelta(days=1)
tomorrow = tomorrow.strftime('%d/%m/%y %H:%M:%S')

dic_basic = {}
#coordinador de cambio
dic_basic['WIN_3_1000003230'] = {'xp':1, 'div':False}
#servicio
dic_basic['WIN_3_303497300'] = {'xp':86, 'div':False, 'service':True}
#motivo
dic_basic['WIN_3_1000000294'] = {'xp':3, 'div':True}
#impacto
dic_basic['WIN_3_1000000163'] = {'xp':4, 'div':True}
#urgencia
dic_basic['WIN_3_1000000162'] = {'xp':4, 'div':True}

resumen_txt = 'cambio rfc'
notas_txt = 'cambio_rfc_notas'

dic_txt = {}
dic_txt['arid_WIN_3_1000000000'] = resumen_txt
dic_txt['arid_WIN_3_1000000151'] = notas_txt
dic_txt['arid_WIN_3_303924000'] = get_date_start()

dic_date = {}
dic_date['arid_WIN_3_1000000350'] = get_date_start()
dic_date['arid_WIN_3_1000000362'] = get_date_end()
dic_date['arid_WIN_3_1000000348'] = get_date_start()
dic_date['arid_WIN_3_1000000364'] = get_date_end()
dic_date['arid_WIN_3_1000000349'] = get_date_start()
dic_date['arid_WIN_3_1000000363'] = get_date_end()

dic_tab = {}
dic_tab['categorizacion'] = 2
dic_tab['fecha_sistema'] = 5
dic_tab['detalle'] = 1

dic_categ = {}

dic_categ['WIN_3_1000000063'] = {'xp':15,'div':False}
dic_categ['WIN_3_1000000064'] = {'xp':6,'div':False}
dic_categ['WIN_3_1000000065'] = {'xp':2,'div':False}
dic_categ['WIN_3_1000001270'] = {'xp':12,'div':False}
dic_categ['WIN_3_1000001271'] = {'xp':3,'div':False}
dic_categ['WIN_3_1000001272'] = {'xp':1,'div':False}
dic_categ['WIN_3_1000002268'] = {'xp':2,'div':False}

dic_riesgo = {}
dic_riesgo['WIN_0_300996200'] = {'xp':2,'div':False}
dic_riesgo['WIN_0_301019100'] = {'xp':1,'div':False}
dic_riesgo['WIN_0_301029000'] = {'xp':2,'div':False}

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
        print(type(self.data_basic))


        self.driver = login_remedy(hide,self.user,self.password,self.remedy_url,self.delay)
        
        
        
        
    def create_new_rfc(self):
        try:
            #abrir menu de aplicaciones
            app_menu = self.driver.find_element_by_id('WIN_0_304316340').click()
            #Si cuando abro el menu de aplicaciones, este viene vacío
            #shunk sigueinte
            #debo ejcutar este codigo. nose porque pero hace q funcione.

            app_menu = self.driver.find_element_by_xpath(xp_menu_fix)

            ActionChains(self.driver).double_click(app_menu).perform()  
            #app_menu = driver.find_element_by_id('WIN_0_80098')

            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.ID, 'WIN_0_80077')))
            #print('myelem: ', myElem.text)

            #print("Page is ready!")

        except TimeoutException:
            print("Error")


        WebDriverWait(self.driver, self.delay)
        #seleccionar un nuevo cambio
        gdc_op = self.driver.find_element_by_xpath(xp_menu_gdc)

        change = self.driver.find_element_by_xpath(xp_menu_gdc_nchange)

        ActionChains(self.driver).move_to_element(gdc_op).click(change).perform()

        print('rfc created')

    def set_rfc_id(self):
        self.rfc_id = self.driver.find_element_by_id('arid_WIN_3_1000000182').get_attribute('value')
        print(self.rfc_id)
        
      
    def setting_data_mobile(self):
        self.set_grupo_coordinador_2()
        #set opciones data 
        self.choose_op(self.data_basic)
        #set txt
        self.complete_txt(dic_txt)
        self.sel_fecha_sistema()
        self.complete_txt(dic_date)
        self.sel_categorizacion()
        #self.choose_op(dic_categ)
        self.choose_op(self.data_categ)
        self.set_riesgo_values()
        
    def get_last_menu_outer_div(self):
        div = self.driver.find_elements_by_class_name('MenuOuter')[-1]
        return div

    def get_count_last_menu(self):
        print(len(self.driver.find_elements_by_class_name('MenuOuter')))
        return len(self.driver.find_elements_by_class_name('MenuOuter'))

    def set_grupo_coordinador_2(self):
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
           
            self.driver.find_element_by_id(element_id).find_element_by_tag_name('a').click()
            time.sleep(1)
            if is_service:
                self.scroll_down(60)
            div = self.driver.find_elements_by_class_name('MenuOuter')[-1]
            div = div.\
                find_elements_by_class_name('MenuTableRow')[op_id-1].\
                    click()

    def set_txt(self, txt_id, txt_value):
        self.driver.find_element_by_id(txt_id).send_keys(txt_value)

    def complete_txt(self, dic):
        for key in dic:
            self.set_txt(key, dic[key])

    def select_tab(self, tab_id):
        self.driver.find_elements_by_class_name('Tab')[tab_id].click()

    def sel_categorizacion(self):
        self.select_tab(dic_tab['categorizacion'])

    def sel_fecha_sistema(self):
        self.select_tab(dic_tab['fecha_sistema'])

    def save_rfc(self):
        save_id = 'WIN_3_1001'
        self.driver.find_element_by_id(save_id).click()

    def save_riesgo(self):
        save_id = 'WIN_0_300994900'
        self.driver.find_element_by_id(save_id).click()

    def set_riesgo_values(self):
        original_wind = self.driver.current_window_handle
        assert len(self.driver.window_handles) == 1
        self.driver.\
            find_element_by_id('WIN_3_301346600').click()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)
        self.choose_op(self.data_riesgo)
        self.save_riesgo()
        self.driver.switch_to.window(original_wind)

    def print_error_txt(self):
        pr = self.driver.find_element_by_class_name('prompttext')
        pr.text

    def cerrar_sesion(self):
        self.driver.find_element_by_id('WIN_0_300000044').click()
        print('cierre sesión ok: page title >', self.driver.title)

    def close_page(self):
        self.driver.close()
        
    




def valida_alert(driver, delay):
    alert_ap = True
    #verifica si aparece un alert con la sesión tomada y si aparece más de una vez
    while alert_ap:
        try:
            WebDriverWait(driver, delay).until(EC.alert_is_present(),
                                           'El usuario está conectado actualmente desde otro equipo')

            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")

        except TimeoutException:
            print("no se encontró alert error")
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
        print("Page is ready!")
        return True
    except TimeoutException:
        print("Loading took too much time!")
        
    return False


def login_remedy(hide=False,user='',password='',remedy_url='',delay=0):
    #set the nav
    op=None
    if hide:
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=op)  
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
    driver.find_element_by_xpath(".//input[@value='Iniciar sesión' and @type='button']").click()
    #wait = WebDriverWait(driver, 10)
    #wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[@value='Submit' and @type='submit']"))).click()
    #elem.click()


    #verifica si aparece un alert con la sesión tomada y si aparece más de una vez
    if valida_alert(driver, delay) == False:
        return False
        

    print('continua a validación de promt')
    if valida_prompt(driver, delay) == False:
        return False

    print('validacion de error finalizada')
    #verifica que el error de la sesión tomada, aparezca como promtext

    print('Usuario con sesión, en página: ', driver.title)
    return driver


def load_data():
    with open('config.json', 'r') as j:
        data = json.load(j)
        return data