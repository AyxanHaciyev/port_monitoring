#!/usr/bin/env python3
import os
import time
import subprocess
from datetime import datetime

# Konsol rəngləri (CLI üçün)
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def check_ports():
    # Ekranı təmizləyir və başlığı yeniləyir
    os.system('clear')
    print(f"{CYAN}======================================================================{RESET}")
    print(f"{GREEN}   CANLI PORT VƏ SERVİS MONITORİNQİ | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{CYAN}======================================================================{RESET}\n")

    # ROOT icazəsi yoxlanılır (Servis adları və PID-ləri tam görmək üçün vacibdir)
    if os.geteuid() != 0:
        print(f"{YELLOW}[!] XƏBƏRDARLIQ: Bütün servis adlarını görmək üçün skripti 'sudo' ilə işlədin.{RESET}\n")

    print(f"{'PROTOKOL':<10} {'YERLİ ÜNVAN VƏ PORT':<30} {'SERVİS VƏ PID'}")
    print("-" * 70)

    try:
        # Linux sistemində dinlənilən TCP/UDP portları çəkirik
        result = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')

        for line in lines[1:]:  # İlk başlığı keçirik
            parts = line.split()
            if len(parts) >= 5:
                proto = parts[0].upper()
                local_addr = parts[4]
                
                # Process / Servis məlumatını çıxarırıq
                process_info = parts[-1] if "users:" in parts[-1] else "İcazə yoxdur / Naməlum"
                
                if "users:" in process_info:
                    # Oxunması rahat formata salırıq
                    process_info = process_info.replace('users:(("', '').replace('",pid=', ' (PID: ').replace(',fd=', '))').replace('))', ')')

                print(f"{proto:<10} {local_addr:<30} {process_info}")

    except Exception as e:
        print(f"Xəta baş verdi: {e}")

def main():
    # Hər 5 saniyədən bir avtomatik olaraq CLI ekranını yeniləyir
    REFRESH_RATE = 5 
    try:
        while True:
            check_ports()
            time.sleep(REFRESH_RATE)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Monitorinq dayandırıldı.{RESET}")

if __name__ == "__main__":
    main()
