<template>
  <div class="register-view">
    <v-card max-width="500" class="mx-auto mt-10" elevation="4">
      <v-card-title class="text-h5 text-center bg-primary">
        Create Your Account
      </v-card-title>
      
      <v-card-text class="pa-6">
        <v-alert v-if="error" type="error" class="mb-4">
          {{ error }}
        </v-alert>
        
        <v-form @submit.prevent="handleRegister">
          <v-text-field
            v-model="username"
            label="Username"
            prepend-icon="mdi-account"
            hint="At least 3 characters"
            required
            :disabled="isSubmitting"
          />
          
          <v-text-field
            v-model="email"
            label="Email"
            type="email"
            prepend-icon="mdi-email"
            required
            :disabled="isSubmitting"
          />
          
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            prepend-icon="mdi-lock"
            hint="At least 6 characters"
            required
            :disabled="isSubmitting"
          />
          
          <v-text-field
            v-model="confirmPassword"
            label="Confirm Password"
            type="password"
            prepend-icon="mdi-lock-check"
            required
            :disabled="isSubmitting"
          />
          
          <v-btn
            type="submit"
            color="primary"
            block
            size="large"
            :loading="isSubmitting"
            :disabled="!isFormValid"
            class="mt-4"
          >
            Register
          </v-btn>
        </v-form>
        
        <div class="text-center mt-4">
          <p class="text-body-2">
            Already have an account?
            <router-link to="/login" class="text-primary">Login here</router-link>
          </p>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { authAPI } from '@/services/api-production';

export default {
  name: 'RegisterView',
  
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      error: null,
      isSubmitting: false
    };
  },
  
  computed: {
    isFormValid() {
      return this.username.length >= 3 &&
             this.email.includes('@') &&
             this.password.length >= 6 &&
             this.password === this.confirmPassword;
    }
  },
  
  methods: {
    async handleRegister() {
      // Validate passwords match
      if (this.password !== this.confirmPassword) {
        this.error = 'Passwords do not match';
        return;
      }
      
      this.isSubmitting = true;
      this.error = null;
      
      try {
        const response = await authAPI.register(
          this.username,
          this.email,
          this.password
        );
        
        // Store token in localStorage
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));
        
        // Redirect to movies page
        this.$router.push('/movies');
        
      } catch (err) {
        console.error('Registration error:', err);
        this.error = err.message || 'Registration failed. Please try again.';
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.register-view {
  min-height: 80vh;
  display: flex;
  align-items: center;
}
</style>