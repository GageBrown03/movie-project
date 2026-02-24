<template>
  <v-dialog v-model="modelValue" max-width="750px" persistent>
    <v-card>
      <v-card-title class="text-h6">
        Edit Showcase
      </v-card-title>

      <v-card-text>
        <div class="editor-section">
          <h3>Top Movies</h3>
          <draggable v-model="draft.topMovies" item-key="mediaId">
            <template #item="{ element }">
              <div class="editor-item">
                {{ element.media?.title }}
              </div>
            </template>
          </draggable>
        </div>

        <div class="editor-section mt-6">
          <h3>Top TV</h3>
          <draggable v-model="draft.topTv" item-key="mediaId">
            <template #item="{ element }">
              <div class="editor-item">
                {{ element.media?.title }}
              </div>
            </template>
          </draggable>
        </div>

        <div class="editor-section mt-6">
          <h3>Favourite Series</h3>
          <draggable v-model="draft.favSeries" item-key="mediaId">
            <template #item="{ element }">
              <div class="editor-item">
                {{ element.tmdbCollectionName || element.media?.title }}
              </div>
            </template>
          </draggable>
        </div>

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
import draggable from "vuedraggable";
import { showcaseAPI } from "@/services/showcase-api";

export default {
  name: "ShowcaseEditor",
  components: { draggable },

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

    async save() {
      await showcaseAPI.save(this.draft);
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
  background: rgba(255,255,255,0.1);
  border-radius: 6px;
  margin-bottom: 6px;
}
</style>
``