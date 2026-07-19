import apiClient from './api'

export const checkText = async (text) => {
  try {
    const response = await apiClient.post('/api/check/text', { text })
    return { success: true, data: response.data }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Terjadi kesalahan pada server'
    }
  }
}

export const checkImage = async (imageFile, caption) => {
  try {
    const formData = new FormData()
    formData.append('image', imageFile)
    formData.append('caption', caption)

    const response = await apiClient.post('/api/check/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return { success: true, data: response.data }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Terjadi kesalahan pada server'
    }
  }
}

export const checkVideo = async (videoFile, caption) => {
  try {
    const formData = new FormData()
    formData.append('video', videoFile)
    formData.append('caption', caption)

    const response = await apiClient.post('/api/check/video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return { success: true, data: response.data }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Terjadi kesalahan pada server'
    }
  }
}