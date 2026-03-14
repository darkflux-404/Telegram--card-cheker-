# Documentacion Operativa del Proyecto

## 1. Resumen ejecutivo

Este proyecto es un bot de Telegram construido con Pyrogram y pyromod. Su funcion principal es:

- Registrar usuarios y grupos en una base SQLite local.
- Asignar membresias, roles, creditos y antispam.
- Exponer comandos de usuario, admin y "gates".
- Ejecutar verificaciones remotas mediante modulos `gates/*.py`.
- Mostrar menus interactivos por botones inline.

La arquitectura real queda asi:

1. `main.py` levanta el cliente Pyrogram y carga los plugins.
2. `plugins/users/*` expone herramientas y comandos de usuario.
3. `plugins/admin/*` expone administracion de usuarios, grupos, keys y broadcast.
4. `plugins/gates_cmds/*` valida entrada, permisos y llama a `gates/*.py`.
5. `gates/*.py` contiene la logica HTTP remota de cada gateway.
6. `utilsdf/db.py` es la capa de persistencia.
7. `assets/*` contiene configuracion estatica y catalogos.

## 2. Datos que debes cambiar para tomar control total

### 2.1 Variables de entorno obligatorias

Definidas o consumidas en varios archivos:

- `TELEGRAM_API_ID`: requerido por [main.py](/c:/Users/iamel/Downloads/telegram-card-checker-bot-main/telegram-card-checker-bot-main/main.py)
- `TELEGRAM_API_HASH`: requerido por [main.py](/c:/Users/iamel/Downloads/telegram-card-checker-bot-main/telegram-card-checker-bot-main/main.py)
- `TELEGRAM_BOT_TOKEN`: requerido por [main.py](/c:/Users/iamel/Downloads/telegram-card-checker-bot-main/telegram-card-checker-bot-main/main.py)
- `TELEGRAM_CHANNEL_LOGS`: canal donde se envian logs operativos.
- `REFES_CHAT`: chat destino del comando `.refe`.
- `CHANNEL_OFFICIAL`: chat/canal destino del comando `.refer`.
- `ID_OWNER`: se lee en algunos plugins, pero el control real del owner no depende de esto; depende de `utilsdf/db.py`.

### 2.2 Valores hardcodeados que debes reemplazar

Estos son mas importantes que las variables de entorno porque hoy mantienen amarrado el proyecto al operador original:

- `utilsdf/db.py`: `ID_OWNER = '5579729798'`
  Debes sustituirlo por tu Telegram ID. Este valor se auto-promueve a admin y premium al iniciar.
- `main.py`: `chat_id == -1001494650944`
  Grupo premium vigilado por el filtro de limpieza automatica. Si no usas ese grupo, cambialo o elimina la logica.
- `plugins/admin/add_premium.py`: crea invitacion y desbanea en `-1001494650944`
  Debe apuntar a tu grupo premium real.
- `plugins/users/claim_key.py`: crea invitacion y desbanea en `-1001960831832`
  Debe apuntar a tu grupo de usuarios/key claim.
- `plugins/users/generator_cmd.py`: envia copia del resultado a `-1002126020233`
  Ese chat recibira logs o fugas de informacion si no lo cambias.
- `plugins/users/claim_key.py`: mensaje menciona `@Sachioyt666` y `@Fucker_504`
  Sustituir por tus usuarios.
- `plugins/users/Plan.py`: `Fucker_504 = 1115269159`
  Ese ID recibe rango visual "Co-Founder". Cambialo o eliminalo.
- `utilsdf/cmds_desing.py` y `utilsdf/functions.py`: enlace `https://t.me/Was_B3`
  Sustituye por tu canal/usuario.
- `utilsdf/functions.py`: enlace `https://t.me/bosascsdctcascsscsacacsvbotbot?start=start`
  Se usa para renderizar simbolos clicables. Debe ser tu bot.
- `plugins/users/Cmds.py`: video externo `https://xddd727272666.alwaysdata.net/...`
  Si no controlas ese dominio, reemplazalo.
- `utilsdf/functions.py`: servicios externos `bincheck.io`, `akatsukichk.com`, `2captcha.com`, `anti-captcha.com`, `boss.alwaysdata.net`, `sachio.itbbarquisimeto.com`
  Debes revisar si quieres depender de ellos.

### 2.3 Otros archivos de runtime que deberias auditar

- `assets/db_bot.db`: base SQLite real de usuarios, keys, grupos y estados.
- `assets/bins.db`: base BIN local usada como fallback.
- `assets/proxies.txt` y `assets/proxies_sh.txt`: se esperan en runtime aunque no vienen en el inventario visible.

## 3. Inventario archivo por archivo

## 3.1 Raiz del proyecto

| Archivo | Funcion | Interaccion | Configuracion critica |
|---|---|---|---|
| `main.py` | Punto de entrada. Inicializa Pyrogram, carga plugins, registra usuarios, bloquea baneados y hace limpieza de un grupo premium. | Importa `Database`, `bot_on`, `PREFIXES`; carga `plugins/`. | `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_LOGS`, chat `-1001494650944`. |
| `run.bat` | Lanzador en bucle para Windows. Reinicia el bot tras caida o cierre. | Ejecuta `python main.py`. | Ninguna, salvo la decision de reinicio interactivo. |
| `requirements.txt` | Dependencias Python. | Necesario para instalar el entorno. | Debe revisarse antes de desplegar. |
| `README.md` | Documentacion general del proyecto. | Referencia instalacion y uso. | Contiene ejemplos de credenciales. |
| `INSTALLATION.md` | Guia de instalacion detallada. | Ayuda a preparar `.env`/secrets. | Incluye placeholders de API y bot token. |
| `CONTRIBUTING.md` | Normas de colaboracion. | No afecta ejecucion. | Ninguna. |
| `LICENSE` | Licencia del repositorio. | No afecta ejecucion. | Ninguna. |

## 3.2 `utilsdf/`

| Archivo | Funcion | Interaccion | Configuracion critica |
|---|---|---|---|
| `utilsdf/vars.py` | Lista de prefijos aceptados por comandos. | Consumido por casi todos los plugins. | Si quieres restringir prefijos, edita `PREFIXES`. |
| `utilsdf/db.py` | Singleton SQLite. Crea tablas, registra usuarios, roles, premium, keys, grupos, baneos, creditos y expiraciones. | Consumido por `main.py`, `plugins/users/*`, `plugins/admin/*`, `plugins/gates_cmds/*`. | `ID_OWNER = '5579729798'` es el control maestro real. |
| `utilsdf/functions.py` | Utilidades globales: captcha, antispam, parseo CC, BIN lookup, extras, traduccion, proxies, texto respondido, boton de compra y wrappers de gates. | Utilizado por casi todo el proyecto. | Enlaces `Was_B3`, `bosascsdctcascsscsacacsvbotbot`, APIs externas y lectura de proxies. |
| `utilsdf/generator.py` | Generador de tarjetas a partir de bin/patron. | Consumido por `.gen`. | No contiene credenciales. |
| `utilsdf/cmds_desing.py` | Textos del menu y botones inline. | Consumido por `plugins/users/Cmds.py` y `plugins/handlers/handlers_cmds.py`. | Canal hardcodeado `https://t.me/Was_B3`; aqui puedes reescribir toda la presentacion del bot. |
| `utilsdf/gates_for_mass.py` | Tabla de imports para los comandos masivos. | Consumido por `mass.py` y `mass_admin.py`. | No tiene credenciales. |
| `utilsdf/woocomerce_funcs.py` | Flujo reutilizable WooCommerce+Braintree. | Puede servir de helper para gates; hoy parece infra no conectada directamente a un comando. | Contiene correos, nombres y direccion hardcodeados tipo "Sachio". |
| `utilsdf/asacasc.py` | Script auxiliar para consultar BIN en `bincodes.net`. | No aparece integrado en plugins principales. | Dependencia externa `bincodes.net`. |

## 3.3 `plugins/handlers/`

| Archivo | Funcion | Interaccion | Configuracion critica |
|---|---|---|---|
| `plugins/handlers/handlers_cmds.py` | Maneja callbacks `home`, `gates`, `auths`, `chargeds`, `specials`, `tools`, `exit`. | Usa los textos y botones de `cmds_desing.py`. | El contenido mostrado depende de `cmds_desing.py`. |
| `plugins/handlers/handlers_main.py` | Responde a nuevos miembros y salidas de chat. | Corre automaticamente por eventos de grupo. | Los mensajes son genericos y algo toscos; no hay IDs fijos. |

## 3.4 `plugins/users/`

| Archivo | Funcion | Interaccion | Configuracion critica |
|---|---|---|---|
| `plugins/users/Cmds.py` | Menu principal y aliases de inicio. | Usa `text_home` y `buttons_cmds`. | Video externo `alwaysdata.net`. |
| `plugins/users/Id.py` | Muestra ID y datos del usuario/chat. | Usa `get_message_from_pyrogram`. | Sin configuracion sensible. |
| `plugins/users/Plan.py` | Muestra plan, rol, antispam, creditos, nick y expiracion de un usuario. | Lee `Database`. | ID fijo `1115269159` marcado como co-founder. |
| `plugins/users/Plang.py` | Muestra estado del grupo actual. | Lee `Database.get_info_group`. | Sin configuracion sensible. |
| `plugins/users/Bin.py` | Consulta informacion BIN de 6 digitos. | Usa `get_bin_info`. | Depende de `bincheck.io` y `assets/banned_bins.json`. |
| `plugins/users/Gbin.py` | Genera BINs cercanos y permite regenerarlos por callback. | Usa `get_bin_info`. | Sin credenciales locales. |
| `plugins/users/generator_cmd.py` | Genera tarjetas desde patron/bin y re-genera por callback. | Usa `Generator`, `get_bin_info`, `Database`. | Log hardcodeado a `-1002126020233`. |
| `plugins/users/extras.py` | Obtiene "extras" por BIN desde API remota. | Usa `get_extras` y `get_bin_info`. | Depende de `akatsukichk.com`. |
| `plugins/users/Rnd.py` | Genera direccion aleatoria por pais. | Usa `get_rand_info`. | Depende de `sachio.itbbarquisimeto.com`; codigos de pais en `assets/countrys.json`. |
| `plugins/users/Sk.py` | Valida una clave `sk_live_` de Stripe consultando balance. | Usa `get_info_sk`. | No guarda la key, pero la envia a Stripe. |
| `plugins/users/translate.py` | Traduce texto a otro idioma. | Usa `translate`, `Languages`, `antispam`. | Sin credenciales locales. |
| `plugins/users/claim_key.py` | Reclama una key premium y entrega invitacion a grupo. | Usa `Database.claim_key`, `CHANNEL_LOGS`. | Grupo fijo `-1001960831832`, prefijo `key-aktz`, menciones a admins originales. |
| `plugins/users/gpt.py` | Comando ChatGPT comentado/desactivado. | No participa en runtime actual. | Si se activa, requeriria revisar integracion. |

## 3.5 `plugins/admin/`

| Archivo | Funcion | Interaccion | Configuracion critica |
|---|---|---|---|
| `plugins/admin/add_premium.py` | Da premium, dias y creditos a un usuario. | Actualiza DB, envia logs y entrega invitacion. | Usa `CHANNEL_LOGS` y grupo fijo `-1001494650944`. |
| `plugins/admin/remove_premium.py` | Resetea premium o elimina grupo autorizado. | Llama `rename_premium` o `remove_group`. | Usa `CHANNEL_LOGS`. |
| `plugins/admin/ban_and_unban.py` | Banea o desbanea usuarios en DB. | Usa `unban_or_ban_user`. | Usa `CHANNEL_LOGS`. |
| `plugins/admin/Rol.py` | Promueve usuario a `seller` o `admin`. | Usa `promote_to_seller/admin`. | Usa `CHANNEL_LOGS`. |
| `plugins/admin/set_antispam.py` | Cambia antispam de un usuario. | Usa `set_antispam`. | Sin IDs fijos. |
| `plugins/admin/Nick.py` | Asigna nick administrativo. | Usa `set_nick`. | Sin IDs fijos. |
| `plugins/admin/Key.py` | Genera keys premium tipo `key-aktzXXXXXXXX`. | Usa `gen_key`. | Usa `CHANNEL_LOGS`; si cambias branding, cambia el prefijo. |
| `plugins/admin/AddGp.py` | Autoriza grupos por dias. | Usa `add_group`. | Usa `CHANNEL_LOGS`. |
| `plugins/admin/Broad.py` | Broadcast a usuarios y grupos registrados. | Usa API Bot HTTP directa y `db.get_chats_ids()`. | Usa `bot_token`; `ID_OWNER` se lee pero no controla nada. |
| `plugins/admin/api.py` | Prueba una URL usando `autoshopify`. | Llama gate general Shopify. | Solo admins; no tiene listas propias. |
| `plugins/admin/Refe.py` | Reenvia media respondida a `REFES_CHAT`. | Usa variable de entorno. | Debes fijar `REFES_CHAT`. |
| `plugins/admin/Refer.py` | Reenvia media respondida a `CHANNEL_OFFICIAL`. | Usa variable de entorno. | Debes fijar `CHANNEL_OFFICIAL`. |
| `plugins/admin/Restart.py` | Comando de reinicio desactivado/comentado. | No participa hoy. | Si lo revives, debes revisar imports viejos. |

## 3.6 `plugins/gates_cmds/`

Patron comun: validan permiso, parsean CC con `get_cc`, aplican antispam, llaman un gate de `gates/*.py`, incrementan checks y devuelven status.

| Archivo | Comando | Acceso | Gate invocado |
|---|---|---|---|
| `plugins/gates_cmds/aktz.py` | `ak` | Premium | `gates/aktz.py` |
| `plugins/gates_cmds/adriana.py` | `adr` | Premium | `gates/adriana.py` |
| `plugins/gates_cmds/ass.py` | `ass` | Premium | `gates/ass.py` |
| `plugins/gates_cmds/astharoth.py` | `at` | Autorizado | `gates/astharoth.py` |
| `plugins/gates_cmds/boruto.py` | `bo` | Premium | `gates/boruto.py` |
| `plugins/gates_cmds/brenda.py` | `br` | Premium | `gates/brenda.py` |
| `plugins/gates_cmds/darkito.py` | `dkt` | Premium | `gates/darkito.py` |
| `plugins/gates_cmds/devilsx.py` | `dx` | Premium | `gates/devilsx.py` |
| `plugins/gates_cmds/djbaby.py` | `dj` | Premium | `gates/djbaby.py` |
| `plugins/gates_cmds/ghoul.py` | `gh` | Premium | `gates/ghoul.py` |
| `plugins/gates_cmds/hinata.py` | `hn` | Premium | `gates/hinata.py` |
| `plugins/gates_cmds/hoshigaki.py` | `ho` | Autorizado | `gates/hoshigaki.py` |
| `plugins/gates_cmds/itachi.py` | `it` | Premium | `gates/CarolinaPayflow.py` |
| `plugins/gates_cmds/ka.py` | `ka` | Premium | `gates/ka.py` |
| `plugins/gates_cmds/ko.py` | `ko` | Autorizado | `gates/ko.py` |
| `plugins/gates_cmds/lynx.py` | `lynx` | Autorizado | `gates/lynx.py` |
| `plugins/gates_cmds/mai.py` | `mai` | Premium | `gates/mai.py` |
| `plugins/gates_cmds/odali.py` | `od` | Premium | `gates/odali.py` |
| `plugins/gates_cmds/or_cmd.py` | `or` | Autorizado | `gates/or_gate.py` |
| `plugins/gates_cmds/pepe.py` | `pe` | Premium | `gates/pepe.py` |
| `plugins/gates_cmds/piccolo.py` | `pi` | Autorizado | `gates/piccolo.py` |
| `plugins/gates_cmds/pp_cmd.py` | `pp` | Autorizado | `gates/pp.py` |
| `plugins/gates_cmds/pp_cmd_1.py` | `ppa` | Autorizado | `gates/pp1.py` |
| `plugins/gates_cmds/pussy.py` | `ps` | Premium | `gates/pussy.py` |
| `plugins/gates_cmds/rohee.py` | `rh` | Premium | `gates/rohee.py` |
| `plugins/gates_cmds/sebas.py` | `sb` | Autorizado | `gates/sebas.py` |
| `plugins/gates_cmds/sexo.py` | `sexo` | Autorizado | `gates/sexo.py` |
| `plugins/gates_cmds/shopifys_cmd.py` | `ha hq da kr za as ob hi ky mi to sa su uc ze ch de ve le gu si jt sn ke ri dr oz st be bl ju mo` | Segun `assets/gates.json`: `premium` o `free` | `gates/shopifys.py` -> `gates/autosh.py` |
| `plugins/gates_cmds/ssh.py` | `ssh` | Solo admin real en codigo | `gates/ssh.py` |
| `plugins/gates_cmds/vbv.py` | `vbv` | Autorizado | `gates/vbv.py` |
| `plugins/gates_cmds/zukesito.py` | `zu` | Premium | `gates/zukesito.py` |
| `plugins/gates_cmds/mass.py` | `ms` | Usuario con creditos suficientes | `gates_for_mass.py` o `autoshopify` |
| `plugins/gates_cmds/mass_admin.py` | `msa` | Admin | `gates_for_mass.py` o `autoshopify` |

## 3.7 `gates/`

Estos archivos son el backend HTTP de los checks. Todos dependen de sitios externos. Si el dominio cae, cambia flujo, bloquea proxies o modifica antifraude, el comando correspondiente deja de funcionar.

| Archivo | Funcion | Sitio principal observado |
|---|---|---|
| `gates/adriana.py` | Flow WellnessLiving | `wellnessliving.com` |
| `gates/aktz.py` | Flow WooCommerce + Stripe setup intent | `steelportknife.com` |
| `gates/ass.py` | Flow iSubscribe + PMNTS + Cardinal | `isubscribe.co.uk` |
| `gates/astharoth.py` | Flow Stripe checkout | `growthrx.com` |
| `gates/autosh.py` | Motor Shopify generico reutilizable | checkout Shopify genrico |
| `gates/boruto.py` | Flow PrepSportswear + Stripe | `prepsportswear.com` |
| `gates/CarolinaPayflow.py` | Flow Carolina + Payflow | `carolina.com` |
| `gates/brenda.py` | Flow BigCommerce/Onrally/Vault | `burjushoes.com` |
| `gates/darkito.py` | Flow GardenerDirect | `gardenerdirect.com` |
| `gates/devilsx.py` | Flow USAKilts | `usakilts.com` |
| `gates/djbaby.py` | Flow SportysHealth + eWay + 3DS | `sportyshealth.com.au` |
| `gates/ghoul.py` | Flow Flanigans + Square | `flanigans.net` |
| `gates/hinata.py` | Flow Desertcart + Checkout.com | `desertcart.us` |
| `gates/hoshigaki.py` | Flow donation Stripe | `abaana.org` |
| `gates/ka.py` | Flow ALeenes checkout | `aleenes.com` |
| `gates/ko.py` | Flow Komodo + Stripe setup intent | `komodomath.com` |
| `gates/lizzy.py` | Flow Helen Dale Dermatology | `helendaledermatology.com` |
| `gates/lynx.py` | Flow dedicado del autor | revisar archivo si se activa |
| `gates/mai.py` | Flow dedicado del autor | revisar archivo si se activa |
| `gates/odali.py` | Flow dedicado del autor | revisar archivo si se activa |
| `gates/or_gate.py` | Flow Stripe CCN | revisar archivo si se activa |
| `gates/pepe.py` | Flow dedicado del autor | revisar archivo si se activa |
| `gates/piccolo.py` | Flow dedicado del autor | revisar archivo si se activa |
| `gates/pp.py` | Flow PayPal $0.01 | `paypal.com` |
| `gates/pp1.py` | Flow PayPal $1 | `paypal.com` |
| `gates/pussy.py` | Flow WooCommerce + Braintree parametrizado por URL | URL dinamica |
| `gates/rohee.py` | Flow Gaia + Adyen | `gaia.com` |
| `gates/sebas.py` | Flow AutoEQ | `autoeq.ca` |
| `gates/sexo.py` | Variante WooCommerce + Braintree parametrizada | URL dinamica |
| `gates/shopifys.py` | Adaptador de comandos dinamicos Shopify | usa `assets/gates.json` |
| `gates/ssh.py` | Generador de accesos SSH contra sitio externo | `hackkcah.com` |
| `gates/vantiv.py` | Flow Springboard/Vantiv | `donate.mpbfoundation.org` |
| `gates/vbv.py` | Verificacion sobre JustFabrics | `justfabrics.co.uk` |
| `gates/zukesito.py` | WooCommerce add-payment-method | `myliporidex.com` |

Nota: `gates/lizzy.py`, `gates/vantiv.py` y algunos dedicados no tienen comando plugin visible en el inventario actual, por lo que hoy parecen codigo huero o reservado.

## 3.8 `assets/`

| Archivo | Funcion | Interaccion | Configuracion critica |
|---|---|---|---|
| `assets/gates.json` | Catalogo de comandos Shopify dinamicos. | Lo usa `shopifys_cmd.py`, `mass.py`, `mass_admin.py`, `gates/shopifys.py`. | Aqui cambias cmd, nombre, sitio y si el gate es `premium` o `free`. |
| `assets/responses.json` | Clasifica respuestas como AVS, low funds, CCN. | Util para interpretar gateways. | Puedes ampliar catalogo de textos. |
| `assets/countrys.json` | Lista de codigos pais para `.rnd`. | Lo usa `get_rand_info`. | Debes mantener consistencia con `Rnd.py`. |
| `assets/banned_bins.json` | BINs a bloquear. | Lo usa `get_bin_info`. | Si quieres permitir o bloquear mas BINs, edita este archivo. |

## 4. Base de datos y control administrativo real

Tablas creadas por `utilsdf/db.py`:

- `bot`: usuarios.
- `bot_keys`: keys premium.
- `groups`: grupos autorizados.

Campos relevantes de `bot`:

- `ID`: Telegram ID del usuario.
- `USERNAME`
- `NICK`
- `RANK`: `user`, `seller`, `admin`
- `STATE`: `free` o `ban`
- `MEMBERSHIP`: `free user` o `Premium`
- `EXPIRATION`
- `ANTISPAM`
- `CREDITS`
- `REGISTERED`
- `CHECKS`

Control real del proyecto:

1. Cambiar `Database.ID_OWNER`.
2. Revisar manualmente `assets/db_bot.db` para eliminar admins/sellers heredados.
3. Cambiar todos los grupos/canales hardcodeados.
4. Cambiar enlaces de compra/canal y menciones personales del autor.

## 5. Lista completa de comandos

### 5.1 Comandos generales de usuario

| Comando | Quien lo ejecuta | Funcion |
|---|---|---|
| `cmds`, `cmd`, `iniciar`, `inicio`, `help`, `menu`, `gates`, `gate`, `start` | Cualquiera | Abre el menu principal del bot. |
| `id`, `perfil`, `about`, `profile`, `me`, `my`, `info` | Cualquiera | Muestra ID de usuario y, en grupos, ID y tipo del chat. |
| `plan` | Cualquiera | Muestra membresia, rol, antispam, creditos, nick y fecha de registro. Acepta ID/@usuario. |
| `plang` | Cualquiera | Muestra si el grupo actual esta autorizado y su expiracion. |
| `bin` | Usuario autorizado | Consulta BIN y devuelve banco, pais, marca, tipo y nivel. |
| `gbin` | Usuario autorizado | Genera BINs cercanos desde un prefijo. |
| `gen` | Usuario autorizado o usuario con creditos | Genera tarjetas desde un patron/bin. |
| `extra` | Usuario autorizado | Consulta extras por BIN. |
| `rnd` | Usuario autorizado | Genera direccion aleatoria por pais. |
| `sk` | Usuario autorizado | Verifica una `sk_live_` de Stripe consultando balance. |
| `tr` | Usuario autorizado | Traduce texto a un idioma. |
| `claim` | Usuario no seller con key valida | Canjea una key premium y entrega invitacion a grupo. |

### 5.2 Comandos administrativos

| Comando | Quien lo ejecuta | Funcion |
|---|---|---|
| `addp` | Admin | Da premium, dias y creditos a un usuario. |
| `delp` | Admin | Quita premium de un usuario o elimina autorizacion de grupo si la ID es negativa. |
| `ban` | Admin | Banea usuario en la DB. |
| `unban` | Admin | Desbanea usuario en la DB. |
| `set_rol` | Admin | Promueve a `seller` o `admin`. |
| `antispam` | Admin | Cambia el antispam de un usuario. |
| `nick` | Admin | Asigna o cambia nick administrativo. |
| `gkey` | Seller o admin | Genera keys premium. |
| `addg` | Seller o admin | Autoriza un grupo por dias. |
| `broad` | Admin | Envia broadcast a todos los chats y grupos registrados. |
| `api` | Admin | Prueba una URL usando el motor Shopify general. |
| `refe` | Cualquiera | Reenvia media respondida al chat `REFES_CHAT`. |
| `refer` | Seller o admin | Reenvia media respondida al chat/canal `CHANNEL_OFFICIAL`. |
| `rbot` | Nadie hoy | Esta comentado. |

### 5.3 Comandos de gates individuales

| Comando | Quien lo ejecuta | Funcion |
|---|---|---|
| `ak` | Premium | Ejecuta gate `aktz`. |
| `adr` | Premium | Ejecuta gate `adriana`. |
| `ass` | Premium | Ejecuta gate `ass`. |
| `at` | Autorizado | Ejecuta gate `astharoth`. |
| `bo` | Premium | Ejecuta gate `boruto`. |
| `br` | Premium | Ejecuta gate `brenda`. |
| `dkt` | Premium | Ejecuta gate `darkito`. |
| `dx` | Premium | Ejecuta gate `devilsx`. |
| `dj` | Premium | Ejecuta gate `djbaby`. |
| `gh` | Premium | Ejecuta gate `ghoul`. |
| `hn` | Premium | Ejecuta gate `hinata`. |
| `ho` | Autorizado | Ejecuta gate `hoshigaki`. |
| `it` | Premium | Ejecuta Payflow via `CarolinaPayflow`. |
| `ka` | Premium | Ejecuta gate `ka`. |
| `ko` | Autorizado | Ejecuta gate `ko`. |
| `lynx` | Autorizado | Ejecuta gate `lynx`. |
| `mai` | Premium | Ejecuta gate `mai`. |
| `od` | Premium | Ejecuta gate `odali`. |
| `or` | Autorizado | Ejecuta gate `or_gate`. |
| `pe` | Premium | Ejecuta gate `pepe`. |
| `pi` | Autorizado | Ejecuta gate `piccolo`. |
| `pp` | Autorizado | Ejecuta PayPal $0.01. |
| `ppa` | Autorizado | Ejecuta PayPal $1. |
| `ps` | Premium | Ejecuta gate `pussy`. |
| `rh` | Premium | Ejecuta gate `rohee`. |
| `sb` | Autorizado | Ejecuta gate `sebas`. |
| `sexo` | Autorizado | Ejecuta gate `sexo`. |
| `ssh` | Admin | Ejecuta generador SSH. |
| `vbv` | Autorizado | Ejecuta gate `vbv`. |
| `zu` | Premium | Ejecuta gate `zukesito`. |
| `ms` | Usuario con creditos | Ejecuta checks masivos, descontando creditos. |
| `msa` | Admin | Ejecuta checks masivos administrativos sin restriccion de creditos de usuario final. |

### 5.4 Comandos Shopify dinamicos

Definidos en `assets/gates.json` y atendidos por `shopifys_cmd.py`.

| Comando | Gate | Sitio | Tipo |
|---|---|---|---|
| `ha` | Haku | `shoepalace.com` | premium |
| `hq` | Harley Quinn | `shop.wellwise.ca` | premium |
| `da` | Daibutsu | `www.burkedecor.com` | premium |
| `kr` | Karin | `morphe.com` | premium |
| `za` | Zabuza | `www.cuccoo.com` | premium |
| `as` | Asuma | `www.edenbrothers.com` | free |
| `ob` | Obito | `www.harrisfarm.com.au` | premium |
| `hi` | Hidan | `splendid.com` | free |
| `ky` | Kyusuke | `journelle.com` | premium |
| `mi` | Minato | `www.kookai.us` | premium |
| `to` | Tobi | `www.sheglam.com` | premium |
| `sa` | Sasori | `www.giftlab.com` | premium |
| `su` | Sakura | `moonmagic.com` | premium |
| `uc` | Uchiha | `thursdayboots.com` | premium |
| `ze` | Zetsu | `www.incu.com` | premium |
| `ch` | Chronic | `bluemercury.com` | premium |
| `de` | Deidara | `blendtec.com` | premium |
| `ve` | Vegeta | `www.ashleyjewels.com` | premium |
| `le` | Lelouch Lamperouge | `ksubi.com` | premium |
| `gu` | Gut | `rockabilia.com` | premium |
| `si` | Saiken | `www.maxtool.com` | free |
| `jt` | Jutsu | `www.myfacesocks.com` | premium |
| `sn` | Sanin | `nothingnew.com` | free |
| `ke` | Kekkei | `shopnicekicks.com` | premium |
| `ri` | Rinegan | `www.petsense.com` | premium |
| `dr` | Droxx | `fellahamilton.com.au` | premium |
| `oz` | Ozzy | `www.thewodlife.com.au` | premium |
| `st` | Sketit | `www.journelle.com` | premium |
| `be` | Beastlord | `www.altitude-sports.com` | free |
| `bl` | Bellingham | `www.svsound.com` | premium |
| `ju` | Jude | `wildflowersex.com` | premium |
| `mo` | Mora | `sweethoneyclothing.com` | premium |

## 6. Riesgos operativos que debes conocer

- El proyecto depende fuerte de servicios y dominios de terceros.
- Hay IDs y enlaces incrustados del operador original.
- El owner real esta duro en `utilsdf/db.py`, no en `.env`.
- El bot entrega links de invitacion automaticos a grupos especificos.
- `broad` usa la API HTTP del bot con el token del bot; si el token se filtra, te toman el control del bot.
- El comando `.gen` copia resultados a un chat externo hardcodeado.

## 7. Orden recomendado para apropiarte del sistema

1. Cambia `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_BOT_TOKEN`.
2. Cambia `utilsdf/db.py` -> `ID_OWNER`.
3. Cambia `TELEGRAM_CHANNEL_LOGS`, `REFES_CHAT`, `CHANNEL_OFFICIAL`.
4. Sustituye todos los IDs negativos hardcodeados por tus grupos reales.
5. Sustituye enlaces `t.me` y menciones a usuarios originales.
6. Audita `assets/db_bot.db` y elimina admins/sellers heredados.
7. Revisa `assets/gates.json` y deja solo los comandos/sites que quieras mantener.

