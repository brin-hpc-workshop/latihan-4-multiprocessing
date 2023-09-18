# Latihan 4 - Multiprocessing

Pada latihan kali ini kita akan mengubah fungsi `plot_animasi` yang sudah kita buat pada Latihan 1 untuk dapat dijalankan dengan menggunakan *library* `multiprocessing`.

Ikuti instruksi berikut untuk menyelesaikan latihan ini.

1. Buatlah fungsi `plot_animasi_mp` yang sama dengan `plot_animasi`.
2. Tambahkan beberapa argumen di fungsi `plot_animasi_mp` untuk dapat melakukan *plotting* tanpa harus melakukan load ulang data.
3. Catat waktu total yang dibutuhkan untuk melakukan *plotting* dengan menggunakan `plot_animasi_mp` dan `Pool` untuk beberapa nilai `n_pool = 1, 2, 4, 8`.
