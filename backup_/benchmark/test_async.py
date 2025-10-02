import asyncio
import aiohttp
import time
import json

# --- KONFIGURASI TARGET API ---
# Definisikan setiap API yang ingin di-hit di sini.
# Setiap item adalah dictionary yang berisi:
# 'name': Nama unik untuk identifikasi
# 'url': URL endpoint API
# 'payload': Data JSON yang akan dikirim
API_TARGETS = [
    {
        "name": "Service 1",
        "url": "http://httpbin.org/post",  # Ganti dengan http_url1 Anda
        "payload": {"user_id": 123, "action": "login", "source": "mobile"} # Ganti dengan payload1
    },
    {
        "name": "Service 2",
        "url": "http://httpbin.org/post",  # Ganti dengan http_url2 Anda
        "payload": {"product_id": "XYZ-001", "quantity": 2, "cart_id": "c7a8b"} # Ganti dengan payload2
    },
    {
        "name": "Service 3",
        "url": "http://httpbin.org/post",  # Ganti dengan http_url3 Anda
        "payload": {"query": "search term", "filter": "last_24_hours"} # Ganti dengan payload3
    }
]

# --- PENGATURAN TEST ---
# Berapa kali setiap API akan di-hit
REQUESTS_PER_API = 50

# --- SCRIPT UTAMA ---

async def hit_api(session: aiohttp.ClientSession, name: str, url: str, payload: dict, request_num: int):
    """
    Fungsi untuk mengirim satu request POST asinkron ke sebuah API.
    """
    start_time = time.monotonic()
    try:
        # Menggunakan session.post untuk mengirim data JSON
        # aiohttp akan otomatis mengatur header 'Content-Type: application/json'
        async with session.post(url, json=payload) as response:
            # Membaca respons sebagai JSON
            response_json = await response.json()
            duration = time.monotonic() - start_time
            
            # response.status adalah kode status HTTP (misal: 200, 404, 500)
            print(
                f"[{name: <10}] [Req #{request_num: <3}] "
                f"Selesai dalam {duration:.4f} dtk | "
                f"Status: {response.status}"
            )
            # Opsional: Cetak data yang diterima dari API untuk verifikasi
            # print(json.dumps(response_json, indent=2))
            
            return (name, duration, response.status, None)

    except aiohttp.ClientConnectorError as e:
        duration = time.monotonic() - start_time
        error_message = f"Koneksi Gagal: {e}"
        print(f"[{name: <10}] [Req #{request_num: <3}] ERROR: {error_message}")
        return (name, duration, None, error_message)
    except Exception as e:
        duration = time.monotonic() - start_time
        error_message = f"Terjadi Error: {e}"
        print(f"[{name: <10}] [Req #{request_num: <3}] ERROR: {error_message}")
        return (name, duration, None, error_message)


async def main():
    """
    Fungsi utama untuk membuat session, menyiapkan semua tugas (tasks),
    dan menjalankannya secara bersamaan.
    """
    total_requests = len(API_TARGETS) * REQUESTS_PER_API
    print("--- Memulai Uji Beban API Async ---")
    print(f"Total requests: {total_requests} ({REQUESTS_PER_API} per API)")
    print("---------------------------------------------")

    # Membuat satu aiohttp.ClientSession yang akan digunakan kembali
    # untuk semua request. Ini jauh lebih efisien.
    async with aiohttp.ClientSession() as session:
        # Membuat daftar semua tugas (coroutine) yang akan dijalankan
        tasks = []
        for api_config in API_TARGETS:
            for i in range(1, REQUESTS_PER_API + 1):
                task = asyncio.create_task(
                    hit_api(
                        session=session,
                        name=api_config["name"],
                        url=api_config["url"],
                        payload=api_config["payload"],
                        request_num=i
                    )
                )
                tasks.append(task)
        
        # Menjalankan semua tugas secara bersamaan dan menunggu hasilnya
        overall_start_time = time.monotonic()
        results = await asyncio.gather(*tasks)
        overall_duration = time.monotonic() - overall_start_time

    # --- Analisis Hasil ---
    print("\n--- Uji Beban Selesai ---")
    print(f"Total waktu eksekusi: {overall_duration:.4f} detik.")
    
    success_count = sum(1 for r in results if r[3] is None and r[2] is not None and 200 <= r[2] < 300)
    error_count = len(results) - success_count
    
    print(f"Total request berhasil (status 2xx): {success_count}")
    print(f"Total request gagal atau error      : {error_count}")

    if success_count > 0:
        avg_request_time = sum(r[1] for r in results if r[3] is None) / success_count
        print(f"Rata-rata waktu request: {avg_request_time:.4f} detik.")

        # Rata-rata per API
        for api_config in API_TARGETS:
            name = api_config["name"]
            api_times = [r[1] for r in results if r[0] == name and r[3] is None]
            if api_times:
                avg_api_time = sum(api_times) / len(api_times)
                print(f"  - Rata-rata waktu untuk {name:<10}: {avg_api_time:.4f} detik.")


if __name__ == "__main__":
    # Menjalankan loop event asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nPengujian dihentikan oleh pengguna.")