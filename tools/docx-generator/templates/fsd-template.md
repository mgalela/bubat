# Functional Specification Document (FSD) Template

> Template hasil ekstraksi dari 5 contoh PDF di `@fsd-template/`.
> Target: spesifikasi fungsional per fitur/modul. Format sumber: Markdown. Export: HTML/DOCX via tool Stage 05.

---

# FUNCTIONAL SPECIFICATION DOCUMENT

## [Nama Institusi / Program]
## [Nama Sistem / Produk]

## [Nama Fitur / Modul]

**Dipersiapkan oleh:** [Nama Vendor / Tim]

| Metadata | Nilai |
|----------|-------|
| Nomor Dokumen | [FSD-XXX-YYY-01] |
| Versi | [1.0.0] |
| Tanggal | [DD MMMM YYYY] |
| Status | Draft / Review / Final |
| Klasifikasi | Internal / Rahasia |

---

## Author

| Nama | Role |
|------|------|
| [Nama Penulis] | Technical Writer / Business Analyst |
| [Nama Reviewer] | Reviewer |
| [Nama Approver] | Approver |

## Detail Daftar Perubahan

| Versi | Tanggal Perubahan | Penulis | Deskripsi |
|-------|-------------------|---------|-----------|
| [1.0.0] | [DD MMMM YYYY] | [Nama] | Draft awal |

## Daftar Isi

> Gunakan heading dokumen ini sebagai sumber ToC otomatis di Word/DOCX.

---

## 1. Gambaran Umum

### 1.1. Latar Belakang
[Jelaskan masalah bisnis, konteks operasional, alasan fitur dibangun.]

### 1.2. Tujuan
- [Tujuan 1]
- [Tujuan 2]
- [Tujuan 3]

### 1.3. Ruang Lingkup
- [Proses utama dalam scope]
- [Integrasi dalam scope]
- [Validasi / aturan bisnis dalam scope]
- [Output / laporan dalam scope]

### 1.4. Definisi
| Istilah | Definisi |
|---------|----------|
| [Term] | [Definisi singkat] |

### 1.5. Objektif
- Dokumen ini menjelaskan detail kebutuhan fungsional fitur/modul.
- Gambar/mockup dipakai untuk mempermudah pemahaman alur dan field.
- Aplikasi ditujukan untuk [peran pengguna] dalam konteks [operasional].

### 1.6. Pengguna
| No | Pengguna | Deskripsi |
|----|----------|-----------|
| 1 | [Role 1] | [Tanggung jawab / tujuan] |
| 2 | [Role 2] | [Tanggung jawab / tujuan] |

---

## 2. Arsitektur Sistem

### 2.1. Arsitektur Sistem
[Diagram arsitektur / integrasi sistem]

**Keterangan:**
- [Komponen 1] → [Fungsi / pertukaran data]
- [Komponen 2] → [Fungsi / pertukaran data]

---

## 3. [Nama Fitur / Modul]

### 3.1. Alur Proses
#### 3.1.1. Alur Proses Utama
[Diagram flow / BPMN / sequence bisnis]

#### 3.1.2. Alur Proses Otorisasi / Override
[Diagram otorisasi bila ada. Jika tidak ada, tulis N/A.]

### 3.2. Keterangan Alur Proses
#### 3.2.1. Keterangan Alur Proses Utama
1. [Langkah 1]
2. [Langkah 2]
3. [Langkah 3]

#### 3.2.2. Keterangan Alur Proses Otorisasi / Override
1. [Langkah otorisasi 1]
2. [Langkah otorisasi 2]
3. [Langkah otorisasi 3]

### 3.3. Use Case
#### 3.3.1. Use Case Utama
| Elemen | Deskripsi |
|--------|-----------|
| Nama Use Case | [Nama use case] |
| Aktor | [Role] |
| Trigger | [Pemicu] |
| Pre-condition | [Kondisi awal] |
| Post-condition | [Kondisi akhir] |
| Alur Normal | [Ringkasan] |
| Alur Alternatif / Exception | [Ringkasan] |

#### 3.3.2. Use Case Otorisasi / Override
| Elemen | Deskripsi |
|--------|-----------|
| Nama Use Case | [Nama use case] |
| Aktor | [Role] |
| Trigger | [Pemicu] |
| Pre-condition | [Kondisi awal] |
| Post-condition | [Kondisi akhir] |
| Alur Normal | [Ringkasan] |
| Alur Alternatif / Exception | [Ringkasan] |

### 3.4. Mockup
#### 3.4.1. Mockup Form / Halaman Utama
[Sisipkan gambar mockup]

#### 3.4.2. Mockup Dialog / Pencarian / Detail
[Sisipkan gambar mockup]

### 3.5. Field Description
#### 3.5.1. Field Description [Nama Form / Tab]
| No | Field | Tipe / Control | Mandatory | Source / Default | Deskripsi / Aturan |
|----|-------|----------------|-----------|------------------|--------------------|
| 1 | [Nama field] | Textbox / Dropdown | Ya / Tidak | [Sumber] | [Aturan] |

> Tambah subsection 3.5.x per tab/form seperti pola contoh PDF.

### 3.6. Action
#### 3.6.1. Action – [Nama Halaman / Tab]
| Action | Output | Keterangan |
|--------|--------|------------|
| Klik tombol [Filter] | [Hasil sistem] | [Catatan] |
| Klik tombol [Reset] | [Hasil sistem] | [Catatan] |
| Klik tombol [Submit] | [Hasil sistem] | [Catatan] |

### 3.7. Tabel Validasi
| Kondisi / Input | Respons Sistem |
|-----------------|----------------|
| [Kondisi validasi 1] | [Output / error / next state] |
| [Kondisi validasi 2] | [Output / error / next state] |

---

## 4. Pengaturan Umum

### 4.1. Pengaturan
| Konfigurasi | Keterangan |
|-------------|------------|
| [Single Session / Timeout / Role Matrix] | [Penjelasan] |

---

## Persetujuan Dokumen [Pihak Klien]

| Nama | Jabatan | Status | Tanggal | Tanda Tangan |
|------|---------|--------|---------|--------------|
| [Nama] | [Jabatan] | Approved / Review | [Tanggal] | [TTD] |

## Persetujuan Dokumen [Pihak Penyusun]

| Nama | Jabatan | Status | Tanggal | Tanda Tangan |
|------|---------|--------|---------|--------------|
| [Nama] | [Jabatan] | Approved / Review | [Tanggal] | [TTD] |

---

## Catatan Ekstraksi

- Struktur dasar muncul konsisten di 5 contoh PDF: `Gambaran Umum` → `Arsitektur Sistem` → `Detail Fitur` → `Pengaturan Umum` → `Persetujuan`.
- Bagian paling bervariasi: jumlah mockup, jumlah subsection field description, nama use case, detail action.
- Untuk fitur read-only, subsection otorisasi bisa diberi `N/A`.
- Untuk fitur kompleks, tambahkan `3.4.x`, `3.5.x`, `3.6.x` sesuai jumlah tab/form.
