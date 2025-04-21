# Lazy-Edgexnet

Program untuk melakukan pendaftaran akun diplatform edgex network disertai kode referral secara otomatis.

## Fitur

* pendaftaran akun otomatis (fitur utama)
* mendukung penggunaan proxy (hanya protokol http)

## Diskusi

Jika anda memiliki pertanyaan silahkan bertanya di grup berikut
[https://t.me/sdsproject_chat](https://t.me/sdsproject_chat)

## Provider Proxy

Provider proxy yang kompatibel:

1. [Proxy-Cheap](https://app.proxy-cheap.com/r/mlShoy)
2. [DataImpulse](https://dataimpulse.com/?aff=48082) (`Harga $1/gb untuk pengguna baru!`)
3. [ProxiesFO](https://app.proxies.fo/ref/c02fda06-da42-f640-7ef7-885127487ef0)


## Instalasi

### Persyaratan

* Python3.8+
* Git
* Kode referral platform edgex network

### Konfigurasi

* Edit file referral_code.txt
	Isi kode referral anda di file ini
* Edit file proxies.txt
	Anda bisa menambahkan proxy yang anda miliki difile ini jika ingin menggunakan proxy, Lihat [Provider Proxy](#provider-proxy) untuk rekomentasi provider proxy.

	Format yang harus digunakan untuk proxy sebagai berikut

	Jika proxy menggunakan autentikasi :

	```
	Format
	http://user:password@proxy_server:proxy_port

	Contoh
	http://admin:admin@192.168.1.1:8080
	```

	Jika proxy tidak menggunakan autentikasi :

	```
	Format
	http://proxy_server:proxy_port

	Contoh
	http://192.168.1.1:8000
	```