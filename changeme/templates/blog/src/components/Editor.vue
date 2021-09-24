<template>
<div class="flex-grow">
        <button v-on:click="addImage()" class="bg-red-500">Add image
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 dark:text-indigo-500" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </button>
        <button >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 dark:text-indigo-500" fill="none" viewBox="0 0 24 24"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
        </button>

        <button @click="toggleBold()" class="btn" >
          B
        </button>
        <button class="btn" @click="toggleHeading(1)"
          >
          H1
        </button>
        <button class="btn" @click="toggleHeading(2)"
          >
          H2
        </button>
        <button class="btn" @click="toggleHeading(3)"
          >
          H3
        </button>
      </div>

  <editor-content class="flex-grow
          my-5
          p-2
          border-4 border-black
          dark:border-indigo-600
          bg-white
          rounded-lg
          prose
        " :editor="editor" />

  <button class="btn-left" @click="send()">Send</button>
</template>

<script>
import { Editor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from "@tiptap/extension-image";

export default {
  components: {
    EditorContent,
  },
  emits: ['sendText'], 
  data() {
    return {
      editor: null,
    }
  },
  methods:{
    addImage(){
      const url = window.prompt("URL")
      if (url){
        this.editor.chain().focus().setImage({src: url}).run()
      }

    },
    send(){
      console.log("Sending text...")
      this.$emit("sendText", this.editor.getHTML())
    },

  },
  mounted() {
    this.editor = new Editor({
      content: '<p>I’m running tiptap with Vue.js. 🎉</p>',
      extensions: [
        StarterKit,
        Image,
      ],
    })
  },

  beforeUnmount() {
    this.editor.destroy()
  },
}
</script>