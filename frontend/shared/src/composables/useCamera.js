import { ref } from 'vue'

/**
 * Camera composable for capturing photos
 * Supports front and back cameras with compression
 * 
 * @returns {object} Camera state and methods
 * 
 * @example
 * ```javascript
 * import { useCamera } from '@shared/composables/useCamera'
 * 
 * const { capturePhoto, stream, error } = useCamera()
 * 
 * // Capture from back camera
 * const imageData = await capturePhoto('back')
 * 
 * // Capture from front camera
 * const selfie = await capturePhoto('front')
 * ```
 */
export function useCamera() {
    const stream = ref(null)
    const error = ref(null)
    const isActive = ref(false)

    /**
     * Start camera stream
     * @param {string} facingMode - 'user' (front) or 'environment' (back)
     */
    async function startCamera(facingMode = 'environment') {
        try {
            error.value = null

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Camera not supported by your browser')
            }

            // Stop existing stream if any
            if (stream.value) {
                stopCamera()
            }

            const constraints = {
                video: {
                    facingMode: facingMode,
                    width: { ideal: 1920 },
                    height: { ideal: 1080 }
                }
            }

            stream.value = await navigator.mediaDevices.getUserMedia(constraints)
            isActive.value = true

            return stream.value
        } catch (err) {
            error.value = err
            throw err
        }
    }

    /**
     * Stop camera stream
     */
    function stopCamera() {
        if (stream.value) {
            stream.value.getTracks().forEach(track => track.stop())
            stream.value = null
            isActive.value = false
        }
    }

    /**
     * Capture photo from camera
     * @param {string} facingMode - 'front' or 'back'
     * @param {object} options - Capture options
     * @returns {Promise<string>} Base64 image data
     */
    async function capturePhoto(facingMode = 'back', options = {}) {
        const {
            quality = 0.8,
            maxWidth = 1920,
            maxHeight = 1080,
            format = 'image/jpeg'
        } = options

        try {
            error.value = null

            // Convert facingMode to MediaDevices constraint
            const facing = facingMode === 'front' ? 'user' : 'environment'

            // Start camera
            const cameraStream = await startCamera(facing)

            // Create video element
            const video = document.createElement('video')
            video.srcObject = cameraStream
            video.autoplay = true
            video.playsInline = true

            // Wait for video to be ready
            await new Promise((resolve) => {
                video.onloadedmetadata = () => {
                    video.play()
                    resolve()
                }
            })

            // Small delay to ensure camera is ready
            await new Promise(resolve => setTimeout(resolve, 500))

            // Create canvas and capture frame
            const canvas = document.createElement('canvas')
            const context = canvas.getContext('2d')

            // Calculate dimensions maintaining aspect ratio
            let width = video.videoWidth
            let height = video.videoHeight

            if (width > maxWidth) {
                height = (height * maxWidth) / width
                width = maxWidth
            }
            if (height > maxHeight) {
                width = (width * maxHeight) / height
                height = maxHeight
            }

            canvas.width = width
            canvas.height = height

            // Draw video frame to canvas
            context.drawImage(video, 0, 0, width, height)

            // Convert to base64
            const imageData = canvas.toDataURL(format, quality)

            // Cleanup
            stopCamera()

            return imageData
        } catch (err) {
            error.value = err
            stopCamera()
            throw err
        }
    }

    /**
     * Compress image
     * @param {string} imageData - Base64 image data
     * @param {object} options - Compression options
     * @returns {Promise<string>} Compressed base64 image
     */
    async function compressImage(imageData, options = {}) {
        const {
            quality = 0.8,
            maxWidth = 1920,
            maxHeight = 1080,
            format = 'image/jpeg'
        } = options

        return new Promise((resolve, reject) => {
            const img = new Image()

            img.onload = () => {
                const canvas = document.createElement('canvas')
                const context = canvas.getContext('2d')

                let width = img.width
                let height = img.height

                // Maintain aspect ratio
                if (width > maxWidth) {
                    height = (height * maxWidth) / width
                    width = maxWidth
                }
                if (height > maxHeight) {
                    width = (width * maxHeight) / height
                    height = maxHeight
                }

                canvas.width = width
                canvas.height = height

                context.drawImage(img, 0, 0, width, height)

                const compressed = canvas.toDataURL(format, quality)
                resolve(compressed)
            }

            img.onerror = reject
            img.src = imageData
        })
    }

    /**
     * Convert base64 to Blob
     * @param {string} base64 - Base64 string
     * @returns {Blob}
     */
    function base64ToBlob(base64) {
        const parts = base64.split(';base64,')
        const contentType = parts[0].split(':')[1]
        const raw = window.atob(parts[1])
        const rawLength = raw.length
        const uInt8Array = new Uint8Array(rawLength)

        for (let i = 0; i < rawLength; ++i) {
            uInt8Array[i] = raw.charCodeAt(i)
        }

        return new Blob([uInt8Array], { type: contentType })
    }

    /**
     * Convert base64 to File
     * @param {string} base64 - Base64 string
     * @param {string} filename - File name
     * @returns {File}
     */
    function base64ToFile(base64, filename = 'photo.jpg') {
        const blob = base64ToBlob(base64)
        return new File([blob], filename, { type: blob.type })
    }

    /**
     * Check if camera is available
     * @returns {boolean}
     */
    function isCameraAvailable() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
    }

    return {
        // State
        stream,
        error,
        isActive,

        // Actions
        startCamera,
        stopCamera,
        capturePhoto,

        // Utilities
        compressImage,
        base64ToBlob,
        base64ToFile,
        isCameraAvailable
    }
}
