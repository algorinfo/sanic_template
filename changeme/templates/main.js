import "./tailwind.css";
import Alpine from "alpinejs";
import { Editor } from "@tiptap/core";
import StarterKit from "@tiptap/starter-kit";
import Image from "@tiptap/extension-image";
// ai is my namespace

window.Alpine = Alpine;

Alpine.data("darkMode", () => ({
  mobileMenuOpen: false,
  init() {
    this.aiCheckTheme();
  },

  aiCheckTheme() {
    const html = document.getElementsByTagName("html")[0];
    if (
      localStorage.theme === "dark" ||
      (!("theme" in localStorage) &&
        window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      // document.documentElement.classList.add('dark')

      html.classList.add("dark");
      html.classList.remove("white");
    } else {
      html.classList.add("white");
      html.classList.remove("dark");
    }
  },
  toggle() {
    const html = document.getElementsByTagName("html")[0];
    if (html.classList.contains("dark")) {
      html.classList.remove("dark");
      html.classList.add("white");
      localStorage.theme = "white";
    } else {
      html.classList.add("dark");
      html.classList.remove("white");
      localStorage.theme = "dark";
    }
  },
  toggleMenu() {
    console.log("BEFORE!: ", this.mobileMenuOpen);
    this.mobileMenuOpen = !this.mobileMenuOpen;
    console.log("AFTER!: ", this.mobileMenuOpen);
  },
}));

Alpine.data("imageViewer", () => ({
  imageUrl: "",
  fileChosen(evt) {
    this.fileToDataUrl(evt, (src) => (this.imageUrl = src));
  },
  init() {
    console.log("Image init");
  },
  fileToDataUrl(event, callback) {
    console.log("Calle...", event);

    if (!event.target.files.length) return;

    let file = event.target.files[0],
      reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = (e) => callback(e.target.result);
  },
}));

Alpine.data("editorJs", () => ({
  editor: null,
  content: "<p>Hello!</p>",
  updatedAt: Date.now(),

  init() {
    this.editor = new Editor({
      element: this.$refs.text,
      extensions: [StarterKit, Image],
      content: this.content,
      onUpdate: ({ editor }) => {
        this.content = editor.getHTML();
        console.log("Updated");
      },
      onSelectionUpdate: () => {
        this.updatedAt = Date.now();
      },
    });
  },
  send() {
    console.log(this.editor.getHTML());
  },
}));

// https://github.com/ueberdosis/tiptap/issues/1515

Alpine.data("editor", (content) => {
  let editor;

  return {
    // Passing updatedAt here to make Alpine
    // rerender the menu buttons.
    //
    // The value of updatedAt will be updated
    // on every Tiptap transaction.
    //
    isActive(type, opts = {}, updatedAt) {
      return editor.isActive(type, opts);
    },
    toggleBold() {
      editor.chain().toggleBold().focus().run();
    },
    send() {
      console.log(editor.getHTML());
    },
    addImage() {
      const url = window.prompt("URL");
      if (url) {
        editor.chain().focus().setImage({ src: url }).run();
      }
    },
    toggleHeading(level) {
      editor.chain().toggleHeading({ level: level }).focus().run();
    },
    updatedAt: Date.now(),
    init() {
      const _this = this;

      editor = new Editor({
        element: this.$refs.editorReference,
        extensions: [StarterKit, Image],
        content: content,
        onCreate({ editor }) {
          _this.updatedAt = Date.now();
        },
        onUpdate({ editor }) {
          _this.updatedAt = Date.now();
        },
        onSelectionUpdate({ editor }) {
          _this.updatedAt = Date.now();
        },
      });
    },
  };
});

/*window.setupEditor = function(content) {
  return {
    editor: null,
    content: content,
    updatedAt: Date.now(), // force Alpine to rerender on selection change
    init(element) {
      this.editor = new Editor({
        element: element,
        extensions: [
          StarterKit,
        ],
        content: this.content,
        onUpdate: ({ editor }) => {
          this.content = editor.getHTML()
        },
        onSelectionUpdate: () => {
          this.updatedAt = Date.now()
        },
      })
    },
  }
}*/

console.log("Hi!");

Alpine.start();

/*document.querySelector('#app').innerHTML = `
  <h1>Hello Vite!</h1>
  <a href="https://vitejs.dev/guide/features.html" target="_blank">Documentation</a>
`
*/
