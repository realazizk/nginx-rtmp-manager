<template>
    <div class="container">
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Stream Name</th>
                    <th>Stream Type</th>
                    <th>Delete</th>
                </tr>
            </thead>
            <tbody>
	      <tr v-for="(row, index) in streams">
		<td>{{ row.name }}</td>
		<td>{{ row.stype }}</td>
		<td><a @click="removeRow(row, index)">Remove</a></td>
	      </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import {API_URL} from '@/shared.js'
import auth from '@/auth'

export default {
  data() {
    return {
      streams: []
    }
  },

  methods: {
    removeRow(row, index) {
      var vm = this
      this.$http.delete(
	API_URL + 'api/stream/' + row.id,
	{headers: auth.getAuthHeader()}
      ).then(
	response => {
	  vm.$delete(vm.streams, index)
	}, response => {
	  vm.$delete(vm.streams, index)
	})
    }
  },
  
  created() {
    // grab user streams
    this.$http.get(API_URL + 'api/streams', {headers: auth.getAuthHeader()}).then(
      response => {
	let data = response.body
	this.streams = data
      })
  }
}
  
</script>


<style scoped>
</style>

