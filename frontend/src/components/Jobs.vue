<template>

    <div class="container">
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>{{$t('jobsp.streamchannel')}}</th>
                    <th>{{$t('jobsp.starttime')}}</th>
                    <th>{{$t('jobsp.endtime')}}</th>
                    <th>{{$t('jobsp.filename')}}</th>
		    <th></th>
                </tr>
            </thead>
            <tbody>
	      <tr v-for="(row, index) in jobs">
		<td>{{ row.stream.name }}</td>
		<td>{{ row.streamstart }}</td>
		<td>{{ row.streamfinish }}</td>
		<td>{{ row.filename }}</td>

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
      jobs: {}
    }
  },
  methods: {
    removeRow(row, index) {
      var vm = this
      this.$http.delete(
	API_URL + 'api/job/' + row.id,
	{headers: auth.getAuthHeader()}
      ).then(
	response => {
	  vm.$delete(vm.jobs, index)
	}, response => {
	  vm.$delete(vm.jobs, index)
	})
    }
  },
  created() {
    this.$http.get(API_URL + 'api/jobs', {headers: auth.getAuthHeader()}).then(
      response => {
	let data = response.body
	this.jobs = data
      })
  }
}
</script>
