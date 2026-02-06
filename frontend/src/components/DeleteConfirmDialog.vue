<template>
  <v-dialog v-model="internalShow" max-width="500">
    <v-card>
      <v-card-title class="text-h5 text-error">
        Delete Movie?
      </v-card-title>
      
      <v-card-text>
        <p class="text-body-1">
          Are you sure you want to delete <strong>{{ movieTitle }}</strong>?
        </p>
        <p class="text-body-2 text-medium-emphasis mt-2">
          This action cannot be undone.
        </p>
      </v-card-text>
      
      <v-card-actions>
        <v-spacer />
        <v-btn
          variant="text"
          @click="cancel"
        >
          Cancel
        </v-btn>
        <v-btn
          color="error"
          variant="flat"
          @click="confirm"
          :loading="deleting"
        >
          Delete
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'DeleteConfirmDialog',
  
  props: {
    show: {
      type: Boolean,
      required: true
    },
    movieTitle: {
      type: String,
      required: true
    },
    deleting: {
      type: Boolean,
      default: false
    }
  },
  
  computed: {
    internalShow: {
      get() {
        return this.show;
      },
      set(value) {
        if (!value) {
          this.$emit('cancel');
        }
      }
    }
  },
  
  methods: {
    cancel() {
      this.$emit('cancel');
    },
    confirm() {
      this.$emit('confirm');
    }
  }
};
</script>