<template>
  <div class="login-view">
    <v-card max-width="500" class="mx-auto mt-10" elevation="4">
      <v-card-title class="text-h5 text-center bg-primary">
        Login to Your Movie Diary
      </v-card-title>
      
      <v-card-text class="pa-6">
        <v-alert v-if="error" type="error" class="mb-4">
          {{ error }}
        </v-alert>
        
        <v-form @submit.prevent="handleLogin">
          <v-text-field
            v-model="username"
            label="Username"
            prepend-icon="mdi-account"
            required
            :disabled="isSubmitting"
          />
          
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            prepend-icon="mdi-lock"
            required
            :disabled="isSubmitting"
          />
          
          <v-btn
            type="submit"
            color="primary"
            block
            size="large"
            :loading="isSubmitting"
            :disabled="!username || !password"
            class="mt-4"
          >
            Login
          </v-btn>
        </v-form>
        
        <div class="text-center mt-4">
          <p class="text-body-2">
            Don't have an account?
            <router-link to="/register" class="text-primary">Register here</router-link>
          </p>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { authAPI } from '@/services/api';

export default {
  name: 'LoginView',
  
  data() {
    return {
      username: '',
      password: '',
      error: null,
      isSubmitting: false
    };
  },
  
  methods: {
    async handleLogin() {
      this.isSubmitting = true;
      this.error = null;
      
      try {
        const response = await authAPI.login(this.username, this.password);
        
        // Store token in localStorage
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('user', JSON.stringify(response.user));
        
        // Redirect to movies page
        this.$router.push('/movies');
        
      } catch (err) {
        console.error('Login error:', err);
        this.error = err.message || 'Invalid username or password';
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.login-view {
  min-height: 80vh;
  display: flex;
  align-items: center;
}
</style>