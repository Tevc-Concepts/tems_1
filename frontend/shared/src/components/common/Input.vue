<template>
  <div :class="wrapperClasses">
    <!-- Label -->
    <label
      v-if="label"
      :for="inputId"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- Input Container -->
    <div class="relative">
      <!-- Prefix Icon -->
      <div v-if="prefixIcon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <component :is="prefixIcon" class="h-5 w-5 text-gray-400" />
      </div>

      <!-- Input -->
      <input
        :id="inputId"
        :type="inputType"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :autocomplete="autocomplete"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />

      <!-- Suffix Icon / Clear Button -->
      <div v-if="suffixIcon || (clearable && modelValue)" class="absolute inset-y-0 right-0 pr-3 flex items-center">
        <button
          v-if="clearable && modelValue"
          type="button"
          @click="handleClear"
          class="text-gray-400 hover:text-gray-600 focus:outline-none"
        >
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
          </svg>
        </button>
        <component v-else-if="suffixIcon" :is="suffixIcon" class="h-5 w-5 text-gray-400" />
      </div>

      <!-- Password Toggle -->
      <button
        v-if="type === 'password'"
        type="button"
        @click="togglePasswordVisibility"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 focus:outline-none"
      >
        <svg v-if="showPassword" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        </svg>
        <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
        </svg>
      </button>
    </div>

    <!-- Helper Text / Error -->
    <p
      v-if="helperText || error"
      :class="[
        'mt-1 text-sm',
        error ? 'text-red-600' : 'text-gray-500'
      ]"
    >
      {{ error || helperText }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  helperText: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  clearable: {
    type: Boolean,
    default: false
  },
  prefixIcon: {
    type: [Object, String],
    default: null
  },
  suffixIcon: {
    type: [Object, String],
    default: null
  },
  autocomplete: {
    type: String,
    default: 'off'
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'clear'])

// Local state
const showPassword = ref(false)
const inputId = ref(`input-${Math.random().toString(36).substr(2, 9)}`)

// Computed
const inputType = computed(() => {
  if (props.type === 'password') {
    return showPassword.value ? 'text' : 'password'
  }
  return props.type
})

const wrapperClasses = computed(() => {
  return 'w-full'
})

const inputClasses = computed(() => {
  const classes = [
    'block w-full rounded-lg border transition-colors',
    'focus:outline-none focus:ring-2 focus:ring-offset-0',
    'disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed'
  ]

  // Size classes
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-4 py-3 text-base'
  }
  classes.push(sizeClasses[props.size])

  // Icon padding
  if (props.prefixIcon) {
    classes.push('pl-10')
  }
  if (props.suffixIcon || props.clearable || props.type === 'password') {
    classes.push('pr-10')
  }

  // Error or normal state
  if (props.error) {
    classes.push('border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500')
  } else {
    classes.push('border-gray-300 text-gray-900 placeholder-gray-400 focus:ring-neon-green focus:border-neon-green')
  }

  return classes.join(' ')
})

// Methods
function handleInput(event) {
  emit('update:modelValue', event.target.value)
}

function handleBlur(event) {
  emit('blur', event)
}

function handleFocus(event) {
  emit('focus', event)
}

function handleClear() {
  emit('update:modelValue', '')
  emit('clear')
}

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
