# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 zornade (https://zornade.com)
# See LICENSE, NOTICE, and COMMERCIAL-LICENSE.md at the repository root.

import os
from typing import Optional

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from .infrastructure import PageLogger


async def _login_sielte(page: Page, logger: PageLogger, username: str, password: str) -> None:
    """Esegue l'autenticazione SPID tramite provider Sielte ID (MySielteID).

    Credenziali richieste:
        ADE_USERNAME — codice fiscale o partita IVA dell'account Sielte
        ADE_PASSWORD — password dell'account Sielte

    Il secondo fattore è gestito tramite notifica push sull'app MySielteID:
    l'utente approva sull'app e clicca 'Autorizza' (timeout 120s).
    """
    step = "sielte_id"
    try:
        print("[LOGIN] Clicco 'Sielte ID'...")
        await page.locator('a[href*="sielte"]').click()
        await logger.log(page, "sielte_id")

        step = "username"
        print("[LOGIN] Inserisco username...")
        await page.get_by_role("textbox", name="Codice Fiscale / Partita IVA").press("CapsLock")
        await page.get_by_role("textbox", name="Codice Fiscale / Partita IVA").fill(username)
        await logger.log(page, "username")

        step = "password"
        print("[LOGIN] Inserisco password...")
        await page.get_by_role("textbox", name="Password").click()
        await page.get_by_role("textbox", name="Password").fill(password)

        step = "prosegui"
        print("[LOGIN] Clicco 'Prosegui'...")
        await page.get_by_role("button", name="Prosegui").click()
        await logger.log(page, "prosegui")

        step = "notifica_push"
        print("[LOGIN] Cerco link notifica (può non esserci)...")
        try:
            await page.get_by_role(
                "link", name="Utilizza il le notifiche Ricevi una notifica sull'app MySielteID"
            ).click(timeout=4000)
            print("[LOGIN] Cliccato link notifica (testo completo).")
        except PlaywrightTimeoutError:
            print("[LOGIN] Link notifica con testo completo non trovato, provo fallback...")
            try:
                await page.locator(
                    'a.link-sso:has(img[alt="Utilizza il le notifiche"]):has(p:text("Ricevi una notifica sull\'app MySielteID"))'
                ).click(timeout=4000)
                print("[LOGIN] Cliccato link notifica (fallback DOM selector).")
            except PlaywrightTimeoutError:
                print("[LOGIN] Nessun link notifica trovato, continuo...")
        await logger.log(page, "notifica_push")

        step = "autorizza"
        appear_timeout_s = int(os.getenv("LOGIN_AUTORIZZA_APPEAR_TIMEOUT_S", "15"))
        print(
            f"[LOGIN] Attendo pulsante 'Autorizza' (max {appear_timeout_s}s) — "
            f"se non appare = credenziali probabilmente errate"
        )
        try:
            await page.get_by_role("button", name="Autorizza").wait_for(
                state="visible", timeout=appear_timeout_s * 1000
            )
        except PlaywrightTimeoutError as e:
            current_url = page.url
            await logger.log(page, f"ERRORE_sielte_{step}_autorizza_non_apparso")
            raise RuntimeError(
                f"Login Sielte fallito: pulsante 'Autorizza' non apparso entro "
                f"{appear_timeout_s}s. Credenziali probabilmente errate o flusso "
                f"Sielte modificato. URL corrente: {current_url}"
            ) from e

        print("[LOGIN] Clicco 'Autorizza'... (attendo conferma notifica push, timeout 120s)")
        await page.get_by_role("button", name="Autorizza").click(timeout=120000)
        await logger.log(page, "autorizza")
    except Exception:
        await logger.log(page, f"ERRORE_sielte_{step}")
        raise


async def _login_poste(page: Page, logger: PageLogger, username: str, password: str) -> None:
    """Esegue l'autenticazione SPID tramite provider Poste Italiane (PosteID).

    Credenziali richieste:
        POSTE_USERNAME — indirizzo email dell'account PosteID
        POSTE_PASSWORD — password dell'account PosteID

    Il secondo fattore è gestito tramite notifica push sull'app PosteID:
    l'utente approva sull'app e la pagina si reindirizza automaticamente
    sul dominio agenziaentrate.gov.it (timeout 120s).
    """
    step = "poste_id"
    try:
        print("[LOGIN] Clicco 'Poste Italiane'...")
        await page.locator('a[href*="poste"]').click()
        await logger.log(page, "poste_id")

        step = "username"
        print("[LOGIN] Inserisco email PosteID...")
        await page.get_by_role("textbox", name="Indirizzo e-mail").fill(username)
        await logger.log(page, "username")

        step = "password"
        print("[LOGIN] Inserisco password PosteID...")
        await page.get_by_role("textbox", name="Password").fill(password)

        step = "avanti"
        print("[LOGIN] Clicco 'Avanti'...")
        await page.get_by_role("button", name="Avanti").click()
        await logger.log(page, "avanti")

        step = "attesa_app"
        appear_timeout_s = int(os.getenv("LOGIN_POSTE_PUSH_APPEAR_TIMEOUT_S", "15"))
        print(
            f"[LOGIN] Attendo transizione push PosteID (max {appear_timeout_s}s) — "
            f"se rimane sulla form = credenziali probabilmente errate"
        )
        try:
            await page.wait_for_function(
                "url => !window.location.href.includes('login') && !window.location.href.includes('Login')",
                timeout=appear_timeout_s * 1000,
            )
        except PlaywrightTimeoutError as e:
            current_url = page.url
            await logger.log(page, f"ERRORE_poste_{step}_push_non_partita")
            raise RuntimeError(
                f"Login PosteID fallito: la pagina non e' uscita dal form di login "
                f"entro {appear_timeout_s}s. Credenziali probabilmente errate o "
                f"flusso PosteID modificato. URL corrente: {current_url}"
            ) from e

        print("[LOGIN] Attendo approvazione sull'app PosteID (timeout 120s)...")
        await page.wait_for_url("**/agenziaentrate.gov.it/**", timeout=120000)
        await logger.log(page, "redirect_post_auth")
    except Exception:
        await logger.log(page, f"ERRORE_poste_{step}")
        raise


async def _login_sister_direct(page: Page, logger: PageLogger, username: str, password: str) -> None:
    """Esegue il login diretto SISTER tramite il tab dedicato sulla pagina ADE.

    Credenziali richieste:
        SISTER_USERNAME — username dell'account SISTER nominale dell'utente
        SISTER_PASSWORD — password dell'account SISTER nominale dell'utente

    Scope d'uso ammesso: questo flusso è destinato all'**intestatario della
    convenzione SISTER** che desidera automatizzare le proprie consultazioni
    con le proprie credenziali nominali. Non è destinato a chi vuole rivendere
    o esporre l'accesso al portale SISTER a terzi (la convenzione SISTER
    richiede che l'utenza sia personale, non cedibile, e che le consultazioni
    siano riconducibili all'intestatario).

    Dopo il login si atterra direttamente nella pagina SceltaServizio di
    SISTER, saltando la navigazione tramite portale ADE.
    """
    step = "sister_tab"
    try:
        print("[LOGIN] Clicco tab 'Sister'...")
        await page.get_by_role("tab", name="Sister").click()
        await logger.log(page, "sister_tab")

        step = "username"
        print("[LOGIN] Inserisco username SISTER...")
        await page.get_by_role("textbox", name="Utente:").fill(username)
        await logger.log(page, "username")

        step = "password"
        print("[LOGIN] Inserisco password SISTER...")
        await page.get_by_role("textbox", name="Password:").fill(password)

        step = "accedi"
        print("[LOGIN] Clicco 'Accedi'...")
        await page.get_by_role("button", name="Accedi").click()
        await logger.log(page, "accedi")

        step = "attesa_sister"
        print("[LOGIN] Attendo caricamento portale SISTER...")
        await page.wait_for_load_state("domcontentloaded", timeout=30000)
        await logger.log(page, "portale_sister")

        MAX_CLOSE_ATTEMPTS = 10

        def _is_orphan(content: str, current_url: str) -> bool:
            return "Utente gia' in sessione" in content or "error_locked.jsp" in current_url

        content = await page.content()
        url = page.url
        attempts_done = 0
        while _is_orphan(content, url) and attempts_done < MAX_CLOSE_ATTEMPTS:
            attempts_done += 1
            print(
                f"[LOGIN] Sessione orfana rilevata (tentativo {attempts_done}/{MAX_CLOSE_ATTEMPTS}) — chiudo e riprovo..."
            )
            step = f"close_session_{attempts_done}"
            await page.goto(
                "https://sister3.agenziaentrate.gov.it/Servizi/CloseSessionsSis",
                timeout=30000,
            )
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
            await logger.log(page, f"close_session_{attempts_done}")

            step = f"sister_tab_retry_{attempts_done}"
            await page.goto(
                "https://iampe.agenziaentrate.gov.it/sam/UI/Login?realm=/agenziaentrate",
                timeout=30000,
            )
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
            await page.get_by_role("tab", name="Sister").click()
            await page.get_by_role("textbox", name="Utente:").fill(username)
            await page.get_by_role("textbox", name="Password:").fill(password)
            await page.get_by_role("button", name="Accedi").click()
            await page.wait_for_load_state("domcontentloaded", timeout=30000)
            await logger.log(page, f"portale_sister_retry_{attempts_done}")

            content = await page.content()
            url = page.url

        if _is_orphan(content, url):
            print("[LOGIN][ERRORE] Troppe sessioni orfane, impossibile liberare la sessione.")
            raise Exception(
                f"Utente già in sessione su un'altra postazione (max {MAX_CLOSE_ATTEMPTS} tentativi raggiunto)"
            )

        print("[LOGIN] Login SISTER completato.")

    except Exception:
        await logger.log(page, f"ERRORE_sister_{step}")
        raise


async def perform_login(page: Page) -> None:
    """Esegue il login completo (SPID + navigazione fino a 'Visure catastali').

    Il provider di autenticazione è selezionato dalla variabile d'ambiente
    ``SPID_PROVIDER`` (case-insensitive):

    * ``sielte`` (default) — SPID Sielte ID, credenziali ``ADE_USERNAME`` /
      ``ADE_PASSWORD``.
    * ``poste`` — SPID PosteID, credenziali ``POSTE_USERNAME`` /
      ``POSTE_PASSWORD``.
    * ``sister`` — login diretto SISTER tramite il tab dedicato della pagina
      ADE, credenziali ``SISTER_USERNAME`` / ``SISTER_PASSWORD``.
    """
    spid_provider = os.getenv("SPID_PROVIDER", "sielte").lower()

    if spid_provider == "sielte":
        username = os.getenv("ADE_USERNAME")
        password = os.getenv("ADE_PASSWORD")
        if not username or not password:
            raise ValueError("ADE_USERNAME and ADE_PASSWORD environment variables must be set")
    elif spid_provider == "poste":
        username = os.getenv("POSTE_USERNAME")
        password = os.getenv("POSTE_PASSWORD")
        if not username or not password:
            raise ValueError("POSTE_USERNAME and POSTE_PASSWORD environment variables must be set")
    elif spid_provider == "sister":
        username = os.getenv("SISTER_USERNAME")
        password = os.getenv("SISTER_PASSWORD")
        if not username or not password:
            raise ValueError("SISTER_USERNAME and SISTER_PASSWORD environment variables must be set")
    else:
        raise ValueError(
            f"SPID_PROVIDER non supportato: '{spid_provider}'. " "Valori validi: 'sielte', 'poste', 'sister'"
        )

    logger = PageLogger("login")
    step = "init"

    try:
        step = "goto_login"
        print("[LOGIN] Navigo alla pagina di login...")
        await page.goto("https://iampe.agenziaentrate.gov.it/sam/UI/Login?realm=/agenziaentrate")
        await logger.log(page, "goto_login")

        if spid_provider == "sister":
            step = "provider_sister"
            await _login_sister_direct(page, logger, username, password)
            return

        step = "entra_con_spid"
        print("[LOGIN] Clicco 'Entra con SPID'...")
        await page.get_by_role("button", name="Entra con SPID").click()
        await logger.log(page, "entra_con_spid")

        step = f"provider_{spid_provider}"
        print(f"[LOGIN] Autenticazione tramite provider: {spid_provider}...")
        if spid_provider == "sielte":
            await _login_sielte(page, logger, username, password)
        else:  # poste
            await _login_poste(page, logger, username, password)

        step = "cerca_sister"
        print("[LOGIN] Cerco servizio SISTER...")
        await page.get_by_role("textbox", name="Cerca il servizio").click()
        await page.get_by_role("textbox", name="Cerca il servizio").fill("SISTER")
        await page.get_by_role("textbox", name="Cerca il servizio").press("Enter")
        await logger.log(page, "cerca_sister")

        step = "vai_al_servizio"
        print("[LOGIN] Clicco 'Vai al servizio'...")
        await page.get_by_role("link", name="Vai al servizio").first.click()

        step = "controllo_sessione"
        print("[LOGIN] Attendo caricamento pagina...")
        await page.wait_for_load_state("domcontentloaded")
        await logger.log(page, "vai_al_servizio")
        print("[LOGIN] Controllo blocco sessione...")
        content = await page.content()
        url = page.url
        if "Utente gia' in sessione" in content or "error_locked.jsp" in url:
            print("[LOGIN][ERRORE] Utente già in sessione su un'altra postazione!")
            raise Exception("Utente già in sessione su un'altra postazione")

        step = "conferma"
        print("[LOGIN] Clicco 'Conferma'...")
        await page.get_by_role("button", name="Conferma").click()
        await logger.log(page, "conferma")

        step = "consultazioni"
        print("[LOGIN] Clicco 'Consultazioni e Certificazioni'...")
        await page.get_by_role("link", name="Consultazioni e Certificazioni").click()
        await logger.log(page, "consultazioni")

        step = "visure_catastali"
        print("[LOGIN] Clicco 'Visure catastali'...")
        await page.get_by_role("link", name="Visure catastali").click()
        await logger.log(page, "visure_catastali")

        step = "conferma_lettura"
        print("[LOGIN] Clicco 'Conferma Lettura'...")
        await page.get_by_role("link", name="Conferma Lettura").click()
        await logger.log(page, "conferma_lettura")

    except Exception:
        await logger.log(page, f"ERRORE_{step}")
        raise


async def perform_logout(page: Page) -> None:
    """Effettua il logout dal portale SISTER."""
    logger = PageLogger("logout")
    try:
        await logger.log(page, "before_logout")
        print("[LOGOUT] Cercando il bottone 'Esci'...")

        logout_selectors = [
            "input[value='Esci']",
            "button:has-text('Esci')",
            "a:has-text('Esci')",
            "input[type='submit'][value*='Esci']",
            "*[onclick*='logout']",
            "*[onclick*='Esci']",
        ]

        logout_success = False

        for selector in logout_selectors:
            try:
                print(f"[LOGOUT] Tentativo selettore: {selector}")
                logout_button = page.locator(selector)
                count = await logout_button.count()
                print(f"[LOGOUT] Trovati {count} elementi con selettore {selector}")

                if count > 0:
                    await logout_button.first.click()
                    try:
                        await page.wait_for_load_state("domcontentloaded", timeout=10000)
                    except Exception:
                        pass
                    print(f"[LOGOUT] Logout effettuato con successo usando selettore: {selector}")
                    logout_success = True
                    break

            except Exception as e:
                print(f"[LOGOUT] Errore con selettore {selector}: {e}")
                continue

        if not logout_success:
            print("[LOGOUT] ATTENZIONE: Non è stato possibile trovare il bottone 'Esci'")
            await logger.log(page, "logout_bottone_non_trovato")
        else:
            await logger.log(page, "after_logout")
            print("[LOGOUT] Sessione chiusa correttamente")

    except Exception as e:
        print(f"[LOGOUT] Errore durante il logout: {e}")
        await logger.log(page, "logout_errore")
