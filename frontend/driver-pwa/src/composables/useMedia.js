import { ref, computed } from 'vue'

export function useCamera() {
    const stream = ref(null)
    const videoElement = ref(null)
    const error = ref(null)
    const isActive = ref(false)

    const isCameraSupported = computed(() => {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
    })

    async function startCamera(videoRef, facingMode = 'environment') {
        if (!isCameraSupported.value) {
            error.value = new Error('Camera not supported on this device')
            throw error.value
        }

        try {
            const constraints = {
                video: {
                    facingMode: facingMode, // 'user' for front camera, 'environment' for back
                    width: { ideal: 1920 },
                    height: { ideal: 1080 }
                },
                audio: false
            }

            stream.value = await navigator.mediaDevices.getUserMedia(constraints)

            if (videoRef) {
                videoElement.value = videoRef
                videoRef.srcObject = stream.value
                await videoRef.play()
                isActive.value = true
            }

            return stream.value
        } catch (err) {
            error.value = err
            throw err
        }
    }

    function stopCamera() {
        if (stream.value) {
            stream.value.getTracks().forEach(track => track.stop())
            stream.value = null
            isActive.value = false
        }

        if (videoElement.value) {
            videoElement.value.srcObject = null
        }
    }

    function capturePhoto() {
        if (!videoElement.value || !isActive.value) {
            throw new Error('Camera not active')
        }

        const canvas = document.createElement('canvas')
        canvas.width = videoElement.value.videoWidth
        canvas.height = videoElement.value.videoHeight

        const ctx = canvas.getContext('2d')
        ctx.drawImage(videoElement.value, 0, 0)

        return new Promise((resolve) => {
            canvas.toBlob((blob) => {
                resolve({
                    blob: blob,
                    dataUrl: canvas.toDataURL('image/jpeg', 0.9)
                })
            }, 'image/jpeg', 0.9)
        })
    }

    async function switchCamera() {
        if (!isActive.value) return

        const currentFacingMode = stream.value
            .getVideoTracks()[0]
            .getSettings().facingMode

        const newFacingMode = currentFacingMode === 'user' ? 'environment' : 'user'

        stopCamera()
        await startCamera(videoElement.value, newFacingMode)
    }

    return {
        stream,
        videoElement,
        error,
        isActive,
        isCameraSupported,
        startCamera,
        stopCamera,
        capturePhoto,
        switchCamera
    }
}

// Voice recording composable
export function useVoiceRecorder() {
    const mediaRecorder = ref(null)
    const audioChunks = ref([])
    const isRecording = ref(false)
    const error = ref(null)
    const recordingDuration = ref(0)
    const durationInterval = ref(null)

    const isSupported = computed(() => {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
    })

    async function startRecording() {
        if (!isSupported.value) {
            error.value = new Error('Audio recording not supported')
            throw error.value
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

            mediaRecorder.value = new MediaRecorder(stream)
            audioChunks.value = []
            recordingDuration.value = 0

            mediaRecorder.value.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.value.push(event.data)
                }
            }

            mediaRecorder.value.start()
            isRecording.value = true

            // Track duration
            durationInterval.value = setInterval(() => {
                recordingDuration.value++
            }, 1000)

        } catch (err) {
            error.value = err
            throw err
        }
    }

    function stopRecording() {
        return new Promise((resolve) => {
            if (!mediaRecorder.value || !isRecording.value) {
                resolve(null)
                return
            }

            mediaRecorder.value.onstop = () => {
                const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })

                // Stop all tracks
                mediaRecorder.value.stream.getTracks().forEach(track => track.stop())

                isRecording.value = false
                clearInterval(durationInterval.value)

                resolve({
                    blob: audioBlob,
                    duration: recordingDuration.value
                })
            }

            mediaRecorder.value.stop()
        })
    }

    function cancelRecording() {
        if (mediaRecorder.value && isRecording.value) {
            mediaRecorder.value.stop()
            mediaRecorder.value.stream.getTracks().forEach(track => track.stop())
            isRecording.value = false
            clearInterval(durationInterval.value)
            audioChunks.value = []
            recordingDuration.value = 0
        }
    }

    return {
        isRecording,
        error,
        isSupported,
        recordingDuration,
        startRecording,
        stopRecording,
        cancelRecording
    }
}
