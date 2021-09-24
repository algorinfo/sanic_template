module.exports = {
  "env": {
    "browser": true,
    "es2021": true,
    "node": true,
  },
  "extends": [
    "eslint:recommended",
    "plugin:vue/essential"
  ],
  "parserOptions": {
    "ecmaVersion": 12,
    "sourceType": "module"
  },
  "plugins": [
    "html",
    "vue",
    "prettier",
    "json"
  ],
  "rules": {
    "indent": [
      "error",
      2
    ],
  }
};
