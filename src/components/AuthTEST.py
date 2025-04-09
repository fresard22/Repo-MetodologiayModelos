from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time  # Opcional, para pausas (mejor usar esperas explícitas)

# Datos de prueba (deberías obtenerlos de un lugar seguro o variables de entorno)
AUTH0_USERNAME = "nicole.navarro@alumnos.uach.cl"
AUTH0_PASSWORD = "123456"
TU_APLICACION_URL = "localhost:3000"
AUTH0_DOMAIN = "https://learner-model-gql.us.auth0.com"  # Dominio auth0
CODIGO_EJERCICIO = "pnc2b01"

def test_login_con_auth0():
    driver = webdriver.Firefox()  # O el navegador que prefieras

    try:
        driver.get(TU_APLICACION_URL)

        # 1. Hacer clic en el botón de "Iniciar sesión" de tu aplicación
        boton_iniciar_sesion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Login')]")) # Ajusta el localizador
        )
        boton_iniciar_sesion.click()

        # 2. Verificar la redirección a Auth0
        WebDriverWait(driver, 10).until(
            EC.url_contains(AUTH0_DOMAIN)
        )
        print(f"Redirigido a la página de Auth0: {driver.current_url}")

        # 3. Localizar e ingresar credenciales en la página de Auth0
        campo_usuario_auth0 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username")) # El ID puede variar
        )
        campo_usuario_auth0.send_keys(AUTH0_USERNAME)

        campo_contrasena_auth0 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password")) # El ID puede variar
        )
        campo_contrasena_auth0.send_keys(AUTH0_PASSWORD)

        # 4. Hacer clic en el botón de "Continuar" o "Iniciar sesión" de Auth0
        boton_login_auth0 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")) # El selector CSS puede variar
        )
        boton_login_auth0.click()

        # 5. Esperar la redirección de vuelta a tu aplicación
        WebDriverWait(driver, 15).until(
            EC.url_contains(TU_APLICACION_URL)
        )
        print(f"Redirigido de vuelta a la aplicación: {driver.current_url}")

        # 6. Verificar que el usuario está autenticado (ejemplo: buscar un elemento específico)
        try:
            elemento_usuario_logueado = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "p.chakra-text.css-1hqktoc"))
            )
            nombre_usuario = elemento_usuario_logueado.text
            print(f"Login exitoso: Nombre de usuario encontrado: {nombre_usuario}")

            # --- Flujo de Obtener y Cargar Ejercicio por Código ---

            # 1. Apretar el enlace "Obtener ejercicio mediante Code"
            enlace_obtener_por_code = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'selectByCode')]"))
            )
            enlace_obtener_por_code.click()

            # 2. Ingresar el código en el input
            # Intento 1: Localizar por el placeholder exacto
            try:
                input_codigo_ejercicio = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Escribe el codigo del ejercicio']"))
                )
                input_codigo_ejercicio.send_keys(CODIGO_EJERCICIO)
                print(f"Código '{CODIGO_EJERCICIO}' ingresado en el input por placeholder.")
            except TimeoutException:
                print("No se encontró el input por el placeholder exacto. Intentando por clase CSS.")
                # Intento 2: Localizar por la clase CSS
                try:
                    input_codigo_ejercicio = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input.chakra-input.css-1c6j008"))
                    )
                    input_codigo_ejercicio.send_keys(CODIGO_EJERCICIO)
                    print(f"Código '{CODIGO_EJERCICIO}' ingresado en el input por clase CSS.")
                except TimeoutException:
                    print("No se encontró el input ni por placeholder exacto ni por clase CSS.")
                    raise  # Relanzar la excepción para que el bloque except principal la capture

            # 3. Apretar el botón "Cargar ejercicio"
            boton_cargar_ejercicio = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cargar Ejercicio')]"))
            )
            boton_cargar_ejercicio.click()

            # 4. Verificar que el código ingresado aparece en la página
            elemento_codigo_cargado = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{CODIGO_EJERCICIO}')]"))
            )
            print(f"Código de ejercicio cargado y encontrado en la página: {elemento_codigo_cargado.text}")
            assert CODIGO_EJERCICIO in elemento_codigo_cargado.text
        except TimeoutException:
            print("Fallo en la verificación: El párrafo con la clase del nombre de usuario no se hizo visible a tiempo.")
            assert False

    except TimeoutException as e:
        print(f"Tiempo de espera agotado: {e}")
        assert False
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        assert False
    finally:
        driver.quit()

if __name__ == "__main__":
    test_login_con_auth0()