<template>
  <v-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    max-width="750px"
    persistent
  >
    <v-card>
      <v-card-title class="text-h6">
        Edit Showcase
      </v-card-title>

      <v-card-text>
        <!-- TOP MOVIES -->
        <div class="editor-section">
          <h3>Top Movies</h3>
          <div
            v-for="(item, i) in draft.topMovies"
            :key="item.mediaId"
            class="editor-item"
          >
            <span>{{ item.media?.title }}</span>
            <div class="controls">
              <v-btn icon size="small" @click="moveUp(draft.topMovies, i)" :disabled="i === 0">
                <v-icon>mdi-arrow-up</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="moveDown(draft.topMovies, i)" :disabled="i === draft.topMovies.length - 1">
                <v-icon>mdi-arrow-down</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="removeItem(draft.topMovies, i)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </div>
        </div>

        <!-- TOP TV -->
        <div class="editor-section mt-6">
          <h3>Top TV</h3>
          <div
            v-for="(item, i) in draft.topTv"
            :key="item.mediaId"
            class="editor-item"
          >
            <span>{{ item.media?.title }}</span>
            <div class="controls">
              <v-btn icon size="small" @click="moveUp(draft.topTv, i)" :disabled="i === 0">
                <v-icon>mdi-arrow-up</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="moveDown(draft.topTv, i)" :disabled="i === draft.topTv.length - 1">
                <v-icon>mdi-arrow-down</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="removeItem(draft.topTv, i)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </div>
        </div>

        <!-- FAVORITE SERIES -->
        <div class="editor-section mt-6">
          <h3>Favourite Series</h3>
          <div
            v-for="(item, i) in draft.favSeries"
            :key="item.mediaId"
            class="editor-item"
          >
            <span>{{ item.tmdbCollectionName || item.media?.title }}</span>
            <div class="controls">
              <v-btn icon size="small" @click="moveUp(draft.favSeries, i)" :disabled="i === 0">
                <v-icon>mdi-arrow-up</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="moveDown(draft.favSeries, i)" :disabled="i === draft.favSeries.length - 1">
                <v-icon>mdi-arrow-down</v-icon>
              </v-btn>
              <v-btn icon size="small" @click="removeItem(draft.favSeries, i)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </div>
        </div>

        <!-- HIDDEN GEM -->
        <div class="editor-section mt-6">
          <h3>Hidden Gem</h3>
          <v-select
            :items="mediaList"
            item-title="title"
            item-value="mediaId"
            v-model="draft.hiddenGem.mediaId"
            label="Pick hidden gem"
          />
          <v-textarea
            v-model="draft.hiddenGem.note"
            label="Why is this special?"
            class="mt-3"
          />
        </div>
      </v-card-text>

      <v-card-actions>
        <v-btn variant="text" @click="close">Cancel</v-btn>
        <v-btn color="primary" @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { showcaseAPI } from "@/services/showcase-api";

export default {
  name: "ShowcaseEditor",

  props: {
    modelValue: Boolean,
    currentShowcase: Object,
    mediaList: Array,
  },

  emits: ["update:modelValue", "saved"],

  data() {
    return {
      draft: JSON.parse(JSON.stringify(this.currentShowcase)),
    };
  },

  methods: {
    close() {
      this.$emit("update:modelValue", false);
    },

    moveUp(list, i) {
      const temp = list[i - 1];
      list[i - 1] = list[i];
      list[i] = temp;
    },

    moveDown(list, i) {
      const temp = list[i + 1];
      list[i + 1] = list[i];
      list[i] = temp;
    },

    removeItem(list, i) {
      list.splice(i, 1);
    },

    async save() {
      const updated = await showcaseAPI.save(this.draft);
      this.$emit("saved", this.draft);
      this.close();
    },
  },
};
</script>

<style scoped>
.editor-section h3 {
  font-weight: 700;
  margin-bottom: 10px;
}

.editor-item {
  padding: 8px;
  background: rgba(255,255,255,0.08);
  border-radius: 6px;
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.controls {
  display: flex;
  gap: 4px;
}
</style>