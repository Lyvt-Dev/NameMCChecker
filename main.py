import itertools
import string
import time
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore
from multiprocessing import Pool, cpu_count, Manager, Process

init(autoreset=True)

SLEEP_TIME = 0  # seconds between requests (it should work on 0 but if you have problems on 0 make it to 0,5)

def get_user_input():
    length = int(input("🧱 How many characters should the name have? (3-16): "))
    if not 3 <= length <= 16:
        print(Fore.RED + "❌ Invalid length!")
        exit()

    use_numbers = input("🔢 Allow numbers? (y/n): ").lower() == 'y'
    use_underscore = input("⛓️ Allow underscore '_'? (y/n): ").lower() == 'y'
    use_dash = input("➖ Allow dash '-'? (y/n): ").lower() == 'y'

    max_cores = cpu_count()
    print(Fore.MAGENTA + f"🧠 You have {max_cores} CPU cores available.")
    while True:
        try:
            instances = int(input(f"⚙️  How many instances do you want to use? (1–{max_cores}): "))
            if 1 <= instances <= max_cores:
                break
            else:
                print(Fore.RED + f"❌ Please enter a number between 1 and {max_cores}.")
        except ValueError:
            print(Fore.RED + "❌ Invalid input.")

    return length, use_numbers, use_underscore, use_dash, instances

def generate_characters(use_numbers, use_underscore, use_dash):
    chars = list(string.ascii_lowercase)
    if use_numbers:
        chars += list(string.digits)
    if use_underscore:
        chars.append('_')
    if use_dash:
        chars.append('-')
    return chars

def generate_names(length, chars):
    return [''.join(name) for name in itertools.product(chars, repeat=length)]

def is_name_available(name):
    url = f"https://de.namemc.com/profile/{name}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return soup.find("h3", string="Username is available!") is not None
    except:
        pass
    return False

def check_chunk(name_chunk, checked_count, found_count, lock):
    found = []
    for name in name_chunk:
        if is_name_available(name):
            print(Fore.GREEN + f"✅ Available: {name}")
            found.append(name)
            with lock:
                found_count.value += 1
        time.sleep(SLEEP_TIME)
        with lock:
            checked_count.value += 1
    return found

def save_to_file(names, filename="names.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")

def live_timer(start_time, total, checked_count, found_count):
    while checked_count.value < total:
        elapsed = time.time() - start_time

        avg_time_per_name = elapsed / max(1, checked_count.value)
        names_left = total - checked_count.value
        eta_seconds = avg_time_per_name * names_left

        print(Fore.YELLOW + f"[⏱ {format_time(elapsed)}] {checked_count.value}/{total} checked – {found_count.value} available – ETA: {format_time(eta_seconds)}", end='\r')
        time.sleep(1)

    elapsed = time.time() - start_time
    print(Fore.YELLOW + f"\n✅ Finished in {format_time(elapsed)} – {found_count.value} names available.")

def format_time(seconds):
    minutes = int(seconds) // 60
    hours = minutes // 60
    return f"{int(hours):02d}:{int(minutes % 60):02d}:{int(seconds % 60):02d}"

def main():
    length, use_numbers, use_underscore, use_dash, instances = get_user_input()
    chars = generate_characters(use_numbers, use_underscore, use_dash)
    all_names = generate_names(length, chars)
    total = len(all_names)

    print(Fore.CYAN + f"\n📦 Generated combinations: {total}")
    print(Fore.CYAN + f"🚀 Starting {instances} instances with live timer...\n")

    chunk_size = total // instances
    name_chunks = [all_names[i:i+chunk_size] for i in range(0, total, chunk_size)]

    with Manager() as manager:
        checked_count = manager.Value('i', 0)
        found_count = manager.Value('i', 0)
        lock = manager.Lock()
        start_time = time.time()

        timer_process = Process(target=live_timer, args=(start_time, total, checked_count, found_count))
        timer_process.start()

        with Pool(processes=instances) as pool:
            results = [pool.apply_async(check_chunk, (chunk, checked_count, found_count, lock)) for chunk in name_chunks]
            all_available = []
            for r in results:
                all_available.extend(r.get())

        timer_process.join()
        save_to_file(all_available)
        print(Fore.GREEN + f"\n📁 {len(all_available)} available names saved in 'names.txt'.")

if __name__ == "__main__":
    main()
