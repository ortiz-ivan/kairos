/**
 * Form Validation System
 * Sistema de validación progresiva y feedback visual en tiempo real
 */

class FormValidator {
  constructor(formSelector) {
    this.form = document.querySelector(formSelector);
    if (!this.form) {
      console.error(`Form ${formSelector} not found`);
      return;
    }

    this.validationRules = {};
    this.setupEventListeners();
  }

  /**
   * Configura las reglas de validación para un campo
   */
  addRule(fieldName, rules) {
    this.validationRules[fieldName] = rules;
    return this;
  }

  /**
   * Configura los event listeners para validación en tiempo real
   */
  setupEventListeners() {
    // Validar mientras escriben (debounce 300ms)
    this.form.querySelectorAll('input, textarea').forEach((field) => {
      field.addEventListener('input', () => this.debounceValidate(field, 300));
      field.addEventListener('blur', () => this.validateField(field));
    });

    // Submit form
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  /**
   * Debounce para no validar demasiado frecuentemente
   */
  debounceValidate(field, delay = 300) {
    clearTimeout(field._validateTimeout);
    field._validateTimeout = setTimeout(() => {
      this.validateField(field);
    }, delay);
  }

  /**
   * Valida un campo específico
   */
  validateField(field) {
    const fieldName = field.name;
    if (!fieldName || !this.validationRules[fieldName]) {
      return true; // Sin reglas definidas
    }

    const rules = this.validationRules[fieldName];
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';

    // Aplicar reglas
    for (const rule of rules) {
      const result = rule.validate(value, field);
      if (!result.valid) {
        isValid = false;
        errorMessage = result.message;
        break; // Mostrar solo el primer error
      }
    }

    // Actualizar UI
    this.updateFieldUI(field, isValid, errorMessage);
    return isValid;
  }

  /**
   * Actualiza los estados visuales del campo
   */
  updateFieldUI(field, isValid, errorMessage = '') {
    // Limpiar estados previos
    field.classList.remove('is-valid', 'is-invalid');
    const existingError = field.parentElement.querySelector('.error-message');
    if (existingError) existingError.remove();

    // Actualizar estado
    if (field.value.trim() === '') {
      // Campo vacío
      field.classList.remove('is-valid', 'is-invalid');
    } else if (isValid) {
      field.classList.add('is-valid');
    } else {
      field.classList.add('is-invalid');
      if (errorMessage) {
        const errorEl = document.createElement('span');
        errorEl.className = 'error-message';
        errorEl.textContent = errorMessage;
        field.parentElement.appendChild(errorEl);
      }
    }
  }

  /**
   * Maneja el submit del formulario
   */
  handleSubmit(e) {
    e.preventDefault();

    // Validar todos los campos
    const fields = this.form.querySelectorAll('input, textarea');
    let formIsValid = true;

    fields.forEach((field) => {
      const isValid = this.validateField(field);
      if (!isValid) formIsValid = false;
    });

    if (formIsValid) {
      this.submitForm();
    }
  }

  /**
   * Envía el formulario (override en subclases si es necesario)
   */
  submitForm() {
    this.form.submit();
  }

  /**
   * Limpia los errores del formulario
   */
  clearErrors() {
    this.form.querySelectorAll('.error-message').forEach((el) => el.remove());
    this.form.querySelectorAll('input, textarea').forEach((field) => {
      field.classList.remove('is-valid', 'is-invalid');
    });
  }
}

/**
 * Reglas de validación comunes
 */
const ValidationRules = {
  // Required
  required: {
    validate: (value) => ({
      valid: value.length > 0,
      message: 'Este campo es obligatorio',
    }),
  },

  // Email
  email: {
    validate: (value) => ({
      valid:
        value.length === 0 ||
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
      message: 'Por favor ingresa un email válido',
    }),
  },

  // Mínimo de caracteres
  minLength: (length) => ({
    validate: (value) => ({
      valid: value.length === 0 || value.length >= length,
      message: `Mínimo ${length} caracteres`,
    }),
  }),

  // Máximo de caracteres
  maxLength: (length) => ({
    validate: (value) => ({
      valid: value.length <= length,
      message: `Máximo ${length} caracteres`,
    }),
  }),

  // Contraseña fuerte (8+ chars, mayúscula, número, especial)
  strongPassword: {
    validate: (value) => {
      if (value.length === 0) return { valid: true };
      const hasMinLength = value.length >= 8;
      const hasUppercase = /[A-Z]/.test(value);
      const hasNumber = /[0-9]/.test(value);
      const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(value);
      const valid = hasMinLength && hasUppercase && hasNumber && hasSpecial;

      if (!valid) {
        const missing = [];
        if (!hasMinLength) missing.push('8+ caracteres');
        if (!hasUppercase) missing.push('mayúscula');
        if (!hasNumber) missing.push('número');
        if (!hasSpecial) missing.push('carácter especial');
        return {
          valid: false,
          message: `Contraseña débil. Necesita: ${missing.join(', ')}`,
        };
      }

      return { valid: true };
    },
  },

  // Coincidencia de campos (ej: confirmar contraseña)
  matches: (otherFieldSelector) => ({
    validate: (value, field) => {
      const otherField = document.querySelector(otherFieldSelector);
      const otherValue = otherField ? otherField.value : '';
      return {
        valid: value === otherValue,
        message: `Los campos no coinciden`,
      };
    },
  }),

  // Verificación remota (ej: username disponible)
  async: (asyncValidateFn) => ({
    validate: async (value, field) => {
      if (value.length === 0) return { valid: true };
      return await asyncValidateFn(value, field);
    },
  }),

  // Patrón regex personalizado
  pattern: (regex, message) => ({
    validate: (value) => ({
      valid: value.length === 0 || regex.test(value),
      message: message || 'Formato inválido',
    }),
  }),
};

/**
 * Password Toggle Component
 * Mostrar/ocultar contraseña
 */
class PasswordToggle {
  constructor() {
    this.setupToggleButtons();
  }

  setupToggleButtons() {
    document.querySelectorAll('.password-toggle-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const input = btn.closest('.password-toggle')?.querySelector('input');
        if (!input) return;

        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';

        // Cambiar ícono
        const icon = btn.querySelector('svg');
        if (icon) {
          icon.classList.toggle('hidden');
        }
      });
    });
  }
}

/**
 * Alert Component
 * Mostrar alertas con auto-dismiss
 */
class Alert {
  static show(message, type = 'info', duration = 5000, container = null) {
    const alertContainer = container || document.querySelector('.alerts-container') || document.body;

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} animate-slide-in`;
    alert.setAttribute('role', 'alert');
    alert.setAttribute('aria-live', 'polite');

    // Ícono según tipo
    const icons = {
      error: '✗',
      success: '✓',
      warning: '⚠',
      info: 'ℹ',
    };

    alert.innerHTML = `
      <span class="alert-icon">${icons[type] || 'ℹ'}</span>
      <div class="alert-content">${message}</div>
      <button class="alert-close" aria-label="Cerrar alerta">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    `;

    // Cerrar manualmente
    alert.querySelector('.alert-close').addEventListener('click', () => {
      alert.remove();
    });

    alertContainer.appendChild(alert);

    // Auto-dismiss
    if (duration > 0) {
      setTimeout(() => alert.remove(), duration);
    }

    return alert;
  }

  static error(message, duration = 5000) {
    return Alert.show(message, 'error', duration);
  }

  static success(message, duration = 5000) {
    return Alert.show(message, 'success', duration);
  }

  static warning(message, duration = 0) {
    return Alert.show(message, 'warning', duration);
  }

  static info(message, duration = 0) {
    return Alert.show(message, 'info', duration);
  }
}

/**
 * Loading State Manager
 * Gestiona el estado de carga de botones y formularios
 */
class LoadingState {
  static enable(buttonSelector) {
    const btn = document.querySelector(buttonSelector);
    if (!btn) return;

    btn.disabled = true;
    btn.classList.add('loading');
    btn.dataset.originalText = btn.textContent;
    btn.textContent = '';
  }

  static disable(buttonSelector) {
    const btn = document.querySelector(buttonSelector);
    if (!btn) return;

    btn.disabled = false;
    btn.classList.remove('loading');
    btn.textContent = btn.dataset.originalText || 'Enviar';
  }

  static toggle(buttonSelector) {
    const btn = document.querySelector(buttonSelector);
    if (!btn) return;

    if (btn.classList.contains('loading')) {
      this.disable(buttonSelector);
    } else {
      this.enable(buttonSelector);
    }
  }
}

/**
 * Inicialización en el DOM
 */
document.addEventListener('DOMContentLoaded', () => {
  // Password toggle
  new PasswordToggle();

  // Inicializar tooltips si existen
  document.querySelectorAll('[data-tooltip]').forEach((el) => {
    el.addEventListener('mouseenter', (e) => {
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip';
      tooltip.textContent = el.dataset.tooltip;
      document.body.appendChild(tooltip);

      const rect = el.getBoundingClientRect();
      tooltip.style.position = 'fixed';
      tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
      tooltip.style.left = rect.left + 'px';
      tooltip.style.zIndex = '9999';

      el.addEventListener(
        'mouseleave',
        () => tooltip.remove(),
        { once: true }
      );
    });
  });
});

// Exportar para uso externo
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    FormValidator,
    ValidationRules,
    PasswordToggle,
    Alert,
    LoadingState,
  };
}
