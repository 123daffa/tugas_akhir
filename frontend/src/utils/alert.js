import Swal from 'sweetalert2'

// Toast kecil di pojok kanan atas, otomatis hilang -- dipakai untuk notifikasi
// sukses yang tidak perlu diklik/dikonfirmasi user (mis. login/register berhasil).
const Toast = Swal.mixin({
  toast: true,
  position: 'top-end',
  showConfirmButton: false,
  timer: 2500,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.onmouseenter = Swal.stopTimer
    toast.onmouseleave = Swal.resumeTimer
  }
})

export function showSuccess(message, title = 'Berhasil') {
  Toast.fire({
    icon: 'success',
    title,
    text: message,
    iconColor: '#20d48a'
  })
}

export function showSuccessRegis(message, title = 'Berhasil') {
  Swal.fire({
    icon: 'success',
    title,
    text: message,
    iconColor: '#20d48a'
  })
}

// Dialog blocking di tengah layar -- dipakai untuk error, supaya user pasti
// membaca alasan gagalnya sebelum lanjut (mis. login/register gagal).
export function showError(message, title = 'Gagal') {
  Swal.fire({
    icon: 'error',
    title,
    text: message,
    confirmButtonText: 'Coba Lagi',
    confirmButtonColor: '#111827'
  })
}

export function showConfirm(message, title = 'Konfirmasi', confirmLabel = 'Ya, lanjutkan') {
  return Swal.fire({
    icon: 'warning',
    title,
    text: message,
    showCancelButton: true,
    confirmButtonText: confirmLabel,
    cancelButtonText: 'Batal',
    confirmButtonColor: '#ff4d4d',
    cancelButtonColor: '#66BB6A',
    color: '#111827',
    customClass: {
      cancelButton: 'swal-cancel-btn-dark-text'
    }
  }).then((result) => result.isConfirmed)
}

export async function confirmAndDelete({
  title = 'Yakin mau menghapus?',
  text = 'Data yang sudah dihapus tidak bisa dikembalikan.',
  successText = 'Data berhasil dihapus.',
  onConfirm
}) {
  const result = await Swal.fire({
    title,
    text,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Ya, hapus!',
    cancelButtonText: 'Batal',
    reverseButtons: true,
    confirmButtonColor: '#ff4d4d',
    cancelButtonColor: '#66BB6A',
    color: '#111827'
  })

  if (!result.isConfirmed) return false

  try {
    await onConfirm()
    await Swal.fire({
      title: 'Terhapus!',
      text: successText,
      icon: 'success',
      confirmButtonColor: '#111827'
    })
    return true
  } catch (err) {
    const message = err.response?.data?.message || 'Terjadi kesalahan, coba lagi.'
    Swal.fire({
      title: 'Gagal Menghapus',
      text: message,
      icon: 'error',
      confirmButtonColor: '#111827'
    })
    return false
  }
}

export function showLoading(message = 'Memproses...') {
  Swal.fire({
    title: message,
    allowOutsideClick: false,
    allowEscapeKey: false,
    showConfirmButton: false,
    didOpen: () => {
      Swal.showLoading()
    }
  })
}

export function closeLoading() {
  Swal.close()
}