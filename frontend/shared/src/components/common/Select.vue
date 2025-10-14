<template>
  <div :class="wrapperClasses">
    <!-- Label -->
    <label
      v-if="label"
      :for="selectId"
      class="block text-sm font-medium text-gray-700 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- Select Container -->
    <div class="relative">
      <select
        :id="selectId"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        :class="selectClasses"
        @change="handleChange"
        @blur="handleBlur"
        @focus="handleFocus"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option
          v-for="option in options"
          :key="getOptionValue(option)"
          :value="getOptionValue(option)"
          :disabled="option.disabled"
        >
          {{ getOptionLabel(option) }}
        </option>
      </select>

      <!-- Dropdown Icon -->
      <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
        <svg class="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </div>
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
    type: [String, Number, Boolean],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select an option'
  },
  options: {
    type: Array,
    required: true
  },
  valueKey: {
    type: String,
    default: 'value'
  },
  labelKey: {
    type: String,
    default: 'label'
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
  required: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'blur', 'focus'])

// Local state
const selectId = ref(`select-${Math.random().toString(36).substr(2, 9)}`)

// Computed
const wrapperClasses = computed(() => {
  return 'w-full'
})

const selectClasses = computed(() => {
  const classes = [
    'block w-full rounded-lg border transition-colors appearance-none',
    'focus:outline-none focus:ring-2 focus:ring-offset-0',
    'disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed',
    'pr-10' // Space for dropdown icon
  ]

  // Size classes
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-4 py-3 text-base'
  }
  classes.push(sizeClasses[props.size])

  // Error or normal state
  if (props.error) {
    classes.push('border-red-300 text-red-900 focus:ring-red-500 focus:border-red-500')
  } else {
    classes.push('border-gray-300 text-gray-900 focus:ring-neon-green focus:border-neon-green')
  }

  return classes.join(' ')
})

// Methods
function getOptionValue(option) {
  if (typeof option === 'object' && option !== null) {
    return option[props.valueKey]
  }
  return option
}

function getOptionLabel(option) {
  if (typeof option === 'object' && option !== null) {
    return option[props.labelKey]
  }
  return option
}

function handleChange(event) {
  const value = event.target.value
  emit('update:modelValue', value)
  emit('change', value)
}

function handleBlur(event) {
  emit('blur', event)
}

function handleFocus(event) {
  emit('focus', event)
}
</script>

<style scoped>
/* Remove default arrow in IE */
select::-ms-expand {
  display: none;
}
</style>
