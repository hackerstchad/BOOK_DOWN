#!/usr/bin/env python3
"""
BOOK-DOWN
Script de téléchargement de livres électroniques depuis des sites web.
Créé par la communauté Hackerst-Tchad.

Usage éthique : téléchargez uniquement des livres libres de droits,
des contenus Creative Commons, ou des contenus que vous avez le droit de télécharger.
"""

import os
import re
import sys
import time
import json
import argparse
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


# ==== STYLES TERMINAL ====
class Style:
    GREEN = '\033[92m'
    DARK_GREEN = '\033[32m'
    BLACK_BG = '\033[40m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


def clear():
    os.system("clear" if sys.platform != "win32" else "cls")


def banner():
    print(Style.BLACK_BG + Style.GREEN + Style.BOLD)
    print("""
    ██████╗  ██████╗  ██████╗ ██╗  ██╗      ██████╗  ██████╗ ██╗    ██╗██╗   ██╗
    ██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝      ██╔══██╗██╔═══██╗██║    ██║██║   ██║
    ██████╔╝██║   ██║██║   ██║█████╔╝       ██║  ██║██║   ██║██║ █╗ ██║██║   ██║
    ██╔══██╗██║   ██║██║   ██║██╔═██╗       ██║  ██║██║   ██║██║███╗██║██║   ██║
    ██████╔╝╚██████╔╝╚██████╔╝██║  ██╗      ██████╔╝╚██████╔╝╚███╔███╔╝╚██████╔╝
    ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝      ╚═════╝  ╚═════╝  ╚══╝╚══╝  ╚═════╝ 
                            Créé par Hackerst-Tchad
    """)
    print(Style.RESET)


def progress_bar(label, current, total, length=40):
    percent = int((current / total) * 100) if total > 0 else 0
    filled = int((current / total) * length) if total > 0 else 0
    bar = '█' * filled + '░' * (length - filled)
    print(f"\r{Style.CYAN}[*] {label} [{Style.GREEN}{bar}{Style.CYAN}] {percent}%{Style.RESET}", end='')
    sys.stdout.flush()


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def is_book_link(href):
    book_extensions = ['.pdf', '.epub', '.mobi', '.azw3', '.djvu', '.txt', '.doc', '.docx', '.rtf']
    if not href:
        return False
    href_lower = href.lower()
    return any(href_lower.endswith(ext) for ext in book_extensions)


def get_filename_from_url(url, default="book"):
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    if not filename:
        filename = default
    filename = re.sub(r'[^\w\-.]', '_', filename)
    return filename


def download_file(url, output_dir, session, index=0, total=0):
    try:
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()

        filename = get_filename_from_url(url, f"book_{index}")
        filepath = os.path.join(output_dir, filename)

        # Éviter d'écraser un fichier existant
        counter = 1
        original_filepath = filepath
        while os.path.exists(filepath):
            name, ext = os.path.splitext(original_filepath)
            filepath = f"{name}_{counter}{ext}"
            counter += 1

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

        size_kb = downloaded / 1024
        return True, filename, size_kb
    except Exception as e:
        return False, str(e), 0


def discover_books(base_url, session, recursive=False, max_depth=2, visited=None, depth=0):
    if visited is None:
        visited = set()

    if base_url in visited or depth > max_depth:
        return set()

    visited.add(base_url)
    books = set()

    try:
        response = session.get(base_url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Recherche directe de liens vers des livres
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)

            if is_book_link(full_url):
                books.add(full_url)
            elif recursive and is_valid_url(full_url):
                # Suivre les liens internes
                parsed_base = urlparse(base_url)
                parsed_link = urlparse(full_url)
                if parsed_base.netloc == parsed_link.netloc:
                    books.update(discover_books(full_url, session, recursive, max_depth, visited, depth + 1))

        # Recherche dans iframes, objets, embeds
        for tag in soup.find_all(['iframe', 'object', 'embed'], src=True):
            src = urljoin(base_url, tag['src'])
            if is_book_link(src):
                books.add(src)

    except Exception as e:
        print(f"\n{Style.RED}[-] Erreur lors de l'analyse de {base_url}: {e}{Style.RESET}")

    return books


def save_manifest(books, output_dir, successful_downloads):
    manifest = {
        'total_found': len(books),
        'total_downloaded': len(successful_downloads),
        'books': list(books),
        'downloaded': successful_downloads
    }
    manifest_path = os.path.join(output_dir, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest_path


def interactive_menu():
    banner()
    print(f"{Style.CYAN}[*] Bienvenue dans BOOK-DOWN{Style.RESET}\n")

    url = input(f"{Style.GREEN}[?] URL du site à analyser : {Style.RESET}").strip()
    if not is_valid_url(url):
        print(f"{Style.RED}[-] URL invalide.{Style.RESET}")
        sys.exit(1)

    output = input(f"{Style.GREEN}[?] Dossier de sortie (défaut: books_download) : {Style.RESET}").strip()
    if not output:
        output = "books_download"

    recursive_input = input(f"{Style.GREEN}[?] Recherche récursive ? (o/n) : {Style.RESET}").strip().lower()
    recursive = recursive_input == 'o'

    max_depth = 1
    if recursive:
        try:
            max_depth = int(input(f"{Style.GREEN}[?] Profondeur maximale (défaut: 2) : {Style.RESET}").strip() or "2")
        except ValueError:
            max_depth = 2

    extensions = input(f"{Style.GREEN}[?] Extensions à rechercher (défaut: pdf,epub,mobi) : {Style.RESET}").strip()
    if extensions:
        global book_extensions
        book_extensions = ['.' + ext.strip().lstrip('.') for ext in extensions.split(',')]

    return url, output, recursive, max_depth


def main():
    parser = argparse.ArgumentParser(
        description="BOOK-DOWN - Téléchargeur de livres électroniques",
        epilog="Utilisation éthique uniquement. Respectez les droits d'auteur."
    )
    parser.add_argument('-u', '--url', help='URL du site à analyser')
    parser.add_argument('-o', '--output', default='books_download', help='Dossier de sortie')
    parser.add_argument('-r', '--recursive', action='store_true', help='Activer la recherche récursive')
    parser.add_argument('-d', '--depth', type=int, default=2, help='Profondeur maximale de recherche')
    parser.add_argument('-e', '--extensions', default='pdf,epub,mobi', help='Extensions de livres à rechercher')
    parser.add_argument('--no-manifest', action='store_true', help='Ne pas créer de manifest.json')

    args = parser.parse_args()

    global book_extensions
    book_extensions = ['.' + ext.strip().lstrip('.') for ext in args.extensions.split(',')]

    if args.url:
        url = args.url
        output_dir = args.output
        recursive = args.recursive
        max_depth = args.depth
    else:
        url, output_dir, recursive, max_depth = interactive_menu()

    if not is_valid_url(url):
        print(f"{Style.RED}[-] URL invalide : {url}{Style.RESET}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    banner()
    print(f"{Style.CYAN}[*] Cible : {url}{Style.RESET}")
    print(f"{Style.CYAN}[*] Dossier de sortie : {output_dir}{Style.RESET}")
    print(f"{Style.CYAN}[*] Recherche récursive : {'Oui' if recursive else 'Non'}{Style.RESET}")
    print(f"{Style.CYAN}[*] Profondeur : {max_depth}{Style.RESET}")
    print(f"{Style.CYAN}[*] Extensions : {', '.join(book_extensions)}{Style.RESET}\n")

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'BOOK-DOWN/1.0 (Educational Book Downloader)'
    })

    print(f"{Style.YELLOW}[!] Recherche des livres en cours...{Style.RESET}")
    books = discover_books(url, session, recursive=recursive, max_depth=max_depth)

    if not books:
        print(f"\n{Style.RED}[-] Aucun livre trouvé.{Style.RESET}")
        sys.exit(0)

    print(f"\n{Style.GREEN}[+] {len(books)} livre(s) trouvé(s).{Style.RESET}\n")

    successful_downloads = []
    total = len(books)

    for i, book_url in enumerate(books, 1):
        progress_bar("Téléchargement", i, total)
        success, info, size_kb = download_file(book_url, output_dir, session, i, total)
        if success:
            successful_downloads.append({
                'url': book_url,
                'filename': info,
                'size_kb': round(size_kb, 2)
            })

    print(f"\n\n{Style.GREEN}[+] Téléchargement terminé.{Style.RESET}")
    print(f"{Style.CYAN}[+] {len(successful_downloads)}/{total} livre(s) téléchargé(s) avec succès.{Style.RESET}")

    if not args.no_manifest:
        manifest_path = save_manifest(books, output_dir, successful_downloads)
        print(f"{Style.CYAN}[+] Manifest sauvegardé : {manifest_path}{Style.RESET}")

    print(f"\n{Style.YELLOW}[!] Rappel : utilisez ce script uniquement pour du contenu libre de droits.{Style.RESET}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Style.RED}[-] Interrompu par l'utilisateur.{Style.RESET}")
