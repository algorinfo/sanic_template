<template>
<div class="container max-w-md mb-3">
	<div class="container max-w-md mb-3">
    <div class="flex flex-col my-1">
      <label class="dark:text-gray-200">Title</label>
      <input type="text" class="p-2 border-4 border-black dark:border-indigo-500 rounded-lg" />
    </div>
    <div class="flex flex-col my-1">
      <label class="dark:text-gray-200">Author</label>
      <input type="text" class="p-2 border-4 border-black dark:border-indigo-500 rounded-lg" />
    </div>
    <div class="flex flex-row my-1">
      <div class="flex flex-col">
        <label class="dark:text-gray-200">Category</label>
        <input type="text" class="p-2 border-4 border-black dark:border-indigo-500 rounded-lg" />
      </div>
      <div class="mx-2 my-auto">
        <button class="flex focus:outline-none hover:bg-indigo-600 dark:text-indigo-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </button>
      </div>

    </div>
    <div class="flex flex-col ml-3">
      <label class="dark:text-gray-200">Create</label>
      <input type="text" class="p-2 border-4 border-black dark:border-indigo-500 rounded-lg" />
    </div>


  </div>

	<Editor @sendText="getTextEditor" ></Editor>
</div>
</template>

<script>
import Editor from "../components/Editor.vue"
// Following composition-api
// https://v3.vuejs.org/guide/composition-api-introduction.html#setup-component-option

export default {
  components: { Editor },
	data(){
		return {
			user: "test"
		}
	},
  setup() {
    console.log("Hi starter index!") 

		const getTextEditor = function(data){
			console.log("Data from editor: ", data)

		}
    return {
			getTextEditor
		} 
  }
}


</script>