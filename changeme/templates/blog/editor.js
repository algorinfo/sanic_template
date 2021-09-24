import { createApp } from "vue";
// import "./index.css";
import App from "./src/App.vue";
import { createRouter, createWebHistory } from "vue-router";
// import utils from "./utils";
import routes from "virtual:generated-pages";
const router = createRouter({
  history: createWebHistory(),
  routes,
});

console.log("Hello from editor.js")
const app = createApp(App);

app.use(router).mount("#editorapp");